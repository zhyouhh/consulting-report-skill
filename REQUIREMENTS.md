# 咨询报告写作 Skill 改造需求规格

## 1. 项目概述

将现有的学术论文写作 skill 改造为咨询报告写作 skill，保留其优秀的工程化协作流程设计，但调整为适配咨询行业的写作场景。

## 2. 核心差异分析

### 2.1 目标用户
- **原 skill**：本科生、研究生、早期科研人员
- **新 skill**：咨询顾问、商业分析师、战略规划人员、企业管理层

### 2.2 写作目标
- **原 skill**：通过同行评审、发表学术成果
- **新 skill**：支持商业决策、提供可执行建议、展示专业洞察

### 2.3 内容结构
- **原 skill**：摘要、引言、文献综述、方法、结果、讨论、结论
- **新 skill**：执行摘要、背景与目标、分析框架、发现与洞察、建议、实施路线图、附录

### 2.4 写作风格
- **原 skill**：客观、严谨、去AI化、避免主观表达
- **新 skill**：专业、直接、面向行动、可以有明确观点和建议

### 2.5 交付物
- **原 skill**：Markdown/LaTeX → Word，重视文本内容
- **新 skill**：Word/PPT/PDF，重视视觉呈现和数据可视化

## 3. 保留的核心设计

### 3.1 工程化流程
- plan/ 目录管理项目上下文
- 先讨论再执行的门禁机制
- 任务入档与进度追踪
- 模块化设计

### 3.2 质量控制
- 去AI化语言规范（调整为咨询场景）
- 输出排版规范
- 三轮质量检查机制

### 3.3 环境支持
- Python 环境配置（用于数据分析和图表）
- 脚本自动化

## 4. 需要改造的模块

### 4.1 核心模块重构

| 原模块 | 新模块 | 改造重点 |
|--------|--------|----------|
| workflow-lifecycle.md | consulting-lifecycle.md | 咨询项目生命周期（启动→研究→分析→报告→演示→交付） |
| writing-core.md | writing-core.md | 咨询写作规范（保留去AI化，调整语气和结构） |
| writing-humanities.md | industry-analysis.md | 行业分析报告写作 |
| writing-medical.md | strategy-consulting.md | 战略咨询报告写作 |
| writing-law.md | compliance-advisory.md | 合规与风险咨询报告 |
| literature-review.md | market-research.md | 市场研究与竞争分析 |
| peer-review.md | quality-review.md | 报告质量审查 |
| statistical-analysis.md | data-analysis.md | 商业数据分析 |
| figures-python.md | business-charts.md | 商业图表制作 |
| figures-diagram.md | framework-diagrams.md | 战略框架与流程图 |
| prompts-collection.md | templates-collection.md | 咨询报告模板库 |

### 4.2 新增模块

| 新模块 | 功能 |
|--------|------|
| executive-summary.md | 执行摘要写作指南 |
| powerpoint-design.md | PPT 演示文稿设计 |
| financial-modeling.md | 财务建模与分析 |
| recommendation-framework.md | 建议框架与优先级排序 |
| stakeholder-communication.md | 利益相关方沟通 |

### 4.3 删除模块

- latex-guide.md（咨询报告不常用 LaTeX）
- environment-setup.md（简化为数据分析环境配置）

## 5. 生命周期阶段重新设计

### 5.1 咨询项目阶段（替代学术论文阶段）

| 阶段 | 目标 | 交付物 |
|------|------|--------|
| S0 项目启动 | 明确客户需求、范围、时间线 | project-overview.md |
| S1 研究设计 | 确定研究方法、数据来源、分析框架 | research-plan.md |
| S2 数据收集 | 收集一手/二手数据、访谈、调研 | data-log.md |
| S3 分析与洞察 | 数据分析、模式识别、关键发现 | analysis-notes.md |
| S4 报告撰写 | 结构化报告、图表制作 | report-draft/ |
| S5 质量审查 | 内部审查、事实核查、逻辑验证 | review-checklist.md |
| S6 演示准备 | PPT 制作、演讲稿、Q&A 准备 | presentation/ |
| S7 交付与跟进 | 最终交付、客户反馈、后续支持 | delivery-log.md |

## 6. 写作风格调整

### 6.1 保留的规范
- 段落之间空一行
- 避免无意义加粗
- 正文少列表（但咨询报告可适当放宽）
- 禁用机械过渡词

### 6.2 调整的规范
- **允许明确观点**：可以使用"我们认为"、"建议"、"应当"等表达
- **面向行动**：强调可执行性和优先级
- **数据驱动**：用数据和案例支撑观点
- **视觉优先**：重视图表、框架图、信息图

### 6.3 新增规范
- **执行摘要优先**：1-2 页核心发现和建议
- **金字塔原理**：结论先行，逐层展开
- **MECE 原则**：分类互斥且完全穷尽
- **So What 测试**：每个发现都要回答"所以呢？"

## 7. 模板与框架

### 7.1 报告结构模板
- 战略咨询报告模板
- 市场研究报告模板
- 尽职调查报告模板
- 运营优化报告模板

### 7.2 分析框架
- SWOT 分析
- Porter 五力模型
- PEST 分析
- 价值链分析
- BCG 矩阵
- McKinsey 7S 模型

### 7.3 图表类型
- 瀑布图（财务分析）
- 桑基图（流程分析）
- 热力图（优先级矩阵）
- 漏斗图（转化分析）
- 甘特图（实施计划）

## 8. 技术栈

### 8.1 保留
- Python（数据分析）
- Matplotlib/Seaborn（基础图表）
- Markdown（草稿）

### 8.2 新增
- Plotly（交互式图表）
- pandas（数据处理）
- PowerPoint 生成（python-pptx）

## 9. 交付要求

### 9.1 最小可用版本（MVP）
- 核心 SKILL.md 文件
- 5 个核心模块（lifecycle, writing-core, business-charts, templates, quality-review）
- 2 个报告模板
- 基础脚本（init_plan, quality_check）

### 9.2 完整版本
- 所有 11 个模块
- 5 个报告模板
- 3 个分析框架模板
- 完整的图表库
- PPT 生成支持

## 10. 成功标准

1. 能够支持完整的咨询项目生命周期
2. 输出符合咨询行业标准的报告结构
3. 提供可复用的分析框架和模板
4. 保持原 skill 的工程化流程优势
5. 生成的报告专业、清晰、面向行动
