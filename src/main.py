"""Command-line runner for the TechRoute Recommender."""

import argparse
import csv
import logging
import sys
from pathlib import Path
from typing import List, Optional

from src.logging_config import configure_logging
from src.path_generator import format_agent_trace
from src.pipeline import PipelineValidationError, run_pipeline
from src.profiles import DEFAULT_PROFILE_NAME, PROFILE_PRESETS

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATASET_PATH = PROJECT_ROOT / "data" / "opportunities.csv"


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--profile",
        default=DEFAULT_PROFILE_NAME,
        metavar="NAME",
        help="Choose a preset learning profile.",
    )
    parser.add_argument(
        "--offline",
        action="store_true",
        help="Use the rule-based path without calling Gemini.",
    )
    parser.add_argument(
        "--list-profiles",
        action="store_true",
        help="Print available preset profile names and exit.",
    )
    parser.add_argument(
        "--trace",
        action="store_true",
        help="Print the learning-path agent trace after the path.",
    )
    args = parser.parse_args(argv)

    if args.list_profiles:
        print("\n".join(PROFILE_PRESETS))
        return 0
    if args.profile not in PROFILE_PRESETS:
        valid_names = ", ".join(PROFILE_PRESETS)
        print(
            f"Error: unknown profile '{args.profile}'. "
            f"Valid profile names: {valid_names}",
            file=sys.stderr,
        )
        return 2

    logger = configure_logging()
    logger.info("app_start")

    print("Loading opportunities from data/opportunities.csv...")
    try:
        result = run_pipeline(
            PROFILE_PRESETS[args.profile],
            offline=args.offline,
            dataset_path=DATASET_PATH,
        )
    except PipelineValidationError as error:
        print(f"Error: invalid profile: {error}", file=sys.stderr)
        return 1
    except (OSError, UnicodeError, csv.Error, ValueError) as error:
        reason = type(error).__name__
        print(
            f"Error: unable to load data/opportunities.csv ({reason}).",
            file=sys.stderr,
        )
        return 1

    print("\nTop opportunities:\n")
    for opportunity, score, explanation in result["recommendations"]:
        print(f"{opportunity['title']} - Score: {score:.2f}")
        print(f"Because: {explanation}")
        print()

    if args.offline:
        print(
            "Privacy notice: only learning preferences (no personal data) are "
            "used; offline mode sends no data to Gemini."
        )
    else:
        print(
            "Privacy notice: only learning preferences (no personal data) and "
            "retrieved opportunity details are sent to Gemini."
        )

    learning_path = result["learning_path"]
    print(f"\nGenerated learning path - {result['source_label']}:\n")
    for step in learning_path["steps"]:
        print(f"{step['step_number']}. {step['stage']}: {step['goal']}")
        if step["opportunity_titles"]:
            print(f"   Opportunities: {', '.join(step['opportunity_titles'])}")
        print(f"   Why: {step['why']}")
    if args.trace:
        print("\nAgent trace:")
        for line in format_agent_trace(learning_path.get("trace", [])):
            print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
