# 自检与评测

## 1. 运行自动化测试

```bash
python -m unittest discover -s tests -v
```

这一步覆盖脚本行为、双脚本平价、公开文档契约、eval schema、轻量 runner 和去 AI 味基准。

## 2. 运行轻量 eval 校验

```bash
python scripts/run_evals.py
```

它会检查：

- `evals/evals.json` 是否符合 schema
- `evals/capability-map.json` 是否引用真实模块
- eval 里的模块和行为标签是否合法
- `disallowed_signals` 是否在公开护栏或质量规则中有对应约束

## 3. 运行去 AI 味基准

```bash
python scripts/benchmark_anti_ai.py            # 配对语料 baseline vs cleaned 跑分
python scripts/benchmark_anti_ai.py report.md  # 给单个稿子打洁净度分
```

这是确定性的 AI 痕迹洁净度评分（脚本可机检项，非 LLM 主观质量分），既用于量化展示，也是回归护栏。

## 4. 检查 hooks（示例配置，不会自动运行）

`.claude/hooks/` 下的 YAML 用的是说明性 schema，**任何 runtime 都不会自动加载执行**——Agent Skill 标准不含「随 skill 自动生效的 hook」机制。它们只标注「可以在哪些时机接入自动化」，要真用得自己翻进所在 runtime 的 hook 机制（如 Claude Code 写进 `settings.json` 的 `PostToolUse`）。自检时确认示例与脚本路径仍一致：

- `.claude/hooks/init-plan-on-create.yaml`（示例：创建 `plan/` 后初始化模板）
- `.claude/hooks/post-report-quality-check.yaml`（示例：写入 `*.md` 后跑质量检查）
- `.claude/hooks/confirm-overwrite.yaml`（示例：覆盖现有报告前确认）

## 5. 导出前抽查

在执行 `scripts/export_draft.ps1` 或 `scripts/export_draft.sh` 前，先确认：

- 高风险占位符已清理
- 元叙事和后台词已处理
- 当前版本确实只是 `可审草稿`，不是最终终排版
