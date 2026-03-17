# Consulting Report Skill - 项目说明

## 项目信息

**版本**: v1.0.0
**创建日期**: 2026-03-17
**项目路径**: `/home/cpilot/projects/consulting-report-skill/`

## 项目描述

咨询报告写作 Skill，支持战略咨询、市场研究、管理制度、实施方案等场景。

## 核心功能

- **15 个专项模块**: 战略、市场、专项研究、管理制度、实施方案、尽职调查等
- **门禁机制**: 先讨论再执行、plan 目录管理、篇幅确认
- **快速报告生成**: 模板化交付，支持形式交付场景
- **商业图表自动生成**: Python/Plotly
- **质量检查脚本**: 数据来源、图表编号、So What 测试

## 测试用例

29 个测试用例，覆盖 10 种场景：
- 战略咨询（4个）
- 市场研究（4个）
- 专项研究（3个）
- 管理制度（3个）
- 实施方案（3个）
- 尽职调查（3个）
- 执行摘要（2个）
- 商业图表（2个）
- 快速报告生成（4个）
- 综合场景（1个）

## 使用方法

### 触发词
```
"写咨询报告"、"战略分析"、"市场研究"、"管理制度"、"实施方案"
```

### 快速报告生成（形式交付）
```
"需要一份15页的XX行业背景报告，合同要求但客户不会细看"
```

## 目录结构

```
consulting-report-skill/
├── SKILL.md                    # 主入口文件
├── README.md                   # 详细文档
├── requirements.txt            # Python 依赖
├── modules/                    # 15 个核心模块
│   ├── writing-core.md
│   ├── consulting-lifecycle.md
│   ├── executive-summary.md
│   ├── business-charts.md
│   ├── templates-collection.md
│   ├── specialized-research.md
│   ├── management-system.md
│   ├── implementation-plan.md
│   ├── quality-review.md
│   ├── strategy-consulting.md
│   ├── market-research.md
│   ├── data-analysis.md
│   ├── framework-diagrams.md
│   ├── recommendation-framework.md
│   └── due-diligence.md
├── plan-template/              # 5 个 plan 模板
├── scripts/                    # 4 个脚本（init + quality_check）
└── evals/                      # 测试用例
    └── evals.json
```

## GitHub

仓库地址: 待推送

## 开发记录

### v1.0.0 (2026-03-17)
- ✅ 完成 15 个核心模块
- ✅ 创建 29 个测试用例
- ✅ 优化 description（14 个触发词，8 个使用示例）
- ✅ 添加快速报告生成功能（支持形式交付）
- ✅ 创建质量检查脚本
- ✅ 完成打包和文档
