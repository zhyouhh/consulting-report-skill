import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
EVALS_PATH = REPO_ROOT / "evals" / "evals.json"
CAPABILITY_MAP_PATH = REPO_ROOT / "evals" / "capability-map.json"
MODULES_DIR = REPO_ROOT / "modules"


class CapabilityMapContractTests(unittest.TestCase):
    def test_capability_map_declares_shared_task_types_and_behavior_tags(self) -> None:
        capability_map = json.loads(CAPABILITY_MAP_PATH.read_text(encoding="utf-8"))

        self.assertIn("task_types", capability_map)
        self.assertIn("behavior_tags", capability_map)
        self.assertIn("general-report", capability_map["task_types"])
        self.assertIn("anti-ai-regression", capability_map["task_types"])
        self.assertIn("create_plan", capability_map["behavior_tags"])
        self.assertIn("route_to_quality_review", capability_map["behavior_tags"])

    def test_capability_map_references_real_modules(self) -> None:
        capability_map = json.loads(CAPABILITY_MAP_PATH.read_text(encoding="utf-8"))

        self.assertIn("capabilities", capability_map)
        self.assertGreaterEqual(len(capability_map["capabilities"]), 10)

        seen_modules: set[str] = set()
        for capability in capability_map["capabilities"]:
            self.assertIn("module", capability)
            self.assertIn("summary", capability)
            self.assertIn("task_types", capability)
            self.assertIn("trigger_phrases", capability)
            self.assertIn("outputs", capability)
            self.assertIn("aliases", capability)
            self.assertNotIn(capability["module"], seen_modules)
            seen_modules.add(capability["module"])
            self.assertTrue((MODULES_DIR / f"{capability['module']}.md").exists(), msg=capability["module"])

    def test_capability_map_task_types_are_constrained_by_shared_registry(self) -> None:
        capability_map = json.loads(CAPABILITY_MAP_PATH.read_text(encoding="utf-8"))
        valid_task_types = set(capability_map["task_types"])

        for capability in capability_map["capabilities"]:
            for task_type in capability["task_types"]:
                self.assertIn(task_type, valid_task_types, msg=f"{capability['module']} uses unknown task type {task_type}")

    def test_capability_map_keeps_executive_summary_visible(self) -> None:
        capability_map = json.loads(CAPABILITY_MAP_PATH.read_text(encoding="utf-8"))
        module_names = {capability["module"] for capability in capability_map["capabilities"]}

        self.assertIn("executive-summary", module_names)


class EvalsContractTests(unittest.TestCase):
    def test_evals_follow_v12_schema(self) -> None:
        capability_map = json.loads(CAPABILITY_MAP_PATH.read_text(encoding="utf-8"))
        evals_data = json.loads(EVALS_PATH.read_text(encoding="utf-8"))
        valid_categories = set(capability_map["task_types"])

        self.assertIn("evals", evals_data)
        self.assertGreaterEqual(len(evals_data["evals"]), 23)

        for eval_case in evals_data["evals"]:
            self.assertEqual(
                set(eval_case.keys()),
                {"id", "category", "prompt", "expected_modules", "expected_behaviors", "disallowed_signals"},
            )
            self.assertTrue(eval_case["id"])
            self.assertIn(eval_case["category"], valid_categories)
            self.assertTrue(eval_case["prompt"])
            self.assertTrue(eval_case["expected_modules"])
            self.assertTrue(eval_case["expected_behaviors"])
            self.assertIsInstance(eval_case["disallowed_signals"], list)

    def test_evals_reference_known_modules_and_behaviors(self) -> None:
        capability_map = json.loads(CAPABILITY_MAP_PATH.read_text(encoding="utf-8"))
        evals_data = json.loads(EVALS_PATH.read_text(encoding="utf-8"))
        known_modules = {capability["module"] for capability in capability_map["capabilities"]}
        valid_behaviors = set(capability_map["behavior_tags"])

        for eval_case in evals_data["evals"]:
            for module_name in eval_case["expected_modules"]:
                self.assertIn(module_name, known_modules, msg=f"unknown module in evals: {module_name}")
            for behavior_name in eval_case["expected_behaviors"]:
                self.assertIn(behavior_name, valid_behaviors, msg=f"unknown behavior in evals: {behavior_name}")

    def test_evals_cover_required_category_volume(self) -> None:
        capability_map = json.loads(CAPABILITY_MAP_PATH.read_text(encoding="utf-8"))
        evals_data = json.loads(EVALS_PATH.read_text(encoding="utf-8"))
        counts = {category: 0 for category in capability_map["task_types"]}

        for eval_case in evals_data["evals"]:
            counts[eval_case["category"]] += 1

        for category in {
            "general-report",
            "specialized-research",
            "management-document",
            "implementation-plan",
            "quick-delivery",
            "reviewable-draft",
        }:
            self.assertGreaterEqual(counts[category], 3, msg=f"insufficient coverage for {category}")

        self.assertGreaterEqual(counts["anti-ai-regression"], 5)

    def test_evals_include_executive_summary_coverage(self) -> None:
        evals_data = json.loads(EVALS_PATH.read_text(encoding="utf-8"))
        self.assertTrue(
            any("executive-summary" in eval_case["expected_modules"] for eval_case in evals_data["evals"]),
            msg="executive-summary is not covered by evals",
        )
