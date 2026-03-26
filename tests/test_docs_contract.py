import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class PublicDocsContractTests(unittest.TestCase):
    def test_readme_is_upgraded_to_v12_information_architecture(self) -> None:
        readme_text = (REPO_ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("v1.2", readme_text)
        self.assertIn("快速开始", readme_text)
        self.assertIn("推荐提问方式", readme_text)
        self.assertIn("自检与评测", readme_text)

    def test_supporting_docs_exist_for_shared_usage(self) -> None:
        docs_dir = REPO_ROOT / "docs"
        required_docs = {
            "quickstart.md": ["scripts/init_plan", "scripts/quality_check", "scripts/export_draft"],
            "prompt-cookbook.md": ["标准咨询报告", "形式交付", "继续已有项目", "质量审查", "可审草稿"],
            "module-routing.md": ["通用主流程", "常见误用", "strategy-consulting", "quality-review"],
            "self-check.md": ["python -m unittest discover -s tests -v", "python scripts/run_evals.py", "post-report-quality-check.yaml"],
        }

        for filename, snippets in required_docs.items():
            path = docs_dir / filename
            self.assertTrue(path.exists(), msg=f"missing doc: {filename}")
            text = path.read_text(encoding="utf-8")
            for snippet in snippets:
                self.assertIn(snippet, text, msg=f"{filename} missing {snippet}")

    def test_skill_and_readme_versions_align_on_v12_boundary(self) -> None:
        skill_text = (REPO_ROOT / "SKILL.md").read_text(encoding="utf-8")
        readme_text = (REPO_ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("版本：1.2.0", skill_text)
        self.assertIn("版本：1.2.0", readme_text)
        self.assertIn("可审草稿", readme_text)
        self.assertIn("不承诺", readme_text)

    def test_skill_mentions_guardrail_and_delivery_modules(self) -> None:
        skill_text = (REPO_ROOT / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn("common-gotchas", skill_text)
        self.assertIn("final-delivery", skill_text)

    def test_quality_review_keeps_structure_sensitive_checks(self) -> None:
        review_text = (REPO_ROOT / "modules" / "quality-review.md").read_text(encoding="utf-8")

        self.assertNotIn("是否有执行摘要", review_text)
        self.assertNotIn("附录是否齐全", review_text)
