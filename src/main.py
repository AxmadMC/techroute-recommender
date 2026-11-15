"""Command-line runner for the TechRoute Recommender."""

import csv
import logging
import sys
from pathlib import Path

from src.logging_config import configure_logging
from src.path_generator import generate_learning_path, validate_profile
from src.recommender import load_opportunities, recommend_opportunities

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATASET_PATH = PROJECT_ROOT / "data" / "opportunities.csv"
DEFAULT_PROFILE = {
    "target_track": "software_engineering",
    "preferred_format": "self_paced",
    "skill_level": 0.3,
    "prefers_free": True,
    "needs_remote": True,
    "max_hours": 20,
    "interests": ["python", "git"],
}


def main() -> int:
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
        user_prefs = validate_profile(DEFAULT_PROFILE)
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
