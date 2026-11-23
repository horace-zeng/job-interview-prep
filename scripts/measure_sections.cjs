#!/usr/bin/env node
/**
 * measure_sections.cjs — 量手册里每个 .page 节的内容高度，供回填 min-height。
 *
 * 用法:
 *   node measure_sections.cjs <handbook.html> [out.json]
 *
 * 原理: 打印分页与连续流不同（break-inside: avoid 的块会整块跳页），
 *       所以先在 DOM 里量内容高得到"理论页数"，再由收敛脚本从渲染后的 PDF
 *       回读各节"实际页跨度"，两者取实际值回填 min-height。
 *
 * 依赖: playwright（找不到时回退到 npm root -g）。没有 playwright 就直接跳过这步，
 *       改用保守页数，不要因此卡住交付。
 */
const path = require('path');
const fs = require('fs');
const { execSync } = require('child_process');

function loadPlaywright() {
  try { return require('playwright'); } catch (_) {}
  const root = execSync('npm root -g', { stdio: ['ignore', 'pipe', 'ignore'] }).toString().trim();
  return require(path.join(root, 'playwright'));
}

const htmlPath = process.argv[2];
const outPath = process.argv[3] || htmlPath.replace(/\.html?$/i, '') + '_fills.json';
if (!htmlPath || !fs.existsSync(htmlPath)) {
  console.error('用法: node measure_sections.cjs <handbook.html> [out.json]');
  process.exit(2);
}

const PAGE_PT = 840;          // A4 页高 842.88pt，留 2.88pt 余量
const CSS_PX_PER_PT = 96 / 72;

(async () => {
  let chromium;
  try { ({ chromium } = loadPlaywright()); }
  catch (e) {
    console.error('[skip] 未找到 playwright，跳过测量。');
    process.exit(0);
  }
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1400, height: 1200 } });
  await page.goto('file:///' + path.resolve(htmlPath).replace(/\\/g, '/'), { waitUntil: 'load' });

  const data = await page.evaluate(() => {
    const out = [];
    document.querySelectorAll('.page.section, .page.toc').forEach((el) => {
      const prev = el.style.minHeight;
      el.style.minHeight = '0px';
      const h = el.getBoundingClientRect().height;
      el.style.minHeight = prev;
      out.push({ id: el.id, h: h });
    });
    return out;
  });

  const res = data.map((d) => {
    const pt = Math.round(d.h / CSS_PX_PER_PT);
    const pages = Math.max(1, Math.ceil(pt / PAGE_PT - 0.001));
    return { id: d.id, pt, pages, mh: pages * PAGE_PT };
  });

  let total = 0;
  res.forEach((r) => {
    total += r.pages;
    console.log(`${r.id.padEnd(10)} content=${String(r.pt).padStart(5)}pt -> ${r.pages}p, min-height=${r.mh}pt`);
  });
  console.log('TOTAL section pages:', total);

  fs.writeFileSync(outPath, JSON.stringify(res, null, 0), 'utf8');
  console.log('written:', outPath);
  await browser.close();
})();
