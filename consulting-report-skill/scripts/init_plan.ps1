# 咨询报告项目初始化脚本 (PowerShell)
# 用途：自动创建 plan 目录并复制模板文件

param()

Write-Host "🚀 开始初始化咨询报告项目..." -ForegroundColor Green

# 检查是否在正确的目录
if (-not (Test-Path "consulting-report-skill/SKILL.md")) {
    Write-Host "❌ 错误：请在项目根目录运行此脚本" -ForegroundColor Red
    exit 1
}

# 创建 plan 目录
if (Test-Path "plan") {
    $response = Read-Host "⚠️  plan 目录已存在，是否覆盖？(y/n)"
    if ($response -ne "y") {
        Write-Host "❌ 取消初始化" -ForegroundColor Yellow
        exit 0
    }
    Remove-Item -Recurse -Force plan
}

Write-Host "📁 创建 plan 目录..." -ForegroundColor Cyan
New-Item -ItemType Directory -Path "plan" | Out-Null

# 复制模板文件
Write-Host "📄 复制模板文件..." -ForegroundColor Cyan
Copy-Item "consulting-report-skill/plan-template/project-overview.md" "plan/"
Copy-Item "consulting-report-skill/plan-template/stage-gates.md" "plan/"
Copy-Item "consulting-report-skill/plan-template/progress.md" "plan/"
Copy-Item "consulting-report-skill/plan-template/research-plan.md" "plan/"
Copy-Item "consulting-report-skill/plan-template/notes.md" "plan/"

Write-Host "✅ 初始化完成！" -ForegroundColor Green
Write-Host ""
Write-Host "已创建以下文件："
Write-Host "  - plan/project-overview.md"
Write-Host "  - plan/stage-gates.md"
Write-Host "  - plan/progress.md"
Write-Host "  - plan/research-plan.md"
Write-Host "  - plan/notes.md"
Write-Host ""
Write-Host "💡 下一步：编辑 plan/project-overview.md 填写项目信息" -ForegroundColor Yellow
