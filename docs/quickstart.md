# 快速开始

这份 Quickstart 面向第一次共享使用这套 Skill 的人，目标是用最短路径跑通一次完整闭环：初始化 `plan/`、产出正文、运行质量检查、按需导出 `可审草稿`。

## 1. 先把任务边界说清楚

建议一次说清五件事：

- 交付物是什么
- 目标篇幅是多少
- 截止时间是什么
- 已有材料有哪些
- 希望先做大纲、正文还是质量检查

## 2. 初始化项目上下文

Windows PowerShell：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/init_plan.ps1
```

macOS / Linux：

```bash
bash scripts/init_plan.sh
```

## 3. 先产出 Markdown 正文

默认先产出 Markdown，不急着一开始就追 Word 成品。正文阶段统一受 `writing-core`、`common-gotchas` 和 `quality-review` 约束。

## 4. 跑质量检查

Windows PowerShell：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/quality_check.ps1 -FilePath report.md
```

macOS / Linux：

```bash
bash scripts/quality_check.sh report.md
```

## 5. 按需导出可审草稿

只有在需要流转、批注或预审时，才导出 `docx` 版本。

Windows PowerShell：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/export_draft.ps1 -InputPath report.md -OutputDir output
```

macOS / Linux：

```bash
bash scripts/export_draft.sh report.md output
```

## 6. 记住边界

- `scripts/init_plan` 负责初始化，不负责写正文
- `scripts/quality_check` 负责告警，不默认阻断流程
- `scripts/export_draft` 产出的是 `可审草稿`，不是最终终排版
