# CLAUDE.md — consulting-report-skill

咨询报告写作助手 Skill（中文），面向咨询顾问 / 分析师，提供 plan 追踪、咨询式写作、去 AI 味、稳定模块路由、可审草稿导出。

这份文件是**维护本仓库的开发约定**（受众：改这个 skill 的 AI / 人）。注意区分受众：`SKILL.md` 是 skill 被调用时的运行指令，`README.md` 是使用者向导，本文件是开发者约定，三者不互抄。

## 命令

- 跑全部测试：`python -m unittest discover -s tests -v`
- 轻量 eval 校验：`python scripts/run_evals.py`
- 去 AI 味洁净度基准：`python scripts/benchmark_anti_ai.py`（配对语料）或 `... report.md`（单文件）
- 初始化 plan：`bash scripts/init_plan.sh` 或 `powershell -ExecutionPolicy Bypass -File scripts/init_plan.ps1`
- 质量检查：`bash scripts/quality_check.sh report.md` 或 `...quality_check.ps1 -FilePath report.md`
- 导出可审草稿：`bash scripts/export_draft.sh report.md output`（需 pandoc）
- 无密钥 / token，不涉及外部凭据。

## 唯一事实源与契约测试

- `evals/capability-map.json` 是**模块名、task_types、behavior_tags 的唯一事实源**。README / SKILL / docs / evals 与它冲突时以它为准。
- 契约测试，改任何东西都要先跑过：
  - `tests/test_docs_contract.py` — README/SKILL 版本号、docs 必含片段、quality-review 结构敏感项。
  - `tests/test_evals_contract.py` — capability-map 与 evals.json 的 schema、module/behavior/category 合法性、类别覆盖量。
  - `tests/test_scripts.py` — 两平台脚本行为 + `EXPECTED_PLAN_FILES` + 去 AI 味检测器双脚本平价。
  - `tests/test_benchmark.py` — 去 AI 味洁净度评分器：clean>problematic、cleaned 语料显著高于 baseline、技术标术语豁免。

## 改动接入清单（红线：少同步一处，契约测试就挂）

- **加报告类型 / module**：同步 `capability-map.json`（task_types + capability 条目）+ `SKILL.md`（专项模块行 + description 触发词）+ `docs/module-routing.md` + `docs/prompt-cookbook.md` + `evals/evals.json`（≥3 用例）+ `README.md` 模块表。
- **版本 bump**：`SKILL.md` + `README.md` 版本段 + `tests/test_docs_contract.py` 的版本断言（2 处「版本：x.y.z」+ README「vX.Y」标题断言）。
- **加 plan-template 模板**：`scripts/init_plan.ps1` 和 `scripts/init_plan.sh` 的 managed list + 完成提示 + `tests/test_scripts.py` 的 `EXPECTED_PLAN_FILES`，三处必须一致。init_plan 语义：选 `n` = 保留已有 + 仅补缺失；`y` / `--force` 才覆盖已存在文件。
- **跨平台脚本对**：`scripts/*.ps1` 与 `scripts/*.sh` 必须语义一致，两边一起改。
- **改 quality_check 检测器 / 去 AI 味规则**：`scripts/quality_check.sh` 与 `.ps1` 同步改（语义一致），并对齐 `scripts/benchmark_anti_ai.py` 的检测项；emoji 一律走 `scripts/count_emoji.py`（唯一实现，别在 shell 里写 `grep -P`，不可移植）。改完跑 `tests/test_scripts.py`（双脚本平价 fixture `ai-traces-report.md`）+ `tests/test_benchmark.py`（锁 README 登的 28.7→99.0）。

## 已知陷阱

- 后台词「技术规范书 / 技规」在**自由报告**里是后台泄漏、要禁；在**技术标**里是招标文件正式术语、必须保留。`quality_check` 有技术标模式（正文含「技术评分索引表 / 技术规范书点对点应答」或一级标题「技术标（技术投标文件）」时，对这条后台词豁免）；文档护栏（`writing-core` / `SKILL` / `quality-review` / `common-gotchas`）已写明例外。改后台词清单时别漏掉这条例外。
- emoji 检测集中在 `scripts/count_emoji.py`（shell `grep -P` 仅 GNU 可用、macOS BSD 会静默跳过，破坏双脚本平价）。两个 `quality_check` 与 `benchmark` 都引用它，改 emoji 规则只动这一处。
- 三段式（首先/其次/最后）在技术标里是评分点列项、不算痕迹：`quality_check`（`IS_BID`/`$isBid`）和 `benchmark`（`is_bid`）都对技术标跳过三段式，与技术规范书豁免同源。改三段式逻辑时两处都要顾。
- hooks 是**示例**：`.claude/hooks/*.yaml` 用自创 schema，任何 runtime 都不自动加载（Agent Skill 标准不含自动 hook 机制）。`README` / `docs/self-check.md` 已据实写明，别再改回「自动触发」表述。

## 与 CRA 的关系

`consulting-report-agent`（CRA）内嵌的 `skill/` 是本 skill 的 app 化分叉版。新能力常先出现在 CRA，需反哺回本仓库，方向恒为 CRA → skill，且必须**去 app 化**（剔除后端工具名、按钮交互、system-prompt 注入、后端阶段流）。详见 agent memory `cra-skill-relationship`。
