#!/bin/bash

# 咨询报告项目初始化脚本
# 用途：自动创建 plan 目录并复制模板文件

set -e

echo "🚀 开始初始化咨询报告项目..."

# 检查是否在正确的目录
if [ ! -f "consulting-report-skill/SKILL.md" ]; then
    echo "❌ 错误：请在项目根目录运行此脚本"
    exit 1
fi

# 创建 plan 目录
if [ -d "plan" ]; then
    echo "⚠️  plan 目录已存在，是否覆盖？(y/n)"
    read -r response
    if [ "$response" != "y" ]; then
        echo "❌ 取消初始化"
        exit 0
    fi
    rm -rf plan
fi

echo "📁 创建 plan 目录..."
mkdir -p plan

# 复制模板文件
echo "📄 复制模板文件..."
cp consulting-report-skill/plan-template/project-overview.md plan/
cp consulting-report-skill/plan-template/stage-gates.md plan/
cp consulting-report-skill/plan-template/progress.md plan/
cp consulting-report-skill/plan-template/research-plan.md plan/
cp consulting-report-skill/plan-template/notes.md plan/

echo "✅ 初始化完成！"
echo ""
echo "已创建以下文件："
echo "  - plan/project-overview.md"
echo "  - plan/stage-gates.md"
echo "  - plan/progress.md"
echo "  - plan/research-plan.md"
echo "  - plan/notes.md"
echo ""
echo "💡 下一步：编辑 plan/project-overview.md 填写项目信息"
