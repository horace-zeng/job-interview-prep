# job-interview-prep

> 把「求职备考」从一堆零散笔记，变成一条可重复、可评测、可交付的生产线。

*A reusable Mavis agent skill that turns job-hunt preparation into a repeatable pipeline: company research → interview-format triage → question bank & verbatim answer scripts → validated HTML + A4 PDF handbook.*

---

## 它解决什么

大多数人的面试准备停在「我准备了这个岗位」。真正费时、又容易悄悄做错的是中间那几步：

- 公司到底做什么、这个岗位每天面对什么文件——查半天才拼出一个模糊印象
- 不知道这轮是群面、结构化、还是 AI 视频——题准备错了方向
- 答案写得漂亮，但没有逻辑链，面试官一追就散架
- 追问接不住；个人化问题没准备，一题定生死
- 交付一堆自己不会再看的文档

这个 skill 把这条路径固化成 **10 步**，每一步都有明确判据、明确的失败处理、明确的产出格式。

## 它不是模板，是流水线

四个关键设计（其余见 `SKILL.md`）：

**1 · 面试形式判定不能跳过。**
先检索该公司该岗位近两年的公开面经，再问用户确认形式（群面 / 结构化 / AI 视频 / 英文场 / 有无笔试）。
形式决定题目形态——结构化面试必须有追问树，群面必须有站位与抢话节奏。
没有提问工具时**不要卡住**：降级为「声明假设 + 双轨覆盖 + 一句可自行求证的话术」，并在材料里标注「本场形式属推断」。

**2 · 答案三段式。**

```
关键词      锚点词（3–5 个）+ 可替换表述池
思考逻辑链  题眼 → 判据 →【转折点】→ 判据 → 素材 → 落点
完整回答    可直接说出口的逐字稿，标时间预算，分 30 / 60 / 90–100 秒三档
```

**3 · 结构化面试必须带追问树。**
同一道主问题往下追 5 层，每一层都写清「追问原文 + 答题要点 + 素材挂载点 + 禁答」，并且必须落到用户自己的真实素材上。

**4 · 交付必须过校验。**
HTML 结构配平 / id 唯一 / 锚点可达 / PDF 命名目标覆盖率 / 页跨度与测算一致 / 无孤儿页——六项全过才算交付。

## 目录结构

```
job-interview-prep/
├── SKILL.md                       # 触发条件 + 10 步流程 + 输出契约 + 失败处理
├── README.md                      # 本文件
├── LICENSE                        # MIT
├── references/
│   ├── README.md                  # 何时读哪一份 reference 的索引
│   ├── research-playbook.md       # 公司/财报/岗位属性/文件清单/查证纪律/面经检索
│   ├── question-bank.md           # 8 种面试形式对照表、追问树、群面七块打法、反问
│   ├── answer-format.md           # 三段式写法 + 差/好答案对照 + 分层编排
│   ├── deliverable-html-pdf.md    # 构建管线 + 五个静默坑
│   └── debrief-compare.md         # 岗位对比表、逐题判分、硬失分点、亮点清单
└── scripts/
    ├── verify_handbook.py         # HTML + PDF 全量校验（纯本地，pymupdf 可选）
    └── measure_sections.cjs       # Playwright 量各节内容高，供回填 min-height
```

## 安装

Mavis 支持从 Git URL 直接安装 skill（repo 根目录必须含 `SKILL.md`）：

```bash
# 全局安装（所有 agent 可见）
git clone https://github.com/horace-zeng/job-interview-prep.git ~/.minimax/skills/job-interview-prep

# 或只装给某一个 agent（把 mavis 换成你的 agent 名）
git clone https://github.com/horace-zeng/job-interview-prep.git ~/.minimax/agents/mavis/skills/job-interview-prep
```

Windows PowerShell：

```powershell
git clone https://github.com/horace-zeng/job-interview-prep.git "$env:USERPROFILE\.minimax\skills\job-interview-prep"
```

也可以直接把整个目录复制到上述位置。**技能在下一个 session 生效，不需要重启运行时。**

验证安装：`skill({ name: "job-interview-prep" })` 能读到 `Location:` 即成功。

### 装不上？先看这两条

| 症状 | 原因 | 处理 |
|---|---|---|
| `error: The requested URL returned error: 400` | clone 地址里还残留 `<你的用户名>` 这类占位符 | `<` `>` 不是合法 URL 字符，GitHub 会直接拒收；把占位符换成真实用户名再试 |
| `Repository not found` | 用户名或仓库名拼错，或仓库不是公开的 | 核对仓库地址；公开仓库 clone 不需要认证 |

> 占位符是这类 README 最常见的残留物。**clone 报 400，八成不是 GitHub 挂了，是地址里还有尖括号。**

## 触发语

装好后，下面这些说法会激活它：

- 「帮我准备 XX 公司的面试」「我在面 XX 岗位，JD 在这里」
- 「这题怎么答」「群面 XX 题的打法」「结构化面试的追问」
- 「面试复盘」「同时面了几家，帮我对比」
- 「我的自我介绍怎么写」「面试该反问什么」

## 它是怎么被造出来的

2026 年秋招季，我在准备一个真实岗位时踩了足够多的坑，最后决定把它固化成 skill——不是写模板，而是写一条**能被检验的流程**。

过程本身也是这个 skill 的一部分：

1. **多轮实战**——同一岗位连续追问深挖，群面题改了三次才找到真正考点（「拓张还是维系」看着是二选一，其实考的是"增长瓶颈卡在漏斗哪一段"）。
2. **提炼**——把散落在几十轮对话里的做法收敛成 10 步，每步挂判据。
3. **写评测**——同一个 prompt 交给两个独立子代理：一个加载 skill，一个不加载，各自产出后逐点对比。
4. **被评测打脸**——第一轮对比暴露了 skill 自己的 5 个缺口，全部改掉。

### 评测暴露的问题与改法

| 评测暴露的问题 | 改法 |
|---|---|
| 数字口径冲突时只并列不给结论 → 用户带着两个数字上考场 | 强制同时给「面试用口径」并说明依据（更新者优先） |
| 没要求挖「这家公司的人是怎么选出来的」→ 答法基调定错 | Step 2 新增第 5 项产出：校招生占比 / 管理层培养机制 ⇒ 考察「可塑性」还是「当下产出」 |
| 关键词限死 3–5 个会丢细节 | 改两栏：锚点词 3–5（记忆负担上限）+ 可替换表述池（说法的弹药库） |
| 逐字稿没标时间预算 → 不知道哪句能临场省略 | 每层标时间预算；长度分档改为必备 30 / 60 / 90–100 秒 |
| 只写「要问用户形式」，没写没有提问工具时怎么办 | 补降级路径：声明假设 + 双轨覆盖 + 一句求证话术 |

## 交付管线里的五个静默坑

这一节是给要复用它的工程师看的——这几个坑**不报错、不崩溃，只表现为页数暴涨或点击失效**：

1. **PDF 渲染器只为被 `href="#id"` 引用过的 id 建命名目标。** 目录里漏掉一节，那节在 PDF 里就点不到、也没有书签。
2. **批量生成目录行时，去重条件必须「整组只让全局第一个触发」。** 写成「跳过组内非首成员」会让每个首成员各吐一遍整块：实测目录从 54 行静默涨到 153 行、PDF 白涨 3 页。
3. **改内容后必须 build → measure → converge 三步全跑。** 收敛脚本只从已渲染 PDF 回读实际页跨度、不重算内容高，沿用旧值会把目录撑到白占几页。
4. **孤页（末页只剩一两百字）的修法是压间距，不是删内容。** 优先动 `line-height` 与表格 padding；收紧 `.callout` 的 padding 会触发回流反而撑高。
5. **DOM 量高 ≠ 打印页数，但打印宽度一致。** `.page` 固定宽度 210mm，测量时不必模拟 A4 纸宽；但 `break-inside: avoid` 会让实际跨度大于算出来的值，min-height 必须用实际跨度回填。

## 边界

- 这是一个**方法论** skill：不含任何个人简历、公司内部资料或面经原文。
- 事实类内容必须带来源与期数；推演类必须标「情景推演」；用户未提供的细节用占位或三档话术处理。
- **不编造**：检索不到就写「公开信息未披露」，宁可少给一个数字，不给错一个。

## License

MIT — 详见 [LICENSE](LICENSE)。Copyright (c) 2026 Haorong Zeng。
