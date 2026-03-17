#!/bin/bash

# 咨询报告质量检查脚本
# 用途：自动检测报告中的常见问题

if [ $# -eq 0 ]; then
    echo "用法: $0 <报告文件.md>"
    exit 1
fi

FILE="$1"

if [ ! -f "$FILE" ]; then
    echo "❌ 文件不存在: $FILE"
    exit 1
fi

echo "🔍 开始检查报告质量: $FILE"
echo ""

# 检查机械过渡词
echo "📝 检查机械过渡词..."
TRANSITIONS=$(grep -n -E "(首先|其次|最后|此外|另外|接下来)" "$FILE" || true)
if [ -n "$TRANSITIONS" ]; then
    echo "⚠️  发现机械过渡词："
    echo "$TRANSITIONS"
else
    echo "✅ 未发现机械过渡词"
fi
echo ""

# 检查空洞强调句
echo "📝 检查空洞强调句..."
EMPHASIS=$(grep -n -E "(值得注意的是|需要指出的是|重要的是|必须强调的是)" "$FILE" || true)
if [ -n "$EMPHASIS" ]; then
    echo "⚠️  发现空洞强调句："
    echo "$EMPHASIS"
else
    echo "✅ 未发现空洞强调句"
fi
echo ""

# 检查空洞形容词
echo "📝 检查空洞形容词..."
ADJECTIVES=$(grep -n -E "(非常|极其|十分|相当)" "$FILE" || true)
if [ -n "$ADJECTIVES" ]; then
    echo "⚠️  发现空洞形容词（建议用具体数据替代）："
    echo "$ADJECTIVES"
else
    echo "✅ 未发现空洞形容词"
fi
echo ""

# 检查段落格式
echo "📝 检查段落格式..."
EMPTY_LINES=$(grep -c "^$" "$FILE" || true)
TOTAL_LINES=$(wc -l < "$FILE")
echo "   空行数: $EMPTY_LINES / 总行数: $TOTAL_LINES"
echo ""

# 检查数据来源标注
echo "📝 检查数据来源标注..."
SOURCE=$(grep -n -E "(根据|来源：|数据来源)" "$FILE" || true)
if [ -n "$SOURCE" ]; then
    echo "✅ 发现数据来源标注："
    echo "$SOURCE"
else
    echo "⚠️  未发现数据来源标注（建议标注数据来源）"
fi
echo ""

# 检查图表编号连续性
echo "📝 检查图表编号连续性..."
FIGURE_NUMS=$(grep -o "图[0-9]\+" "$FILE" | grep -o "[0-9]\+" | sort -n || true)
if [ -n "$FIGURE_NUMS" ]; then
    PREV=0
    GAP_FOUND=false
    for NUM in $FIGURE_NUMS; do
        if [ $PREV -ne 0 ] && [ $((NUM - PREV)) -gt 1 ]; then
            echo "❌ 图编号不连续：图$PREV -> 图$NUM"
            GAP_FOUND=true
        fi
        PREV=$NUM
    done
    if [ "$GAP_FOUND" = false ]; then
        echo "✅ 图编号连续"
    fi
else
    echo "   未发现图编号"
fi
echo ""

# 检查表格编号连续性
echo "📝 检查表格编号连续性..."
TABLE_NUMS=$(grep -o "表[0-9]\+" "$FILE" | grep -o "[0-9]\+" | sort -n || true)
if [ -n "$TABLE_NUMS" ]; then
    PREV=0
    GAP_FOUND=false
    for NUM in $TABLE_NUMS; do
        if [ $PREV -ne 0 ] && [ $((NUM - PREV)) -gt 1 ]; then
            echo "❌ 表编号不连续：表$PREV -> 表$NUM"
            GAP_FOUND=true
        fi
        PREV=$NUM
    done
    if [ "$GAP_FOUND" = false ]; then
        echo "✅ 表编号连续"
    fi
else
    echo "   未发现表格编号"
fi
echo ""

# 检查 So What（关键发现但缺少行动建议）
echo "📝 检查 So What..."
KEY_FINDINGS=$(grep -n -E "(发现|显示|表明|数据显示)" "$FILE" || true)
if [ -n "$KEY_FINDINGS" ]; then
    ACTION_WORDS=$(grep -c -E "(建议|应当|需要|可以|应该)" "$FILE" || true)
    if [ "$ACTION_WORDS" -lt 3 ]; then
        echo "⚠️  发现关键发现但行动建议较少（建议回答 'So What'）"
    else
        echo "✅ 包含行动建议"
    fi
else
    echo "   未检测到关键发现"
fi
echo ""

echo "✅ 检查完成！"
echo ""
echo "💡 建议："
echo "  1. 用具体数据替代空洞形容词"
echo "  2. 用语义衔接替代机械过渡词"
echo "  3. 确保段落之间空一行"
echo "  4. 每个发现都要回答 'So What'"
echo "  5. 标注数据来源增强可信度"
echo "  6. 确保图表编号连续"
