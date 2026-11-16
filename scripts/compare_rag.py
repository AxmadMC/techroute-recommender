"""Compare opportunity-only retrieval with track-guide context."""

from contextlib import redirect_stdout
from datetime import date
from io import StringIO
import logging
from pathlib import Path
import re
import sys
import time

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src import main as cli
from src.guide_retriever import core_skill_terms
from src.path_generator import DEFAULT_MODEL, _load_gemini_config
from src.profiles import PROFILE_PRESETS

PROFILE_NAMES = (
    "cloud_career_changer",
    "networking_student",
    "ai_engineering_student",
)
COMMAND = "python scripts/compare_rag.py"
OUTPUT_PATH = PROJECT_ROOT / "assets" / "rag_comparison.md"
CALL_PAUSE_SECONDS = 1.0
WORD_PATTERN = re.compile(r"\b[\w'-]+\b")


def _quiet_logger():
    logger = logging.getLogger("techroute")
    logger.addHandler(logging.NullHandler())
    logger.propagate = False
    return logger


def _run_cli(profile_name: str, no_guides: bool):
    results = []
    original_pipeline = cli.run_pipeline
    original_configure_logging = cli.configure_logging

    def capture_pipeline(
        profile,
        offline=False,
        dataset_path=None,
        use_guides=True,
    ):
        result = original_pipeline(
            profile,
            offline=offline,
            dataset_path=dataset_path,
            use_guides=use_guides,
        )
        results.append(result)
        return result

    cli.run_pipeline = capture_pipeline
    cli.configure_logging = _quiet_logger
    arguments = ["--profile", profile_name]
    if no_guides:
        arguments.append("--no-guides")
    try:
        with redirect_stdout(StringIO()):
            exit_code = cli.main(arguments)
    finally:
        cli.run_pipeline = original_pipeline
        cli.configure_logging = original_configure_logging
    if exit_code != 0 or len(results) != 1:
        raise RuntimeError(f"CLI comparison run failed for {profile_name}.")
    return results[0]


def _path_text(result) -> str:
    path = result["learning_path"]
    lines = [str(result["source_label"])]
    for step in path["steps"]:
        lines.append(f"{step['step_number']}. {step['stage']}: {step['goal']}")
        titles = step["opportunity_titles"]
        lines.append(
            "   Opportunities: " + (", ".join(titles) if titles else "none")
        )
        lines.append(f"   Why: {step['why']}")
    return "\n".join(lines)


def _metrics(result, track: str):
    path = result["learning_path"]
    terms = core_skill_terms(track)
    explanation_text = " ".join(
        f"{step['goal']} {step['why']}" for step in path["steps"]
    ).casefold()
    matched_terms = [
        term for term in terms if term.casefold() in explanation_text
    ]
    why_lengths = [
        len(WORD_PATTERN.findall(step["why"]))
        for step in path["steps"]
    ]
    average_why_length = (
        sum(why_lengths) / len(why_lengths) if why_lengths else 0.0
    )
    verified = any(
        entry.get("step_name") == "VERIFY"
        and entry.get("decision") == "accepted"
        for entry in path.get("trace", [])
    )
    return {
        "matched_skill_terms": len(matched_terms),
        "total_skill_terms": len(terms),
        "average_why_words": average_why_length,
        "verified": verified,
        "repairs": path.get("repair_attempts", 0),
    }


def _verification_label(metrics) -> str:
    return "Pass" if metrics["verified"] else "Fail"


def main() -> int:
    api_key, model = _load_gemini_config()
    if not api_key:
        raise SystemExit(
            "GEMINI_API_KEY must be configured to create a real RAG comparison."
        )
    del api_key
    model = model or DEFAULT_MODEL

    runs = {}
    call_count = 0
    for profile_name in PROFILE_NAMES:
        runs[profile_name] = {}
        for variant, no_guides in (("before", True), ("after", False)):
            if call_count:
                time.sleep(CALL_PAUSE_SECONDS)
            runs[profile_name][variant] = _run_cli(profile_name, no_guides)
            call_count += 1

    report_lines = [
        "# RAG Enhancement Comparison",
        "",
        f"- Command: `{COMMAND}`",
        f"- Date: {date.today().isoformat()}",
        f"- Model: `{model}`",
        "",
        "The before run invokes the CLI with `--no-guides`; the after run uses "
        "the track guide. Skill-term cells show matched/available core-skill "
        "terms and the average Why length in words.",
        "",
        "| Profile | Before skill terms | After skill terms | Before/after verification | Repairs |",
        "| --- | --- | --- | --- | --- |",
    ]

    metrics_by_profile = {}
    for profile_name in PROFILE_NAMES:
        track = PROFILE_PRESETS[profile_name]["target_track"]
        before_metrics = _metrics(runs[profile_name]["before"], track)
        after_metrics = _metrics(runs[profile_name]["after"], track)
        metrics_by_profile[profile_name] = (before_metrics, after_metrics)
        report_lines.append(
            f"| {profile_name} "
            f"| {before_metrics['matched_skill_terms']}/"
            f"{before_metrics['total_skill_terms']} "
            f"(Why avg {before_metrics['average_why_words']:.1f} words) "
            f"| {after_metrics['matched_skill_terms']}/"
            f"{after_metrics['total_skill_terms']} "
            f"(Why avg {after_metrics['average_why_words']:.1f} words) "
            f"| {_verification_label(before_metrics)} / "
            f"{_verification_label(after_metrics)} "
            f"| {before_metrics['repairs']} / {after_metrics['repairs']} |"
        )

    for profile_name in PROFILE_NAMES:
        for variant, no_guides in (("before", True), ("after", False)):
            run = runs[profile_name][variant]
            command = (
                f"python -m src.main --profile {profile_name} --no-guides"
                if no_guides
                else f"python -m src.main --profile {profile_name}"
            )
            report_lines.extend(
                [
                    "",
                    f"## {profile_name} — {variant}",
                    "",
                    f"Command: `{command}`",
                    "",
                    "```text",
                    _path_text(run),
                    "```",
                ]
            )

    report_lines.extend(["", "Observation:", "", "Limitation:", ""])
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text("\n".join(report_lines), encoding="utf-8")
    print("Wrote real before/after RAG comparison to assets/rag_comparison.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
