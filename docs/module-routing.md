# 模块路由指南

## 通用主流程

默认从 `consulting-lifecycle`、`writing-core`、`common-gotchas`、`quality-review` 这几类通用模块起步，再按任务类型叠加专项模块。

## 典型路由

| 任务类型 | 推荐模块组合 |
|---|---|
| 战略研究 / 战略咨询 | `strategy-consulting` + `market-research` + `recommendation-framework` |
| 执行摘要 | `executive-summary` + `quality-review` |
| 专项研究 | `specialized-research` + `data-analysis` + `quality-review` |
| 管理制度 | `management-system` + `writing-core` + `quality-review` |
| 实施方案 | `implementation-plan` + `recommendation-framework` + `quality-review` |
| 可审草稿导出 | `quality-review` + `final-delivery` |
| 只做质量审查 | `quality-review` + `common-gotchas` |

## 路由提示

- 当用户提“竞争战略、市场进入、增长策略”时，优先看 `strategy-consulting`
- 当用户提“市场规模、行业趋势、竞争格局”时，优先看 `market-research`
- 当用户提“执行摘要、管理层摘要、summary”时，优先看 `executive-summary`
- 当用户直接说“review、审一下、质检一下”时，优先走 `quality-review`

## 常见误用

- 不要脑补仓库里不存在的模块名
- 不要把 `quality-review` 当成只在最后才用的模块，它也适合阶段性复核
- 不要把 `final-delivery` 理解成最终终排版，它只负责 `可审草稿`
