# 咨询报告写作助手 (Consulting Report Assistant)

> 别再让 AI 帮你「凑一篇」。这个 Skill 把咨询报告写作做成可追踪、可恢复、可复用、可评测的工程化流程——接管项目上下文、按场景路由模块、交付前自动清 AI 味，还能写招投标技术标。

![Agent Skill](https://img.shields.io/badge/Agent-Skill-6E56CF) ![Claude Code](https://img.shields.io/badge/Claude%20Code-✓-444) ![Codex · Cursor · Gemini](https://img.shields.io/badge/Codex·Cursor·Gemini-runtime--neutral-444) ![Tests](https://img.shields.io/badge/tests-35%20passing-2DA44E) ![License](https://img.shields.io/badge/License-MIT-blue)

SKILL.md 内容 runtime 中性，可在 Claude Code、Codex、Cursor、Gemini CLI 等读取 `SKILL.md` 的 Agent 里使用。

## 你什么时候需要它？

- **写长篇咨询交付**：战略 / 市场 / 专项研究、管理制度、实施方案、尽职调查——写到第二轮就丢上下文、丢决策，需要一个能记住项目状态的写法。
- **交付前要去 AI 味**：稿子读着「AI」，元叙事、套话、三段式、后台词泄漏混在一起，需要系统排查而不是手删几个词。
- **写招投标技术标**：被招标文件、技术规范书、评分标准三样反向约束，每章都要对上评分点、逐条应答——漏一个点就丢分。

## 它交付什么？

主产物是可迭代的项目内文本资产：报告正文（Markdown）、`plan/*.md` 项目上下文、图表脚本（Python），按需导出 `可审草稿`（docx）。

**可见证明 · 去 AI 味 before/after**（仓库内置 fixture，`bash scripts/quality_check.sh tests/fixtures/problematic-report.md` 可复现）：

```diff
- 首先，需要指出的是，该领域具有非常重要的战略价值。
- 技术规范书和内部材料已经在前期讨论中使用。
- 落款：XXX
+ 市场规模在过去三年持续增长。
+ 根据国家数据局 2025 年公开文件，企业数据开发利用要求正在加快明确。
+ 建议围绕重点场景建立数据供给、共享和评价闭环。
```

质检脚本对这两份稿子的真实打分：

| 文件 | 高风险 | 中风险 | 低风险 |
|---|---:|---:|---:|
| `problematic-report.md`（清洗前） | 3 | 3 | 2 |
| `clean-report.md`（清洗后） | 0 | 0 | 0 |

高风险命中占位符 `XXX`、后台词「内部材料」；中风险命中机械过渡词、空洞强调句；低风险命中图表跳号（图1→图3）。内容问题分级告警，不阻断流程。

## 安装

```bash
# 方式一：skills CLI（推荐，跨 runtime）
npx skills add https://github.com/zhyouhh/consulting-report-skill

# 方式二：手动复制到 Claude Code 个人 skills 目录
git clone https://github.com/zhyouhh/consulting-report-skill
cp -r consulting-report-skill ~/.claude/skills/consulting-report-assistant
```

装好后，跟 Agent 说「写一份……咨询报告」或「帮我去掉这份稿子的 AI 味」即可触发。

## 快速开始

### 第一步：初始化任务上下文

先明确四件事：目标、篇幅、时间、已有材料。只要不是一问一答型小问题，都建议创建或读取 `plan/`。

```powershell
powershell -ExecutionPolicy Bypass -File scripts/init_plan.ps1
```

```bash
bash scripts/init_plan.sh
```

### 第二步：产出 Markdown 正文

先产出可评审的 Markdown 版正文，再决定是否转成其他交付形态。正文写作统一受 `writing-core`、`common-gotchas` 和 `quality-review` 约束。

### 第三步：运行质量检查

```powershell
powershell -ExecutionPolicy Bypass -File scripts/quality_check.ps1 -FilePath report.md
```

```bash
bash scripts/quality_check.sh report.md
```

质量检查默认分级告警，内容问题不阻断流程，但会提示元叙事、后台词、占位符和结构类风险。

### 第四步：按需导出可审草稿

如果需要给领导或同事预审，可导出 `docx` 可审草稿：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/export_draft.ps1 -InputPath report.md -OutputDir output
```

```bash
bash scripts/export_draft.sh report.md output
```

导出产物只用于预审、流转和批注，不等于最终终排版。更详细的共享使用说明见 `docs/quickstart.md`。

## 推荐提问方式

最稳的方式不是一句「帮我写报告」，而是把任务边界一次说清。推荐至少包含：交付物、目标篇幅、截止时间、已有材料、希望先做什么。

高频入口可直接参考：

- 标准咨询报告：见 `docs/prompt-cookbook.md` 的「标准咨询报告」
- 形式交付 / 救火模式：见 `docs/prompt-cookbook.md` 的「形式交付 / 救火模式」
- 继续已有项目：见 `docs/prompt-cookbook.md` 的「继续已有项目」
- 质量审查：见 `docs/prompt-cookbook.md` 的「质量审查」
- 导出 `可审草稿`：见 `docs/prompt-cookbook.md` 的「可审草稿」

## 它和同类有什么不同？

| | 临时问 AI | 通用文档 skill（docx 等） | 本 Skill |
|---|---|---|---|
| 跨轮记住项目上下文 | ✗ | ✗ | ✅ `plan/` 状态机，可恢复 |
| 咨询写作规范 + So What | 看运气 | ✗ | ✅ 模块化、可路由 |
| 去 AI 味 | 删几个词 | ✗ | ✅ 语域感知 AI 痕迹清单 |
| 招投标技术标 | ✗ | ✗ | ✅ 评分点对标、点对点应答 |
| 交付前质检 | ✗ | 部分 | ✅ 分级告警脚本 |
| 自身可评测 / 契约护栏 | — | 不一 | ✅ 35 个契约测试 |

定位说明：方法论厚度上不和 management-consulting 这类「框架库」比框架数量，去 AI 味深度上参考并致敬 Humanizer-zh；本 Skill 的差异化是**把咨询项目当工程来管**——状态可恢复、改动有契约护栏、覆盖中文招投标技术标。

## 重要边界

1. Skill 默认主产物是 Markdown、纯文本和图表脚本，不直接承诺最终 `.docx` 成品。
2. Skill 可以按需导出 `可审草稿`，但这是 reviewable draft，`不承诺` 最终中文排版效果、公司模板适配、页眉页脚、自动目录、页码和图表版式全部一次到位。
3. Pandoc 导出解决的是「快速成稿」和「可传阅」，不是「最终交付终排」。
4. 数据与案例不会编造，引用需可追溯；高风险结论请人工二次核验。

## 模块地图

### 核心模块

| 场景 | 模块 |
|---|---|
| 通用报告写作 | `modules/writing-core.md` |
| 执行摘要提炼 | `modules/executive-summary.md` |
| 常见踩坑与去 AI 味 | `modules/common-gotchas.md` |
| 质量审查 | `modules/quality-review.md` |
| 最终交付与可审草稿 | `modules/final-delivery.md` |
| 咨询项目全流程 | `modules/consulting-lifecycle.md` |

### 业务场景模块

| 场景 | 模块 |
|---|---|
| 专项研究报告 | `modules/specialized-research.md` |
| 管理制度编写 | `modules/management-system.md` |
| 实施方案编写 | `modules/implementation-plan.md` |
| 战略咨询 | `modules/strategy-consulting.md` |
| 市场研究 | `modules/market-research.md` |
| 尽职调查 | `modules/due-diligence.md` |
| 招投标技术标 | `modules/technical-bid.md` |

### 工具模块

| 场景 | 模块 |
|---|---|
| 商业图表制作 | `modules/business-charts.md` |
| 战略框架图 | `modules/framework-diagrams.md` |
| 数据分析 | `modules/data-analysis.md` |
| 建议框架 | `modules/recommendation-framework.md` |
| 报告模板库 | `modules/templates-collection.md` |

模块命名、任务类别和行为标签的唯一事实源是 `evals/capability-map.json`。如果 README、SKILL、evals 和测试之间出现冲突，以 capability map 为准。

## 自动化 hooks（可选，需自行接入）

`.claude/hooks/` 下放的是**示例 hook 配置**，说明可以在项目里接入哪些自动化时机；是否生效、如何挂载取决于你的 runtime 与项目设置，默认不随 Skill 自动运行：

- `init-plan-on-create.yaml`：创建 `plan/` 后自动初始化模板
- `post-report-quality-check.yaml`：写入 `*.md` 后自动调用质量检查
- `confirm-overwrite.yaml`：覆盖现有报告前需要确认

把它们当成可复制的起点，按需接进你自己的项目自动化里。

## 自检与评测

### 运行自动化测试

```bash
python -m unittest discover -s tests -v
```

### 运行轻量 eval 校验

```bash
python scripts/run_evals.py
```

更细的自检说明见 `docs/self-check.md`。

## FAQ

### 为什么默认产物不是 Word 成品？

因为咨询协作更需要可追踪、可复用、可版本化的文本资产。Markdown 更适合过程迭代，Word 更适合最终交付，所以两者在流程中的角色不同。

### 可以直接让我生成「最终可提交版本」吗？

可以生成接近终稿的内容，也可以导出 `可审草稿`，但正式模板、页眉页脚、页码、图表微调、目录和中文排版细节仍建议人工在 Word 中完成。

### 这个 Skill 会不会瞎编数据？

不会。规则层面明确禁止编造数据与案例；引用要求可追溯。遇到高风险判断时，建议人工再核验一轮。

## 仓库结构

```text
consulting-report-skill/
├── SKILL.md
├── docs/                 # 共享使用说明（quickstart / prompt-cookbook / module-routing / self-check）
├── evals/                # capability-map.json（唯一事实源）+ evals.json
├── modules/              # writing-core / common-gotchas / quality-review / 专项模块……
├── scripts/              # init_plan / quality_check / export_draft / run_evals
├── plan-template/        # plan/ 初始化模板
├── .claude/hooks/        # 示例 hook 配置
└── tests/                # 契约测试三件套
```

## v1.4 更新

- **去 AI 味深化**：新增语域感知的「AI 痕迹清单」（内容 / 语言语法 / 格式 / 语气四类 + 嗓音校准），参考并致敬开源 skill Humanizer-zh，按咨询场景改写，保留技术标「技术规范书」术语豁免。
- **店面升级**：补齐安装入口、跨 runtime 声明、去 AI 味 before/after 可见产物、同类对比表。
- **诚实化**：hooks 改为「示例配置、需自行接入」的真实表述；`docs/` 与 `.claude/` 不再被打包排除，README/SKILL 引用的文件随包发布。
- 沿用 v1.3 招投标技术标支持与项目过程模板，仍不把 Word 导出包装成最终中文排版。

## 版本

- 版本：1.4.0
- 创建日期：2026-03-17
- 最近更新：2026-07-01
- 维护目标：流程稳定、内容可追溯、评测可跑、边界不夸大、装得上看得见；覆盖招投标技术标

## 许可证

MIT License
