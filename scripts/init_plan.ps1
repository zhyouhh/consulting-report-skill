# 咨询报告项目初始化脚本 (PowerShell)
# 用途：在当前工作目录下创建/补齐 plan 目录，并从仓库模板复制项目管理文件

param(
    [switch]$Force
)

$ErrorActionPreference = "Stop"

$templateDir = Join-Path $PSScriptRoot "..\plan-template"
$templateDir = (Resolve-Path -LiteralPath $templateDir).Path
$planPath = Join-Path (Get-Location).Path "plan"
$managedFiles = @(
    "project-overview.md",
    "stage-gates.md",
    "progress.md",
    "research-plan.md",
    "notes.md"
)

Write-Host "🚀 开始初始化咨询报告项目..." -ForegroundColor Green

if (-not (Test-Path -LiteralPath $templateDir)) {
    Write-Error "模板目录不存在: $templateDir"
    exit 1
}

if (-not (Test-Path -LiteralPath $planPath)) {
    Write-Host "📁 创建 plan 目录..." -ForegroundColor Cyan
    New-Item -ItemType Directory -Path $planPath | Out-Null
    $overwriteManagedFiles = $false
}
else {
    $existingManagedFiles = @(
        $managedFiles | Where-Object {
            Test-Path -LiteralPath (Join-Path $planPath $_)
        }
    )

    if ($existingManagedFiles.Count -eq 0) {
        Write-Host "📁 检测到已有 plan 目录，将补齐模板文件..." -ForegroundColor Cyan
        $overwriteManagedFiles = $false
    }
    elseif ($Force) {
        Write-Host "📁 plan 目录已存在，按 Force 模式覆盖模板文件..." -ForegroundColor Cyan
        $overwriteManagedFiles = $true
    }
    else {
        $response = Read-Host "⚠️  plan 目录已存在且包含模板文件，是否覆盖这些模板文件？(y/n)"
        if ($response -ne "y") {
            Write-Host "❌ 取消初始化" -ForegroundColor Yellow
            exit 0
        }
        $overwriteManagedFiles = $true
    }
}

Write-Host "📄 复制模板文件..." -ForegroundColor Cyan
foreach ($fileName in $managedFiles) {
    $sourcePath = Join-Path $templateDir $fileName
    $targetPath = Join-Path $planPath $fileName
    if ($overwriteManagedFiles -or -not (Test-Path -LiteralPath $targetPath)) {
        Copy-Item -LiteralPath $sourcePath -Destination $targetPath -Force
    }
}

Write-Host "✅ 初始化完成！" -ForegroundColor Green
Write-Host ""
Write-Host "已确保以下文件存在："
Write-Host "  - plan/project-overview.md"
Write-Host "  - plan/stage-gates.md"
Write-Host "  - plan/progress.md"
Write-Host "  - plan/research-plan.md"
Write-Host "  - plan/notes.md"
Write-Host ""
Write-Host "💡 下一步：编辑 plan/project-overview.md 填写项目信息" -ForegroundColor Yellow
