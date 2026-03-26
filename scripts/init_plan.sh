#!/usr/bin/env bash

# 咨询报告项目初始化脚本
# 用途：在当前工作目录下创建/补齐 plan 目录，并从仓库模板复制项目管理文件

set -euo pipefail

force=0
if [[ "${1:-}" == "--force" ]]; then
  force=1
fi

script_source="${BASH_SOURCE[0]}"
if command -v cygpath >/dev/null 2>&1 && [[ "$script_source" =~ ^[A-Za-z]:\\ ]]; then
  script_source="$(cygpath "$script_source")"
fi

script_dir="$(cd -- "$(dirname -- "$script_source")" && pwd)"
template_dir="$(cd -- "$script_dir/../plan-template" && pwd)"
plan_dir="$(pwd)/plan"
managed_files=(
  "project-overview.md"
  "stage-gates.md"
  "progress.md"
  "research-plan.md"
  "notes.md"
)

echo "🚀 开始初始化咨询报告项目..."

if [[ ! -d "$template_dir" ]]; then
  echo "❌ 错误：模板目录不存在: $template_dir" >&2
  exit 1
fi

overwrite_managed_files=0
if [[ ! -d "$plan_dir" ]]; then
  echo "📁 创建 plan 目录..."
  mkdir -p "$plan_dir"
else
  existing_managed_files=0
  for file_name in "${managed_files[@]}"; do
    if [[ -f "$plan_dir/$file_name" ]]; then
      existing_managed_files=1
      break
    fi
  done

  if [[ "$existing_managed_files" -eq 0 ]]; then
    echo "📁 检测到已有 plan 目录，将补齐模板文件..."
  elif [[ "$force" -eq 1 ]]; then
    echo "📁 plan 目录已存在，按 force 模式覆盖模板文件..."
    overwrite_managed_files=1
  else
    echo "⚠️  plan 目录已存在且包含模板文件，是否覆盖这些模板文件？(y/n)"
    read -r response
    if [[ "$response" != "y" ]]; then
      echo "❌ 取消初始化"
      exit 0
    fi
    overwrite_managed_files=1
  fi
fi

echo "📄 复制模板文件..."
for file_name in "${managed_files[@]}"; do
  source_path="$template_dir/$file_name"
  target_path="$plan_dir/$file_name"
  if [[ "$overwrite_managed_files" -eq 1 || ! -f "$target_path" ]]; then
    cp "$source_path" "$target_path"
  fi
done

echo "✅ 初始化完成！"
echo ""
echo "已确保以下文件存在："
echo "  - plan/project-overview.md"
echo "  - plan/stage-gates.md"
echo "  - plan/progress.md"
echo "  - plan/research-plan.md"
echo "  - plan/notes.md"
echo ""
echo "💡 下一步：编辑 plan/project-overview.md 填写项目信息"
