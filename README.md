# 咨询报告写作助手 (Consulting Report Assistant)

> 将咨询报告写作从一次性对话，升级为可追踪、可恢复、可复用、可评测的工程化协作流程。

这个 Skill 面向咨询顾问、商业分析师、战略规划人员，也适合短周期救火式的形式交付场景。它的定位不是“帮你凑字数”，而是把咨询项目里的对齐、写作、质检、导出和回写做成一个稳定可复用的工作流。

## v1.2 完善版

这一版同时补强四条线：

- 评测可跑：新增 capability map 和轻量 eval runner，避免模块名和路由口径继续漂移
- 共享可用：补齐快速开始、推荐 prompt、模块路由和自检说明
- 护栏更稳：README、SKILL、evals、测试统一引用 capability map 中的模块、类别和行为标签
- 边界更清楚：继续坚持 `可审草稿` 能力，不把 Word 导出包装成最终中文排版

## 项目定位

这不是一个只会润色句子的提示词包，而是一套完整的咨询报告协作系统。它会先对齐目标与约束，再接管 `plan/` 项目上下文，然后按任务类型路由到对应模块执行。

如果你在做战略咨询、市场研究、专项研究、管理制度、实施方案或尽职调查，这个 Skill 会比普通对话式写作工具更稳定，因为它强调流程、记录、回写和交付前护栏。

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

先让 Skill 产出可评审的 Markdown 版正文，再决定是否转成其他交付形态。正文写作统一受 `writing-core`、`common-gotchas` 和 `quality-review` 约束。

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

导出产物只用于预审、流转和批注，不等于最终终排版。

更详细的共享使用说明见 `docs/quickstart.md`。

## 推荐提问方式

最稳的方式不是一句“帮我写报告”，而是把任务边界一次说清。推荐至少包含：交付物、目标篇幅、截止时间、已有材料、希望先做什么。

高频入口可直接参考：

- 标准咨询报告：见 `docs/prompt-cookbook.md` 的“标准咨询报告”
- 形式交付 / 救火模式：见 `docs/prompt-cookbook.md` 的“形式交付 / 救火模式”
- 继续已有项目：见 `docs/prompt-cookbook.md` 的“继续已有项目”
- 质量审查：见 `docs/prompt-cookbook.md` 的“质量审查”
- 导出 `可审草稿`：见 `docs/prompt-cookbook.md` 的“可审草稿”

## 重要边界

1. Skill 默认主产物是 Markdown、纯文本和图表脚本，不直接承诺最终 `.docx` 成品。
2. Skill 可以按需导出 `可审草稿`，但这是 reviewable draft，`不承诺` 最终中文排版效果、公司模板适配、页眉页脚、自动目录、页码和图表版式全部一次到位。
3. Pandoc 导出解决的是“快速成稿”和“可传阅”，不是“最终交付终排”。
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

### 工具模块

| 场景 | 模块 |
|---|---|
| 商业图表制作 | `modules/business-charts.md` |
| 战略框架图 | `modules/framework-diagrams.md` |
| 数据分析 | `modules/data-analysis.md` |
| 建议框架 | `modules/recommendation-framework.md` |
| 报告模板库 | `modules/templates-collection.md` |

模块命名、任务类别和行为标签的唯一事实源是 `evals/capability-map.json`。如果 README、SKILL、evals 和测试之间出现冲突，以 capability map 为准。

## 自检与评测

### 运行自动化测试

```bash
python -m unittest discover -s tests -v
```

### 运行轻量 eval 校验

```bash
python scripts/run_evals.py
```

### 检查 hooks 和质量脚本联动

- `init-plan-on-create.yaml`：创建 `plan/` 后自动初始化模板
- `post-report-quality-check.yaml`：写入 `*.md` 后自动调用质量检查
- `confirm-overwrite.yaml`：覆盖现有报告前需要确认

更细的自检说明见 `docs/self-check.md`。

## FAQ

### 为什么默认产物不是 Word 成品？

因为咨询协作更需要可追踪、可复用、可版本化的文本资产。Markdown 更适合过程迭代，Word 更适合最终交付，所以两者在流程中的角色不同。

### 可以直接让我生成“最终可提交版本”吗？

可以生成接近终稿的内容，也可以导出 `可审草稿`，但正式模板、页眉页脚、页码、图表微调、目录和中文排版细节仍建议人工在 Word 中完成。

### 这个 Skill 会不会瞎编数据？

不会。规则层面明确禁止编造数据与案例；引用要求可追溯。遇到高风险判断时，建议人工再核验一轮。

## 仓库结构

```text
consulting-report-skill/
├── SKILL.md
├── docs/
│   ├── quickstart.md
│   ├── prompt-cookbook.md
│   ├── module-routing.md
│   └── self-check.md
├── evals/
│   ├── capability-map.json
│   └── evals.json
├── modules/
│   ├── writing-core.md
│   ├── common-gotchas.md
│   ├── quality-review.md
│   ├── final-delivery.md
│   └── ...
├── scripts/
│   ├── run_evals.py
│   ├── quality_check.ps1
│   ├── export_draft.ps1
│   └── ...
└── tests/
```

## 版本

- 版本：1.2.0
- 创建日期：2026-03-17
- 最近更新：2026-03-26
- 维护目标：流程稳定、内容可追溯、评测可跑、边界不夸大

## 许可证

MIT License
