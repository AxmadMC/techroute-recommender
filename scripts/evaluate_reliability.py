"""Evaluate ranking and RAG reliability against TechRoute opportunities."""

import argparse
from collections import Counter
from contextlib import redirect_stdout
from datetime import date
from io import StringIO
import logging
from pathlib import Path
import sys
import time
from typing import Callable, Dict, List, Optional, Tuple

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.path_generator import (
    FALLBACK_SOURCE,
    _load_gemini_config,
    _retrieve_opportunities,
    generate_learning_path,
    validate_profile,
)
from src.profiles import EVALUATION_PROFILE_NAMES, PROFILE_LABELS, PROFILE_PRESETS
from src.recommender import load_opportunities, recommend_opportunities

Profile = Dict[str, object]
Recommendation = Tuple[Dict, float, str]
Check = Callable[..., Tuple[bool, str]]
EXPECTED_STAGES = ("Foundations", "Build Skills", "Prove Skills", "Apply")
CALL_PAUSE_SECONDS = 1.0
REPORT_PATH = PROJECT_ROOT / "assets" / "evaluation_results.md"

PROFILES: List[Tuple[str, Profile]] = [
    (PROFILE_LABELS[name], PROFILE_PRESETS[name])
    for name in EVALUATION_PROFILE_NAMES
]


def check_track_relevance(
    profile: Profile, results: List[Recommendation], _: str = ""
) -> Tuple[bool, str]:
    target = profile["target_track"]
    matches = sum(
        opportunity.get("career_track") == target
        for opportunity, _, _ in results
    )
    return matches >= 4, f"{matches}/{len(results)} recommendations match {target}"


def check_remote_guardrail(
    profile: Profile, results: List[Recommendation], _: str = ""
) -> Tuple[bool, str]:
    if profile["needs_remote"] is not True:
        return True, "Remote requirement is not enabled"
    non_remote = [
        opportunity["title"]
        for opportunity, _, _ in results
        if opportunity.get("remote") is not True
    ]
    return not non_remote, (
        "all results are remote"
        if not non_remote
        else f"non-remote results: {', '.join(non_remote)}"
    )


def check_prerequisite_guardrail(
    profile: Profile, results: List[Recommendation], _: str = ""
) -> Tuple[bool, str]:
    if profile["skill_level"] >= 0.5 or not results:
        return True, "no low-skill prerequisite violation at rank #1"
    first = results[0][0]
    tags = set(filter(None, (first.get("eligibility") or "").split(";")))
    has_prerequisite = "prior_experience" in tags
    return not has_prerequisite, (
        f"rank #1: {first['title']}"
        + (
            " requires prior experience"
            if has_prerequisite
            else " has no prior_experience tag"
        )
    )


def check_result_count(
    _: Profile, results: List[Recommendation], recommender_output: str = ""
) -> Tuple[bool, str]:
    if len(results) == 5:
        return True, "returned 5 recommendations"
    has_shortfall_message = "fewer than 5" in recommender_output
    return has_shortfall_message, (
        f"returned {len(results)}; "
        + (
            "recommender printed a clear fewer-than-5 message"
            if has_shortfall_message
            else "no clear fewer-than-5 message was printed"
        )
    )


def check_grounding(
    path: Dict[str, object], retrieved: List[Dict[str, object]]
) -> Tuple[bool, str]:
    retrieved_titles = {item["title"] for item in retrieved}
    path_titles = {
        title
        for step in path["steps"]
        for title in step["opportunity_titles"]
    }
    invented = sorted(path_titles - retrieved_titles)
    return not invented, (
        "all path titles are in the retrieved set"
        if not invented
        else f"unretrieved titles: {', '.join(invented)}"
    )


def check_structure(path: Dict[str, object]) -> Tuple[bool, str]:
    steps = path["steps"]
    details = []
    for stage in EXPECTED_STAGES:
        matching = [step for step in steps if step.get("stage") == stage]
        if not matching:
            details.append(f"{stage} stage missing")
    if not details:
        return (
            True,
            "all four stages are present; empty stages are explicitly printed as none",
        )
    return False, "; ".join(details)


def check_no_invented_apply(
    path: Dict[str, object], retrieved: List[Dict[str, object]]
) -> Tuple[bool, str]:
    apply_steps = [step for step in path["steps"] if step.get("stage") == "Apply"]
    apply_titles = {
        item["title"]
        for item in retrieved
        if item.get("type") in {"internship", "job"}
    }
    if apply_titles:
        return True, f"{len(apply_titles)} internship/job item(s) retrieved"
    if not apply_steps:
        return False, "Apply step is missing"

    mentioned_titles = [
        title
        for step in apply_steps
        for title in step.get("opportunity_titles", [])
    ]
    text = " ".join(
        f"{step.get('goal', '')} {step.get('why', '')}" for step in apply_steps
    ).lower()
    clear_none_message = (
        ("no " in text or "none" in text or "not available" in text)
        and ("internship" in text or "job" in text)
    )
    passed = not mentioned_titles and clear_none_message
    return passed, (
        "Apply says no internships/jobs are available and names none"
        if passed
        else "Apply must say none are available and list no opportunities"
    )


def check_apply_contains_retrieved_internship_job(
    path: Dict[str, object], retrieved: List[Dict[str, object]]
) -> Tuple[bool, str]:
    internship_job_titles = {
        item["title"]
        for item in retrieved
        if item.get("type") in {"internship", "job"}
    }
    if not internship_job_titles:
        return True, "not applicable: no internship/job rows were retrieved"

    apply_steps = [step for step in path["steps"] if step.get("stage") == "Apply"]
    apply_titles = {
        title
        for step in apply_steps
        for title in step.get("opportunity_titles", [])
    }
    included = sorted(internship_job_titles & apply_titles)
    if included:
        return True, f"Apply includes retrieved opportunity: {', '.join(included)}"
    if not apply_steps:
        return False, "Apply step is missing despite retrieved internship/job rows"
    return False, "Apply step omits all retrieved internship/job rows"


def check_source_label(path: Dict[str, object]) -> Tuple[bool, str]:
    source = path.get("source", "")
    valid_gemini = is_gemini_source(path)
    valid_fallback = isinstance(source, str) and source.startswith(
        f"{FALLBACK_SOURCE} (reason: "
    )
    return valid_gemini or valid_fallback, str(source)


def is_gemini_source(path: Dict[str, object]) -> bool:
    source = path.get("source", "")
    return isinstance(source, str) and source.startswith(
        "Source: Gemini (verified"
    )


def check_agent_stage_size(path: Dict[str, object]) -> Tuple[bool, str]:
    oversized = [
        f"{step.get('stage', 'Unknown')}={len(step.get('opportunity_titles', []))}"
        for step in path["steps"]
        if len(step.get("opportunity_titles", [])) > 3
    ]
    return not oversized, (
        "all stages contain at most 3 opportunities"
        if not oversized
        else f"stage sizes exceed 3: {', '.join(oversized)}"
    )


def check_agent_duplicate_titles(path: Dict[str, object]) -> Tuple[bool, str]:
    title_stages: Dict[str, str] = {}
    duplicates = []
    for step in path["steps"]:
        stage = step.get("stage", "Unknown")
        for title in step.get("opportunity_titles", []):
            previous_stage = title_stages.get(title)
            if previous_stage is not None and previous_stage != stage:
                duplicates.append(f"{title} ({previous_stage}, {stage})")
            else:
                title_stages[title] = stage
    return not duplicates, (
        "no opportunity title appears across multiple stages"
        if not duplicates
        else f"duplicate titles across stages: {', '.join(duplicates)}"
    )


RANKING_CHECKS: List[Tuple[str, Check]] = [
    ("Track relevance", check_track_relevance),
    ("Remote guardrail", check_remote_guardrail),
    ("Prerequisite guardrail", check_prerequisite_guardrail),
    ("Result count", check_result_count),
]
PATH_CHECKS: List[Tuple[str, Check]] = [
    ("Grounding", check_grounding),
    ("Structure", check_structure),
    ("No invented opportunities", check_no_invented_apply),
    (
        "Apply step contains at least one retrieved internship/job",
        check_apply_contains_retrieved_internship_job,
    ),
    ("Source label", check_source_label),
    ("Agent: stage size <= 3", check_agent_stage_size),
    ("Agent: no duplicate titles", check_agent_duplicate_titles),
]


class CallPacer:
    def __init__(self, enabled: bool):
        self.enabled = enabled
        self.call_count = 0

    def before_call(self) -> None:
        if self.enabled and self.call_count:
            time.sleep(CALL_PAUSE_SECONDS)
        if self.enabled:
            self.call_count += 1


def _record_check(
    lines: List[str],
    counts: Dict[str, int],
    check_name: str,
    passed: bool,
    detail: str,
) -> None:
    counts["total"] += 1
    if passed:
        counts["passed"] += 1
    status = "PASS" if passed else "FAIL"
    lines.append(f"{status}: {check_name}: {detail}")


def _run_profile(
    profile_name: str,
    profile: Profile,
    opportunities: List[Dict],
    offline: bool,
    pacer: CallPacer,
    lines: List[str],
    counts: Dict[str, int],
    path_sources: Counter,
) -> Tuple[Dict[str, object], List[Dict[str, object]]]:
    safe_profile = validate_profile(profile)
    lines.append(f"\n=== {profile_name} ===")
    lines.append(f"Input profile: {safe_profile}")

    captured = StringIO()
    with redirect_stdout(captured):
        rankings = recommend_opportunities(safe_profile, opportunities, k=5)
    recommender_output = captured.getvalue()
    if recommender_output:
        lines.append(recommender_output.rstrip())

    for rank, (opportunity, score, explanation) in enumerate(rankings, start=1):
        lines.append(
            f"{rank}. {opportunity['title']} | {opportunity['provider']} "
            f"| score={score:.2f}"
        )
        lines.append(f"   {explanation}")

    for check_name, check in RANKING_CHECKS:
        passed, detail = check(safe_profile, rankings, recommender_output)
        _record_check(lines, counts, check_name, passed, detail)

    retrieved = _retrieve_opportunities(safe_profile, opportunities)
    lines.append(f"Retrieved opportunities for path generation: {len(retrieved)}")
    if not offline:
        pacer.before_call()
    path = generate_learning_path(
        safe_profile,
        opportunities,
        offline=offline,
    )

    source = path["source"]
    path_sources["Gemini" if is_gemini_source(path) else "fallback"] += 1
    lines.append(str(source))
    lines.append(f"Agent repair attempts used: {path.get('repair_attempts', 0)}")
    for step in path["steps"]:
        lines.append(f"{step['step_number']}. {step['stage']}: {step['goal']}")
        if step["opportunity_titles"]:
            lines.append(f"   Opportunities: {', '.join(step['opportunity_titles'])}")
        else:
            lines.append("   Opportunities: none")
        lines.append(f"   Why: {step['why']}")

    for check_name, check in PATH_CHECKS:
        if check_name == "Grounding":
            passed, detail = check(path, retrieved)
        elif check_name == "Structure":
            passed, detail = check(path)
        elif check_name in {
            "No invented opportunities",
            "Apply step contains at least one retrieved internship/job",
        }:
            passed, detail = check(path, retrieved)
        else:
            passed, detail = check(path)
        _record_check(lines, counts, check_name, passed, detail)
    return path, retrieved


def _title_overlap(first_path: Dict[str, object], second_path: Dict[str, object]) -> float:
    first_titles = {
        title
        for step in first_path["steps"]
        for title in step["opportunity_titles"]
    }
    second_titles = {
        title
        for step in second_path["steps"]
        for title in step["opportunity_titles"]
    }
    union = first_titles | second_titles
    return len(first_titles & second_titles) / len(union) * 100 if union else 0.0


def _write_report(command: str, output: str) -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    report = (
        "# RAG Reliability Evaluation\n\n"
        f"- Command: `{command}`\n"
        f"- Date: {date.today().isoformat()}\n\n"
        "```text\n"
        f"{output.rstrip()}\n"
        "```\n"
    )
    sections = []
    if REPORT_PATH.exists():
        sections = REPORT_PATH.read_text(encoding="utf-8").split(
            "\n\n---\n\n"
        )
        sections = [
            section
            for section in sections
            if f"- Command: `{command}`" not in section
        ]
    sections.append(report.rstrip())
    REPORT_PATH.write_text(
        "\n\n---\n\n".join(sections) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--offline",
        action="store_true",
        help="Force rule-based paths and make no Gemini API calls.",
    )
    args = parser.parse_args(argv)
    command = "python scripts/evaluate_reliability.py"
    if args.offline:
        command += " --offline"

    app_logger = logging.getLogger("techroute")
    app_logger.addHandler(logging.NullHandler())
    app_logger.propagate = False

    captured_loader = StringIO()
    with redirect_stdout(captured_loader):
        opportunities = load_opportunities(
            str(PROJECT_ROOT / "data" / "opportunities.csv")
        )

    if args.offline:
        key_available = False
    else:
        api_key, _ = _load_gemini_config()
        key_available = bool(api_key)
        del api_key
    online = key_available and not args.offline
    pacer = CallPacer(online)
    path_sources: Counter = Counter()
    counts = {"total": 0, "passed": 0}
    lines = [
        f"Command: {command}",
        f"Date: {date.today().isoformat()}",
        f"Dataset rows: {len(opportunities)}",
        (
            "Gemini mode: online"
            if online
            else (
                "Gemini mode: offline"
                if args.offline
                else "Gemini mode: unavailable; fallback paths will be used"
            )
        ),
    ]

    profile_paths: Dict[str, Dict[str, object]] = {}
    cloud_profile: Optional[Profile] = None
    cloud_name = "Cloud career changer"
    for profile_name, profile in PROFILES:
        path, _ = _run_profile(
            profile_name,
            profile,
            opportunities,
            args.offline,
            pacer,
            lines,
            counts,
            path_sources,
        )
        profile_paths[profile_name] = path
        if profile_name == cloud_name:
            cloud_profile = profile

    consistency_overlap: Optional[float] = None
    consistency_result = "Not run (offline mode)" if args.offline else "Not run (no API key)"
    if online and cloud_profile is not None:
        lines.append("\n=== Cloud career changer consistency run ===")
        pacer.before_call()
        second_cloud_path = generate_learning_path(cloud_profile, opportunities)
        path_sources[
            "Gemini" if is_gemini_source(second_cloud_path) else "fallback"
        ] += 1
        first_cloud_path = profile_paths[cloud_name]
        if (
            is_gemini_source(first_cloud_path)
            and is_gemini_source(second_cloud_path)
        ):
            consistency_overlap = _title_overlap(
                first_cloud_path, second_cloud_path
            )
            passed = consistency_overlap >= 70.0
            consistency_result = (
                f"{'PASS' if passed else 'FAIL'}: title overlap "
                f"{consistency_overlap:.1f}% (Jaccard; threshold 70%)"
            )
            _record_check(
                lines,
                counts,
                "Gemini consistency",
                passed,
                consistency_result.split(": ", 1)[1],
            )
        else:
            consistency_result = (
                "FAIL: overlap unavailable because one or both Gemini runs "
                "fell back to the rule-based path"
            )
            _record_check(
                lines,
                counts,
                "Gemini consistency",
                False,
                consistency_result.removeprefix("FAIL: "),
            )
        lines.append(f"Second run source: {second_cloud_path['source']}")
        lines.append(
            "Consistency run repair attempts used: "
            f"{second_cloud_path.get('repair_attempts', 0)}"
        )
        lines.append(f"Consistency overlap: {consistency_result}")

    failed = counts["total"] - counts["passed"]
    rate = counts["passed"] / counts["total"] * 100 if counts["total"] else 0.0
    lines.extend(
        [
            "\n=== Final summary ===",
            f"Total checks: {counts['total']}",
            f"Passed: {counts['passed']}",
            f"Failed: {failed}",
            f"Pass rate: {rate:.1f}%",
            f"Paths from Gemini: {path_sources['Gemini']}",
            f"Paths from fallback: {path_sources['fallback']}",
            f"Consistency overlap: {consistency_result}",
        ]
    )
    output = "\n".join(lines)
    _write_report(command, output)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
