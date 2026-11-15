"""Shared orchestration for the TechRoute CLI and web app."""

import csv
import logging
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from typing import Dict, List, Optional, Tuple, TypedDict

from src.path_generator import (
    FALLBACK_SOURCE,
    generate_learning_path,
    validate_profile,
)
from src.recommender import load_opportunities, recommend_opportunities

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATASET_PATH = PROJECT_ROOT / "data" / "opportunities.csv"

Profile = Dict[str, object]
Opportunity = Dict[str, object]
Recommendation = Tuple[Opportunity, float, str]


class PipelineValidationError(ValueError):
    """A profile did not pass the shared input validation."""


class PipelineResult(TypedDict):
    recommendations: List[Recommendation]
    learning_path: Dict[str, object]
    source_label: str
    fallback_reason: Optional[str]


def run_pipeline(
    profile: Profile,
    offline: bool = False,
    opportunities: Optional[List[Opportunity]] = None,
    dataset_path: Optional[Path] = None,
) -> PipelineResult:
    """Load, validate, rank, and generate a path using the existing pipeline."""
    logger = logging.getLogger("techroute")
    if opportunities is None:
        try:
            with redirect_stdout(StringIO()):
                opportunities = load_opportunities(
                    str(dataset_path or DATASET_PATH)
                )
        except (OSError, UnicodeError, csv.Error, ValueError) as error:
            logger.error("dataset_load_failed reason=%s", type(error).__name__)
            raise
    logger.info("dataset_loaded row_count=%d", len(opportunities))

    try:
        safe_profile = validate_profile(profile)
    except ValueError as error:
        logger.warning("profile_validation_failed reason=%s", error)
        raise PipelineValidationError(str(error)) from error
    logger.info(
        "profile_validated target_track=%s",
        safe_profile["target_track"] or "unspecified",
    )

    recommendations = recommend_opportunities(
        safe_profile, opportunities, k=5
    )
    learning_path = generate_learning_path(
        safe_profile,
        opportunities,
        offline=offline,
    )

    source_label = str(learning_path["source"])
    fallback_reason = None
    reason_prefix = f"{FALLBACK_SOURCE} (reason: "
    if source_label.startswith(reason_prefix) and source_label.endswith(")"):
        fallback_reason = source_label[len(reason_prefix):-1]

    return {
        "recommendations": recommendations,
        "learning_path": learning_path,
        "source_label": source_label,
        "fallback_reason": fallback_reason,
    }
