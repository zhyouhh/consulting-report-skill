import subprocess
import shutil
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
EVAL_FIXTURES = REPO_ROOT / "tests" / "fixtures" / "evals"
REPORT_FIXTURES = REPO_ROOT / "tests" / "fixtures"


def find_git_bash() -> str | None:
    candidates = [
        r"C:\Program Files\Git\bin\bash.exe",
        r"C:\Program Files\Git\usr\bin\bash.exe",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return candidate
    bash_on_path = shutil.which("bash")
    if bash_on_path and "Windows\\System32\\bash.exe" not in bash_on_path:
        return bash_on_path
    return None


def run_powershell_init_plan(workdir: Path, input_text: str | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            "pwsh",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(REPO_ROOT / "scripts" / "init_plan.ps1"),
        ],
        input=input_text,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        cwd=workdir,
        check=False,
    )


def run_shell_init_plan(workdir: Path, input_text: str | None = None) -> subprocess.CompletedProcess[str]:
    bash_path = find_git_bash()
    if bash_path is None:
        raise RuntimeError("git bash not available")
    return subprocess.run(
        [
            bash_path,
            str(REPO_ROOT / "scripts" / "init_plan.sh"),
        ],
        input=input_text,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        cwd=workdir,
        check=False,
    )


def run_shell_quality_check(report_path: Path) -> subprocess.CompletedProcess[str]:
    bash_path = find_git_bash()
    if bash_path is None:
        raise RuntimeError("git bash not available")
    return subprocess.run(
        [
            bash_path,
            str(REPO_ROOT / "scripts" / "quality_check.sh"),
            str(report_path),
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        cwd=REPO_ROOT,
        check=False,
    )


def run_shell_export_draft(report_path: Path, output_dir: Path) -> subprocess.CompletedProcess[str]:
    bash_path = find_git_bash()
    if bash_path is None:
        raise RuntimeError("git bash not available")
    return subprocess.run(
        [
            bash_path,
            str(REPO_ROOT / "scripts" / "export_draft.sh"),
            str(report_path),
            str(output_dir),
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        cwd=REPO_ROOT,
        check=False,
    )


def run_powershell_quality_check(report_path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            "pwsh",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(REPO_ROOT / "scripts" / "quality_check.ps1"),
            "-FilePath",
            str(report_path),
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        cwd=REPO_ROOT,
        check=False,
    )


def run_powershell_export_draft(report_path: Path, output_dir: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            "pwsh",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(REPO_ROOT / "scripts" / "export_draft.ps1"),
            "-InputPath",
            str(report_path),
            "-OutputDir",
            str(output_dir),
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        cwd=REPO_ROOT,
        check=False,
    )


def run_eval_runner(evals_path: Path, capability_map_path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            "python",
            str(REPO_ROOT / "scripts" / "run_evals.py"),
            "--evals",
            str(evals_path),
            "--capability-map",
            str(capability_map_path),
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        cwd=REPO_ROOT,
        check=False,
    )


class EvalRunnerTests(unittest.TestCase):
    def test_eval_runner_accepts_valid_fixture(self) -> None:
        result = run_eval_runner(EVAL_FIXTURES / "valid-evals.json", EVAL_FIXTURES / "capability-map.json")

        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        self.assertIn("PASS", result.stdout)

    def test_eval_runner_rejects_duplicate_ids(self) -> None:
        result = run_eval_runner(EVAL_FIXTURES / "duplicate-id-evals.json", EVAL_FIXTURES / "capability-map.json")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("duplicate id", (result.stdout + result.stderr).lower())

    def test_eval_runner_rejects_unknown_module(self) -> None:
        result = run_eval_runner(EVAL_FIXTURES / "unknown-module-evals.json", EVAL_FIXTURES / "capability-map.json")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unknown module", (result.stdout + result.stderr).lower())

    def test_eval_runner_rejects_unknown_behavior(self) -> None:
        result = run_eval_runner(EVAL_FIXTURES / "unknown-behavior-evals.json", EVAL_FIXTURES / "capability-map.json")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unknown behavior", (result.stdout + result.stderr).lower())

    def test_eval_runner_rejects_bad_category(self) -> None:
        result = run_eval_runner(EVAL_FIXTURES / "bad-category-evals.json", EVAL_FIXTURES / "capability-map.json")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("invalid category", (result.stdout + result.stderr).lower())

    def test_eval_runner_rejects_capability_map_with_invalid_task_type(self) -> None:
        result = run_eval_runner(EVAL_FIXTURES / "valid-evals.json", EVAL_FIXTURES / "capability-map-invalid-task-type.json")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unknown task type", (result.stdout + result.stderr).lower())


class InitPlanScriptTests(unittest.TestCase):
    def test_powershell_init_plan_bootstraps_from_current_workdir(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workdir = Path(temp_dir)
            result = run_powershell_init_plan(workdir)

            self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
            self.assertTrue((workdir / "plan" / "project-overview.md").exists())
            self.assertTrue((workdir / "plan" / "notes.md").exists())

    def test_powershell_init_plan_populates_existing_empty_plan_dir(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            workdir = Path(temp_dir)
            (workdir / "plan").mkdir()
            result = run_powershell_init_plan(workdir)

            self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
            self.assertTrue((workdir / "plan" / "project-overview.md").exists())

    def test_shell_init_plan_bootstraps_from_current_workdir(self) -> None:
        if find_git_bash() is None:
            self.skipTest("git bash not available")
        with tempfile.TemporaryDirectory() as temp_dir:
            workdir = Path(temp_dir)
            result = run_shell_init_plan(workdir)

            self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
            self.assertTrue((workdir / "plan" / "project-overview.md").exists())

    def test_shell_init_plan_populates_existing_empty_plan_dir(self) -> None:
        if find_git_bash() is None:
            self.skipTest("git bash not available")
        with tempfile.TemporaryDirectory() as temp_dir:
            workdir = Path(temp_dir)
            (workdir / "plan").mkdir()
            result = run_shell_init_plan(workdir)

            self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
            self.assertTrue((workdir / "plan" / "project-overview.md").exists())


class QualityCheckScriptTests(unittest.TestCase):
    def test_powershell_script_reports_risk_levels_without_blocking_content_issues(self) -> None:
        result = run_powershell_quality_check(REPORT_FIXTURES / "problematic-report.md")

        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        self.assertIn("高风险", result.stdout)
        self.assertIn("中风险", result.stdout)
        self.assertIn("低风险", result.stdout)
        self.assertIn("元叙事", result.stdout)
        self.assertIn("后台", result.stdout)
        self.assertIn("占位", result.stdout)

    def test_powershell_script_fails_for_missing_file(self) -> None:
        result = run_powershell_quality_check(REPORT_FIXTURES / "does-not-exist.md")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("文件不存在", result.stdout + result.stderr)

    def test_powershell_script_accepts_clean_report(self) -> None:
        result = run_powershell_quality_check(REPORT_FIXTURES / "clean-report.md")

        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        self.assertIn("检查完成", result.stdout)


class DraftExportScriptTests(unittest.TestCase):
    def test_powershell_export_script_fails_for_missing_input(self) -> None:
        output_dir = REPO_ROOT / "tests" / "tmp-missing"
        result = run_powershell_export_draft(REPORT_FIXTURES / "missing-report.md", output_dir)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("文件不存在", result.stdout + result.stderr)

    def test_powershell_export_script_creates_reviewable_docx(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT / "tests") as temp_dir:
            output_dir = Path(temp_dir)
            result = run_powershell_export_draft(REPORT_FIXTURES / "clean-report.md", output_dir)

            self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
            self.assertTrue((output_dir / "clean-report.docx").exists())
            self.assertIn("可审草稿", result.stdout)


class ShellScriptParityTests(unittest.TestCase):
    def test_shell_quality_check_executes_successfully(self) -> None:
        if find_git_bash() is None:
            self.skipTest("git bash not available")
        result = run_shell_quality_check(REPORT_FIXTURES / "problematic-report.md")

        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        self.assertIn("高风险", result.stdout)
        self.assertIn("中风险", result.stdout)
        self.assertIn("低风险", result.stdout)

    def test_shell_export_script_executes_successfully(self) -> None:
        if find_git_bash() is None:
            self.skipTest("git bash not available")
        with tempfile.TemporaryDirectory(dir=REPO_ROOT / "tests") as temp_dir:
            output_dir = Path(temp_dir)
            result = run_shell_export_draft(REPORT_FIXTURES / "clean-report.md", output_dir)

            self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
            self.assertTrue((output_dir / "clean-report.docx").exists())
            self.assertIn("可审草稿", result.stdout)

    def test_shell_script_contains_new_risk_categories(self) -> None:
        shell_text = (REPO_ROOT / "scripts" / "quality_check.sh").read_text(encoding="utf-8")

        self.assertIn("高风险", shell_text)
        self.assertIn("中风险", shell_text)
        self.assertIn("低风险", shell_text)
        self.assertIn("本章", shell_text)
        self.assertIn("技术规范书", shell_text)
        self.assertIn("XXX", shell_text)

    def test_export_shell_script_contains_reviewable_draft_flow(self) -> None:
        shell_text = (REPO_ROOT / "scripts" / "export_draft.sh").read_text(encoding="utf-8")

        self.assertIn("pandoc", shell_text)
        self.assertIn("可审草稿", shell_text)

    def test_init_plan_hook_targets_real_shell_script(self) -> None:
        hook_text = (REPO_ROOT / ".claude" / "hooks" / "init-plan-on-create.yaml").read_text(encoding="utf-8")

        self.assertIn('script: scripts/init_plan.sh', hook_text)
        self.assertIn('pattern: "plan/"', hook_text)
