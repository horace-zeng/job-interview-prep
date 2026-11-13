#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""校验面试备考手册的 HTML 与 PDF。

用法:
    python verify_handbook.py <handbook.html> [handbook.pdf] [--fills fills.json]

检查项
  HTML : 标签配平 / id 唯一 / href="#id" 全部可达 / 每个 section 是否被目录引用
  PDF  : 页数与页面尺寸 / 命名目标覆盖率 / 各节实际页跨度与 fills 是否一致 / 孤儿页

退出码: 0 = 全部通过, 1 = 有 FAIL, 2 = 参数或文件错误。
pymupdf 缺失时自动跳过 PDF 检查（只报 HTML 结果），不视为失败。
"""
import io
import json
import os
import re
import sys

TAGS = ['div', 'span', 'ul', 'ol', 'li', 'table', 'tr', 'td', 'th', 'p',
        'h1', 'h2', 'h3', 'h4', 'h5', 'strong', 'em', 'a', 'b', 'i', 'ul', 'ol']
PAGE_RE = re.compile(r'<div class="page (?:toc|section)" id="([^"]+)"')
HREF_RE = re.compile(r'href="#([^"]+)"')
ID_RE = re.compile(r'\bid="([^"]+)"')

problems = []
notes = []


def fail(msg):
    problems.append(msg)


def check_html(path):
    src = io.open(path, encoding='utf-8').read()
    for tag in TAGS:
        opens = len(re.findall(r'<%s[ >]' % tag, src))
        closes = src.count('</%s>' % tag)
        if opens != closes:
            fail('HTML 标签未配平: <%s> %d 个 vs </%s> %d 个' % (tag, opens, tag, closes))

    ids = ID_RE.findall(src)
    dup = sorted({i for i in ids if ids.count(i) > 1})
    if dup:
        fail('HTML id 重复: %s' % dup)

    idset = set(ids)
    hrefs = HREF_RE.findall(src)
    broken = sorted(set(hrefs) - idset)
    if broken:
        fail('锚点指向不存在的 id: %s' % broken)

    sections = PAGE_RE.findall(src)
    unlinked = sorted(set(sections) - set(hrefs))
    if unlinked:
        fail('这些节没有任何 href 引用（PDF 里将没有命名目标、点不到）: %s' % unlinked)

    notes.append('HTML: %d 节, %d 锚点引用, %d 个 id' % (len(sections), len(hrefs), len(ids)))
    return src, sections


def check_pdf(pdf_path, sections, fills_path=None):
    try:
        import pymupdf
    except ImportError:
        try:
            import fitz as pymupdf
        except ImportError:
            notes.append('PDF: 跳过（未安装 pymupdf）')
            return

    doc = pymupdf.open(pdf_path)
    rect = doc[0].rect
    notes.append('PDF: %d 页, 尺寸 %.2f x %.2f pt' % (len(doc), rect.width, rect.height))
    if abs(rect.width - 595.92) > 1 or abs(rect.height - 842.88) > 1:
        notes.append('PDF: 尺寸不是 A4 (595.92 x 842.88)，确认是否有意为之')

    named = doc.resolve_names()
    missing = [s for s in sections if s not in named]
    if missing:
        fail('PDF 缺命名目标（目录里补 href="#id"）: %s' % missing)
    notes.append('PDF: 命名目标 %d/%d' % (len(named), len(sections)))

    pages = {k: named[k]['page'] + 1 for k in named}
    if fills_path and os.path.exists(fills_path):
        fills = {f['id']: f for f in json.load(io.open(fills_path, encoding='utf-8'))}
        for i, sid in enumerate(sections):
            if sid not in pages:
                continue
            nxt = pages.get(sections[i + 1], len(doc) + 1) if i + 1 < len(sections) else len(doc) + 1
            actual = nxt - pages[sid]
            expect = fills.get(sid, {}).get('pages')
            if expect is not None and actual != expect:
                fail('页跨度与测算不符: %s 实际 %d 页 / 测算 %d 页' % (sid, actual, expect))

    lens = [len(p.get_text().strip()) for p in doc]
    orphans = [(i + 1, n) for i, n in enumerate(lens) if n < 250]
    if orphans:
        fail('孤儿页（正文 < 250 字，需压间距或并页）: %s' % orphans)
    notes.append('PDF: 每页正文字符 min=%d max=%d' % (min(lens), max(lens)))


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    opts = [a for a in sys.argv[1:] if a.startswith('--')]
    if not args:
        print(__doc__)
        return 2
    html_path = args[0]
    if not os.path.exists(html_path):
        print('找不到文件: %s' % html_path)
        return 2
    pdf_path = args[1] if len(args) > 1 else os.path.splitext(html_path)[0] + '.pdf'
    fills_path = None
    for o in opts:
        if o.startswith('--fills'):
            fills_path = o.split('=', 1)[1] if '=' in o else (args[2] if len(args) > 2 else None)

    src, sections = check_html(html_path)
    if os.path.exists(pdf_path):
        check_pdf(pdf_path, sections, fills_path)
    else:
        notes.append('PDF: 跳过（%s 不存在）' % pdf_path)

    for n in notes:
        print('[info] %s' % n)
    for p in problems:
        print('[FAIL] %s' % p)
    if problems:
        print('\n结果: FAIL（%d 项）' % len(problems))
        return 1
    print('\n结果: PASS')
    return 0


if __name__ == '__main__':
    sys.exit(main())
