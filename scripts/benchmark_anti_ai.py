#!/usr/bin/env python3
"""去 AI 味·确定性洁净度基准。

这是什么：一个确定性评分器，**检测项复用** `quality_check` 那套 AI 痕迹（元叙事、后台词、
占位符、机械过渡词、空洞强调/形容词、AI 套话词、破折号、三段式、emoji、无来源），给 Markdown
稿打一个 0-100 的「AI 痕迹洁净度」分（痕迹越少分越高）。它**不是** LLM 主观质量分，不声称等同
人评——衡量的是脚本可机检的 AI 痕迹密度，用于：
  1. 量化展示 skill 引导前后的差距（README 登分）；
  2. 回归护栏：cleaned 语料分数必须显著高于 baseline，改坏了会被测试拦住。

计数口径与 quality_check 的差异（透明声明）：本评分器对高/中风险痕迹按**出现次数**累加扣分，
而 quality_check 的摘要按**命中行数**计数，因此两者绝对分数不直接可比，但方向一致。

用法：
  python scripts/benchmark_anti_ai.py                 # 跑配对语料，输出 baseline vs cleaned 差值
  python scripts/benchmark_anti_ai.py path/to/report.md   # 给单个文件打分

评分模型（透明、可复算）：score = max(0, 100 - Σ penalty)
  高风险痕迹 每处 -15；中风险痕迹 每处 -6；低风险痕迹 每类命中 -3。
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from count_emoji import EMOJI_RE  # emoji 检测的单一事实源，与 quality_check 共用

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CORPUS = REPO_ROOT / "tests" / "fixtures" / "benchmark"

HIGH_PENALTY = 15
MID_PENALTY = 6
LOW_PENALTY = 3

# 技术标专有结构出现时，「技术规范书 / 技规」是招标正式术语，不计为后台词（与 quality_check 一致）
BID_MARKERS = ("技术评分索引表", "技术规范书点对点应答", "技术标（技术投标文件）")
BACKSTAGE_FULL = r"技术规范书|内部材料|内部资料|AI reference|AI材料|技规"
BACKSTAGE_BID = r"内部材料|内部资料|AI reference|AI材料"

HIGH_PATTERNS = [
    ("元叙事", r"本章|本报告|后文|下文|换言之|总体来看|本质上看|也正因为如此|进一步看"),
    ("占位符", r"XXX|待确认|TBD|TODO|待补"),
]
MID_PATTERNS = [
    ("机械过渡词", r"首先|其次|最后|此外|另外|接下来"),
    ("空洞强调句", r"值得注意的是|需要指出的是|重要的是|必须强调的是"),
    ("空洞形容词", r"非常|极其|十分|相当"),
    ("AI 套话词", r"赋能|抓手|组合拳|多措并举"),
]


def count_hits(text: str) -> dict[str, int]:
    """返回每类痕迹的命中数（高/中按出现次数，低按是否命中）。"""
    is_bid = any(m in text for m in BID_MARKERS)
    backstage = BACKSTAGE_BID if is_bid else BACKSTAGE_FULL
    hits: dict[str, int] = {}
    for name, pat in HIGH_PATTERNS:
        hits[f"high:{name}"] = len(re.findall(pat, text))
    hits["high:后台词"] = len(re.findall(backstage, text))
    for name, pat in MID_PATTERNS:
        hits[f"mid:{name}"] = len(re.findall(pat, text))
    # 低风险：每类命中即 +1（与 quality_check 摘要口径一致）
    hits["low:破折号滥用"] = 1 if text.count("——") >= 3 else 0
    # 三段式：技术标按评分点列项是要求、不算痕迹，与 quality_check 技术标模式一致
    hits["low:三段式套话"] = 0 if is_bid else (1 if ("首先" in text and "其次" in text and "最后" in text) else 0)
    hits["low:emoji"] = 1 if EMOJI_RE.search(text) else 0
    hits["low:无来源"] = 0 if re.search(r"根据|来源：|数据来源|资料来源", text) else 1
    return hits


def score_text(text: str) -> tuple[int, dict[str, int]]:
    hits = count_hits(text)
    penalty = 0
    for key, n in hits.items():
        if not n:
            continue
        if key.startswith("high:"):
            penalty += HIGH_PENALTY * n
        elif key.startswith("mid:"):
            penalty += MID_PENALTY * n
        else:
            penalty += LOW_PENALTY * n
    return max(0, 100 - penalty), hits


def score_file(path: Path) -> tuple[int, dict[str, int]]:
    return score_text(path.read_text(encoding="utf-8"))


def run_corpus(corpus: Path) -> int:
    baseline_dir = corpus / "baseline"
    cleaned_dir = corpus / "cleaned"
    if not baseline_dir.is_dir() or not cleaned_dir.is_dir():
        print(f"❌ 语料目录不完整: {corpus}", file=sys.stderr)
        return 2

    pairs = sorted(p.name for p in baseline_dir.glob("*.md"))
    if not pairs:
        print(f"❌ 未找到配对语料: {baseline_dir}", file=sys.stderr)
        return 2

    print(f"📊 去 AI 味洁净度基准（语料: {corpus.relative_to(REPO_ROOT)}）\n")
    print(f"{'样本':<16}{'baseline':>10}{'cleaned':>10}{'Δ':>8}")
    print("-" * 44)
    base_scores: list[int] = []
    clean_scores: list[int] = []
    for name in pairs:
        b, _ = score_file(baseline_dir / name)
        cleaned_path = cleaned_dir / name
        if not cleaned_path.exists():
            print(f"⚠️  缺少 cleaned/{name}，跳过", file=sys.stderr)
            continue
        c, _ = score_file(cleaned_path)
        base_scores.append(b)
        clean_scores.append(c)
        print(f"{name:<16}{b:>10}{c:>10}{c - b:>+8}")

    base_avg = sum(base_scores) / len(base_scores)
    clean_avg = sum(clean_scores) / len(clean_scores)
    print("-" * 44)
    print(f"{'平均':<16}{base_avg:>10.1f}{clean_avg:>10.1f}{clean_avg - base_avg:>+8.1f}")
    print(f"\n结论：去 AI 味后洁净度平均提升 {clean_avg - base_avg:+.1f} 分"
          f"（baseline {base_avg:.1f} → cleaned {clean_avg:.1f}）。")
    print("说明：本分数为确定性 AI 痕迹洁净度（脚本可机检项），非 LLM 主观质量分。")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="去 AI 味洁净度基准")
    parser.add_argument("file", nargs="?", help="给单个 Markdown 文件打分；省略则跑配对语料")
    parser.add_argument("--corpus", default=str(DEFAULT_CORPUS), help="配对语料目录")
    args = parser.parse_args(argv)

    if args.file:
        path = Path(args.file)
        if not path.exists():
            print(f"❌ 文件不存在: {path}", file=sys.stderr)
            return 1
        score, hits = score_file(path)
        flagged = {k: v for k, v in hits.items() if v}
        print(f"{path.name}: 洁净度 {score}/100")
        if flagged:
            print("命中痕迹:", ", ".join(f"{k}×{v}" for k, v in flagged.items()))
        return 0

    return run_corpus(Path(args.corpus))


if __name__ == "__main__":
    raise SystemExit(main())
