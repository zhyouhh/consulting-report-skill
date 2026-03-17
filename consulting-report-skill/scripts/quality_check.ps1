# 咨询报告质量检查脚本 (PowerShell)
# 用途：自动检测报告中的常见问题

param(
    [Parameter(Mandatory=$true)]
    [string]$FilePath
)

if (-not (Test-Path $FilePath)) {
    Write-Host "❌ 文件不存在: $FilePath" -ForegroundColor Red
    exit 1
}

Write-Host "🔍 开始检查报告质量: $FilePath" -ForegroundColor Green
Write-Host ""

$content = Get-Content $FilePath -Encoding UTF8

# 检查机械过渡词
Write-Host "📝 检查机械过渡词..." -ForegroundColor Cyan
$transitions = Select-String -Path $FilePath -Pattern "(首先|其次|最后|此外|另外|接下来)" -AllMatches
if ($transitions) {
    Write-Host "⚠️  发现机械过渡词：" -ForegroundColor Yellow
    $transitions | ForEach-Object { Write-Host "  行 $($_.LineNumber): $($_.Line)" }
} else {
    Write-Host "✅ 未发现机械过渡词" -ForegroundColor Green
}
Write-Host ""

# 检查空洞强调句
Write-Host "📝 检查空洞强调句..." -ForegroundColor Cyan
$emphasis = Select-String -Path $FilePath -Pattern "(值得注意的是|需要指出的是|重要的是|必须强调的是)" -AllMatches
if ($emphasis) {
    Write-Host "⚠️  发现空洞强调句：" -ForegroundColor Yellow
    $emphasis | ForEach-Object { Write-Host "  行 $($_.LineNumber): $($_.Line)" }
} else {
    Write-Host "✅ 未发现空洞强调句" -ForegroundColor Green
}
Write-Host ""

# 检查空洞形容词
Write-Host "📝 检查空洞形容词..." -ForegroundColor Cyan
$adjectives = Select-String -Path $FilePath -Pattern "(非常|极其|十分|相当)" -AllMatches
if ($adjectives) {
    Write-Host "⚠️  发现空洞形容词（建议用具体数据替代）：" -ForegroundColor Yellow
    $adjectives | ForEach-Object { Write-Host "  行 $($_.LineNumber): $($_.Line)" }
} else {
    Write-Host "✅ 未发现空洞形容词" -ForegroundColor Green
}
Write-Host ""

# 检查段落格式
Write-Host "📝 检查段落格式..." -ForegroundColor Cyan
$emptyLines = ($content | Where-Object { $_ -eq "" }).Count
$totalLines = $content.Count
Write-Host "   空行数: $emptyLines / 总行数: $totalLines"
Write-Host ""

# 检查数据来源标注
Write-Host "📝 检查数据来源标注..." -ForegroundColor Cyan
$sources = Select-String -Path $FilePath -Pattern "(根据|来源：|数据来源)" -AllMatches
if ($sources) {
    Write-Host "✅ 发现数据来源标注：" -ForegroundColor Green
    $sources | ForEach-Object { Write-Host "  行 $($_.LineNumber): $($_.Line)" }
} else {
    Write-Host "⚠️  未发现数据来源标注（建议标注数据来源）" -ForegroundColor Yellow
}
Write-Host ""

# 检查图表编号连续性
Write-Host "📝 检查图表编号连续性..." -ForegroundColor Cyan
$figureMatches = Select-String -Path $FilePath -Pattern "图(\d+)" -AllMatches
if ($figureMatches) {
    $figureNums = $figureMatches | ForEach-Object { $_.Matches.Groups[1].Value } | Sort-Object {[int]$_}
    $prev = 0
    $gapFound = $false
    foreach ($num in $figureNums) {
        $numInt = [int]$num
        if ($prev -ne 0 -and ($numInt - $prev) -gt 1) {
            Write-Host "❌ 图编号不连续：图$prev -> 图$numInt" -ForegroundColor Red
            $gapFound = $true
        }
        $prev = $numInt
    }
    if (-not $gapFound) {
        Write-Host "✅ 图编号连续" -ForegroundColor Green
    }
} else {
    Write-Host "   未发现图编号"
}
Write-Host ""

# 检查表格编号连续性
Write-Host "📝 检查表格编号连续性..." -ForegroundColor Cyan
$tableMatches = Select-String -Path $FilePath -Pattern "表(\d+)" -AllMatches
if ($tableMatches) {
    $tableNums = $tableMatches | ForEach-Object { $_.Matches.Groups[1].Value } | Sort-Object {[int]$_}
    $prev = 0
    $gapFound = $false
    foreach ($num in $tableNums) {
        $numInt = [int]$num
        if ($prev -ne 0 -and ($numInt - $prev) -gt 1) {
            Write-Host "❌ 表编号不连续：表$prev -> 表$numInt" -ForegroundColor Red
            $gapFound = $true
        }
        $prev = $numInt
    }
    if (-not $gapFound) {
        Write-Host "✅ 表编号连续" -ForegroundColor Green
    }
} else {
    Write-Host "   未发现表格编号"
}
Write-Host ""

# 检查 So What（关键发现但缺少行动建议）
Write-Host "📝 检查 So What..." -ForegroundColor Cyan
$keyFindings = Select-String -Path $FilePath -Pattern "(发现|显示|表明|数据显示)" -AllMatches
if ($keyFindings) {
    $actionWords = (Select-String -Path $FilePath -Pattern "(建议|应当|需要|可以|应该)" -AllMatches).Count
    if ($actionWords -lt 3) {
        Write-Host "⚠️  发现关键发现但行动建议较少（建议回答 'So What'）" -ForegroundColor Yellow
    } else {
        Write-Host "✅ 包含行动建议" -ForegroundColor Green
    }
} else {
    Write-Host "   未检测到关键发现"
}
Write-Host ""

Write-Host "✅ 检查完成！" -ForegroundColor Green
Write-Host ""
Write-Host "💡 建议：" -ForegroundColor Yellow
Write-Host "  1. 用具体数据替代空洞形容词"
Write-Host "  2. 用语义衔接替代机械过渡词"
Write-Host "  3. 确保段落之间空一行"
Write-Host "  4. 每个发现都要回答 'So What'"
Write-Host "  5. 标注数据来源增强可信度"
Write-Host "  6. 确保图表编号连续"
