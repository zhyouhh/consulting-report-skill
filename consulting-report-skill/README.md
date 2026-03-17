# 咨询报告写作助手 (Consulting Report Assistant)

> 📊 将咨询报告写作从一次性对话，升级为可追踪、可恢复、可复用的工程化协作流程。

这个 Skill 面向咨询顾问、商业分析师、战略规划人员，目标很直接：提高报告质量，减少返工，把时间花在真正有价值的分析和洞察上。

## 项目定位

这不是一个"只会润色句子"的提示词包，而是一套完整的咨询报告协作系统。它会在任务开始前先对齐目标与约束，自动接管 `plan/` 项目上下文，再按报告类型路由到对应模块执行。

如果你在做战略咨询、市场研究、尽职调查或运营优化项目，这个 Skill 会比普通对话式写作工具更稳定，因为它强调流程、记录和回写，不依赖单轮记忆。

## 核心能力

- **全流程协作**：从项目启动、研究设计、数据收集到报告撰写、质量审查、演示准备，按阶段门禁执行
- **专业化写作**：保留去AI化规范，同时支持明确观点和建议，符合咨询行业写作风格
- **商业分析框架**：内置 SWOT、Porter 五力、PEST、价值链等常用分析框架
- **商业图表生成**：支持瀑布图、热力图、漏斗图、甘特图、桑基图等专业图表
- **模板库**：提供战略咨询、市场研究、尽职调查、运营优化等报告模板
- **计划可恢复**：`plan/` 持续记录目标、产出、决策和下一步动作

## 当前版本（v1.0.0 完整版）

**已实现功能** ✅：
- 咨询写作核心规范（金字塔原理、MECE、So What 测试）
- 咨询项目生命周期管理（8 个阶段）
- 执行摘要写作指南
- 商业图表生成（瀑布图、热力图、漏斗图、甘特图）
- 报告模板库（战略咨询、市场研究、尽职调查、运营优化）
- 专项研究报告（数据管理、流程优化、技术选型等）
- 管理制度编写
- 实施方案编写
- 质量审查体系
- 战略咨询专项
- 市场研究专项
- 数据分析
- 战略框架图
- 建议框架
- 尽职调查

## 适用平台

本 Skill 采用目录化设计，适用于主流本地技能加载工作流，当前适配以下平台：

- Cursor
- Windsurf
- Antigravity
- Qoder
- CC
- OpenCode

## 你会得到什么产物

默认情况下，Skill 产物是项目内文件，不是 Word 成品文件。

| 产物类型 | 默认格式 | 说明 |
|---|---|---|
| 报告正文 | `.md` / 纯文本 | 便于版本管理和后续再加工 |
| 过程记录 | `plan/*.md` | 包含目标、进度、阶段门禁、决策 |
| 图表脚本 | `.py` | 可复现图表生成逻辑 |
| 分析框架 | `.md` | 可复用的 SWOT、Porter 等框架 |

## 重要边界（务必先看）

1. Skill 默认不会自动生成或直接写入 `.docx`
2. Skill 默认不会替你"打开 Word 并排版"，需要你手动复制或用工具转换
3. Skill 可以生成适合粘贴进 Word 的纯文本段落，但最终样式需要你在 Word 端处理
4. 数据与案例不会编造，引用需可追溯；高风险结论请你二次核验

## 安装

下载仓库，解压后把 `consulting-report-skill/` 复制到你的项目目录就可以用了。

推荐步骤：

1. 下载本仓库压缩包并解压
2. 把 `consulting-report-skill/` 文件夹复制到你的咨询项目目录
3. 在你使用的平台中加载该本地 Skill 目录（或复制到平台要求的 skills 目录）

## 环境配置（可选）

如果需要使用商业图表生成功能，需要安装 Python 依赖：

```bash
# 安装依赖
pip install -r consulting-report-skill/requirements.txt

# 或手动安装
pip install pandas plotly matplotlib seaborn
```

**环境要求**：
- Python 3.8+
- pandas >= 2.0.0
- plotly >= 5.18.0

如果不使用图表生成功能，可以跳过此步骤。

## 标准协作流程（推荐）

1. 明确本轮任务目标、输出物、截止时间
2. 让 Skill 创建或读取 `plan/`
3. 让 Skill 先产出可审阅的 Markdown 正文
4. 运行质量检查脚本，处理去AI化与排版问题
5. 确认数据、分析、建议后再做终稿整理
6. 手动迁移到 Word/PPT 并完成最终排版

## 如何把 Markdown 交付到 Word

### 方案 A：手动复制（默认推荐）

1. 让 Skill 输出"纯文本段落版"正文（避免 Markdown 标记）
2. 在编辑器中复制正文并粘贴到 Word
3. 在 Word 中应用公司模板样式（标题、正文、图注）
4. 手动检查图表、数据来源、建议优先级

### 方案 B：Pandoc 转换（可选）

如果你本地已安装 Pandoc，可尝试：

```bash
pandoc report.md -o report.docx
```

说明：这只解决格式转换，不替代公司模板排版和最终人工校对。

## 常用脚本

- 初始化计划目录  
  macOS/Linux: `bash consulting-report-skill/scripts/init_plan.sh`  
  Windows PowerShell: `powershell -ExecutionPolicy Bypass -File consulting-report-skill/scripts/init_plan.ps1`

- 报告质量检查  
  macOS/Linux: `bash consulting-report-skill/scripts/quality_check.sh <文件.md>`  
  Windows PowerShell: `powershell -ExecutionPolicy Bypass -File consulting-report-skill/scripts/quality_check.ps1 -FilePath <文件.md>`

## 模块地图

### 核心模块
| 场景 | 模块 |
|---|---|
| 咨询项目全流程 | `modules/consulting-lifecycle.md` |
| 通用报告写作 | `modules/writing-core.md` |
| 执行摘要写作 | `modules/executive-summary.md` |
| 质量审查 | `modules/quality-review.md` |

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

## FAQ

### 为什么默认产物不是 Word？

因为咨询协作更需要可追踪、可复用、可版本化的文本资产，Markdown 更适合过程迭代。Word 适合最终交付，所以放在最后一步处理更稳妥。

### 可以直接让我"生成最终可提交版本"吗？

可以做接近终稿的内容，但公司模板、页码、图表编号、格式细节仍建议在 Word 端完成。

### 这个 Skill 会不会瞎编数据？

不会。规则层面明确禁止编造数据与案例；引用要求可追溯。

## 仓库结构

```text
consulting-report-skill/
├── SKILL.md
├── modules/
│   ├── writing-core.md
│   ├── consulting-lifecycle.md
│   ├── executive-summary.md
│   ├── business-charts.md
│   └── templates-collection.md
├── plan-template/
│   ├── project-overview.md
│   ├── stage-gates.md
│   ├── progress.md
│   ├── research-plan.md
│   └── notes.md
├── scripts/
│   ├── init_plan.sh
│   ├── init_plan.ps1
│   ├── quality_check.sh
│   └── quality_check.ps1
└── README.md
```

## 版本

- 版本：1.0.0
- 创建日期：2026-03-17
- 维护目标：流程稳定、内容可追溯、产物可交付

## 许可证

MIT License
