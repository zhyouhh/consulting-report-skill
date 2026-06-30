import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import benchmark_anti_ai as bench  # noqa: E402

FIXTURES = REPO_ROOT / "tests" / "fixtures"
BENCH = FIXTURES / "benchmark"


class AntiAiBenchmarkTests(unittest.TestCase):
    def test_clean_fixture_scores_higher_than_problematic(self) -> None:
        clean, _ = bench.score_file(FIXTURES / "clean-report.md")
        prob, _ = bench.score_file(FIXTURES / "problematic-report.md")

        self.assertEqual(clean, 100)
        self.assertGreaterEqual(clean - prob, 50)

    def test_cleaned_corpus_beats_baseline_by_margin(self) -> None:
        baseline_dir = BENCH / "baseline"
        cleaned_dir = BENCH / "cleaned"
        names = sorted(p.name for p in baseline_dir.glob("*.md"))

        self.assertGreaterEqual(len(names), 3, msg="benchmark corpus must have >=3 pairs")
        for name in names:
            self.assertTrue((cleaned_dir / name).exists(), msg=f"missing cleaned/{name}")

        base = [bench.score_file(baseline_dir / n)[0] for n in names]
        clean = [bench.score_file(cleaned_dir / n)[0] for n in names]
        base_avg = sum(base) / len(base)
        clean_avg = sum(clean) / len(clean)

        # 回归护栏：去 AI 味后洁净度必须显著高于 baseline
        self.assertGreaterEqual(clean_avg - base_avg, 30)
        for c in clean:
            self.assertGreaterEqual(c, 90, msg="cleaned 语料不应残留显著 AI 痕迹")

    def test_corpus_scores_match_readme_numbers(self) -> None:
        # 锁住 README 登出的精确分数，改语料/评分器若动了这两个数，测试会拦住
        baseline_dir = BENCH / "baseline"
        cleaned_dir = BENCH / "cleaned"
        names = sorted(p.name for p in baseline_dir.glob("*.md"))
        base = [bench.score_file(baseline_dir / n)[0] for n in names]
        clean = [bench.score_file(cleaned_dir / n)[0] for n in names]
        base_avg = sum(base) / len(base)
        clean_avg = sum(clean) / len(clean)

        self.assertAlmostEqual(base_avg, 28.7, places=1)
        self.assertAlmostEqual(clean_avg, 99.0, places=1)

    def test_technical_bid_exemption_in_scorer(self) -> None:
        bid = (
            "# 技术标（技术投标文件）\n技术规范书点对点应答\n"
            "根据招标文件，本方案严格响应技术规范书要求。"
        )
        free = "根据公开资料，本方案严格响应技术规范书要求。"

        bid_score, _ = bench.score_text(bid)
        free_score, _ = bench.score_text(free)

        # 技术标场景下「技术规范书」是正式术语，不应被当后台词扣分
        self.assertGreater(bid_score, free_score)

    def test_three_part_not_penalized_in_technical_bid(self) -> None:
        bid = (
            "# 技术标（技术投标文件）\n技术规范书点对点应答\n根据评分标准，"
            "首先完成需求评估，其次开展方案设计，最后推进实施落地。"
        )
        free = "根据评分标准，首先完成需求评估，其次开展方案设计，最后推进实施落地。"

        _, bid_hits = bench.score_text(bid)
        _, free_hits = bench.score_text(free)

        # 技术标模式下三段式不计痕迹，自由报告里照计——与 quality_check 口径一致
        self.assertEqual(bid_hits["low:三段式套话"], 0)
        self.assertEqual(free_hits["low:三段式套话"], 1)


if __name__ == "__main__":
    unittest.main()
