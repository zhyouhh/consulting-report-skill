import argparse
import json
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description="Run lightweight eval contract checks.")
    parser.add_argument("--evals", default=str(repo_root / "evals" / "evals.json"))
    parser.add_argument("--capability-map", default=str(repo_root / "evals" / "capability-map.json"))
    return parser.parse_args()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_constraint_corpus(repo_root: Path) -> str:
    candidate_paths = [
        repo_root / "README.md",
        repo_root / "SKILL.md",
        repo_root / "modules" / "writing-core.md",
        repo_root / "modules" / "common-gotchas.md",
        repo_root / "modules" / "quality-review.md",
        repo_root / "modules" / "final-delivery.md",
        repo_root / "scripts" / "quality_check.ps1",
        repo_root / "scripts" / "quality_check.sh",
    ]
    corpus_parts: list[str] = []
    for path in candidate_paths:
        if path.exists():
            corpus_parts.append(path.read_text(encoding="utf-8"))
    return "\n".join(corpus_parts)


def validate_registry(capability_map: dict) -> tuple[set[str], set[str], list[str]]:
    errors: list[str] = []
    task_types = capability_map.get("task_types")
    behavior_tags = capability_map.get("behavior_tags")

    if not isinstance(task_types, list) or not task_types:
        errors.append("capability map missing task_types")
        task_type_set: set[str] = set()
    else:
        task_type_set = set(task_types)
        if len(task_type_set) != len(task_types):
            errors.append("duplicate task type")

    if not isinstance(behavior_tags, list) or not behavior_tags:
        errors.append("capability map missing behavior_tags")
        behavior_tag_set: set[str] = set()
    else:
        behavior_tag_set = set(behavior_tags)
        if len(behavior_tag_set) != len(behavior_tags):
            errors.append("duplicate behavior tag")

    return task_type_set, behavior_tag_set, errors


def validate_capability_map(capability_map: dict, repo_root: Path, valid_task_types: set[str]) -> tuple[set[str], list[str]]:
    errors: list[str] = []
    capabilities = capability_map.get("capabilities")
    if not isinstance(capabilities, list) or not capabilities:
        return set(), ["capability map missing capabilities"]

    seen_modules: set[str] = set()
    for capability in capabilities:
        module_name = capability.get("module")
        if not module_name:
            errors.append("capability map missing module")
            continue
        if module_name in seen_modules:
            errors.append(f"duplicate module {module_name}")
        seen_modules.add(module_name)
        module_path = repo_root / "modules" / f"{module_name}.md"
        if not module_path.exists():
            errors.append(f"unknown module {module_name}")
        for field in ("summary", "task_types", "trigger_phrases", "outputs", "aliases"):
            if field not in capability:
                errors.append(f"capability {module_name} missing {field}")
        if isinstance(capability.get("task_types"), list):
            for task_type in capability["task_types"]:
                if task_type not in valid_task_types:
                    errors.append(f"capability {module_name} uses unknown task type {task_type}")
    return seen_modules, errors


def validate_evals(
    evals_data: dict,
    known_modules: set[str],
    valid_categories: set[str],
    valid_behaviors: set[str],
    corpus: str,
) -> list[str]:
    errors: list[str] = []
    evals = evals_data.get("evals")
    if not isinstance(evals, list) or not evals:
        return ["evals file missing evals"]

    seen_ids: set[str] = set()
    required_fields = {"id", "category", "prompt", "expected_modules", "expected_behaviors", "disallowed_signals"}

    for index, eval_case in enumerate(evals, start=1):
        case_id = eval_case.get("id", f"case-{index}")

        if set(eval_case.keys()) != required_fields:
            errors.append(f"{case_id}: invalid schema")
            continue

        if case_id in seen_ids:
            errors.append(f"{case_id}: duplicate id")
        seen_ids.add(case_id)

        category = eval_case["category"]
        if category not in valid_categories:
            errors.append(f"{case_id}: invalid category {category}")

        for module_name in eval_case["expected_modules"]:
            if module_name not in known_modules:
                errors.append(f"{case_id}: unknown module {module_name}")

        for behavior_name in eval_case["expected_behaviors"]:
            if behavior_name not in valid_behaviors:
                errors.append(f"{case_id}: unknown behavior {behavior_name}")

        disallowed_signals = eval_case["disallowed_signals"]
        if not isinstance(disallowed_signals, list):
            errors.append(f"{case_id}: invalid disallowed_signals")
        else:
            for signal in disallowed_signals:
                if signal and signal not in corpus:
                    errors.append(f"{case_id}: unconstrained signal {signal}")

    return errors


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    evals_path = Path(args.evals)
    capability_map_path = Path(args.capability_map)

    try:
        capability_map = load_json(capability_map_path)
        evals_data = load_json(evals_path)
    except FileNotFoundError as exc:
        print(f"FAIL missing file: {exc.filename}")
        return 1
    except json.JSONDecodeError as exc:
        print(f"FAIL invalid json: {exc}")
        return 1

    valid_categories, valid_behaviors, registry_errors = validate_registry(capability_map)
    known_modules, capability_errors = validate_capability_map(capability_map, repo_root, valid_categories)
    corpus = load_constraint_corpus(repo_root)
    eval_errors = validate_evals(evals_data, known_modules, valid_categories, valid_behaviors, corpus)
    errors = registry_errors + capability_errors + eval_errors

    if errors:
        for error in errors:
            print(f"FAIL {error}")
        print(f"FAIL summary: {len(errors)} issue(s)")
        return 1

    for eval_case in evals_data["evals"]:
        print(f"PASS {eval_case['id']}")
    print(f"PASS summary: {len(evals_data['evals'])} eval(s) validated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
