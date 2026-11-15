"""Command-line runner for the TechRoute Recommender."""

import argparse
import csv
import logging
import sys
from pathlib import Path
from typing import List, Optional
from unittest.mock import patch

from src.logging_config import configure_logging
from src.path_generator import (
    DEFAULT_MODEL,
    FALLBACK_SOURCE,
    generate_learning_path,
    validate_profile,
)
from src.profiles import DEFAULT_PROFILE_NAME, PROFILE_PRESETS
from src.recommender import load_opportunities, recommend_opportunities

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

    try:
        opportunities = load_opportunities(str(DATASET_PATH))
    except (OSError, UnicodeError, csv.Error, ValueError) as error:
        reason = type(error).__name__
        logger.error("dataset_load_failed reason=%s", reason)
        print(
            f"Error: unable to load data/opportunities.csv ({reason}).",
            file=sys.stderr,
        )
        return 1
    logger.info("dataset_loaded row_count=%d", len(opportunities))

    try:
        user_prefs = validate_profile(PROFILE_PRESETS[args.profile])
    except ValueError as error:
        logger.warning("profile_validation_failed reason=%s", error)
        print(f"Error: invalid profile: {error}", file=sys.stderr)
        return 1
    logger.info(
        "profile_validated target_track=%s",
        user_prefs["target_track"] or "unspecified",
    )

    recommendations = recommend_opportunities(user_prefs, opportunities, k=5)

    print("\nTop opportunities:\n")
    for opportunity, score, explanation in recommendations:
        print(f"{opportunity['title']} - Score: {score:.2f}")
        print(f"Because: {explanation}")
        print()

    if args.offline:
        print(
            "Privacy notice: only learning preferences (no personal data) are "
            "used; offline mode sends no data to Gemini."
        )
        with patch(
            "src.path_generator._load_gemini_config",
            return_value=(None, DEFAULT_MODEL),
        ):
            learning_path = generate_learning_path(user_prefs, opportunities)
        learning_path["source"] = f"{FALLBACK_SOURCE} (reason: offline mode)"
    else:
        print(
            "Privacy notice: only learning preferences (no personal data) and "
            "retrieved opportunity details are sent to Gemini."
        )
        learning_path = generate_learning_path(user_prefs, opportunities)

    print(f"\nGenerated learning path - {learning_path['source']}:\n")
    for step in learning_path["steps"]:
        print(f"{step['step_number']}. {step['stage']}: {step['goal']}")
        if step["opportunity_titles"]:
            print(f"   Opportunities: {', '.join(step['opportunity_titles'])}")
        print(f"   Why: {step['why']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
