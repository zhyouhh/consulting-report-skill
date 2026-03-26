# 自检与评测

## 1. 运行自动化测试

```bash
python -m unittest discover -s tests -v
```

这一步覆盖脚本行为、公开文档契约、eval schema 和轻量 runner。

## 2. 运行轻量 eval 校验

```bash
python scripts/run_evals.py
```

它会检查：

- `evals/evals.json` 是否符合 schema
- `evals/capability-map.json` 是否引用真实模块
- eval 里的模块和行为标签是否合法
- `disallowed_signals` 是否在公开护栏或质量规则中有对应约束

## 3. 检查 hooks

重点看以下 hook 是否仍与文档描述一致：

- `.claude/hooks/init-plan-on-create.yaml`
- `.claude/hooks/post-report-quality-check.yaml`
- `.claude/hooks/confirm-overwrite.yaml`

其中 `post-report-quality-check.yaml` 会在写入 `*.md` 时自动触发质量检查。

## 4. 导出前抽查

在执行 `scripts/export_draft.ps1` 或 `scripts/export_draft.sh` 前，先确认：

- 高风险占位符已清理
- 元叙事和后台词已处理
- 当前版本确实只是 `可审草稿`，不是最终终排版
