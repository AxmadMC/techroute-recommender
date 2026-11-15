import pytest

from scripts.evaluate_reliability import (
    PROFILES,
    check_apply_contains_retrieved_internship_job,
)
from src.profiles import EVALUATION_PROFILE_NAMES, PROFILE_LABELS, PROFILE_PRESETS


def test_evaluator_includes_every_preset():
    assert len(PROFILES) == 6
    assert PROFILES == [
        (PROFILE_LABELS[name], PROFILE_PRESETS[name])
        for name in EVALUATION_PROFILE_NAMES
    ]


@pytest.mark.parametrize("opportunity_type", ["internship", "job"])
def test_apply_check_requires_retrieved_internship_or_job(opportunity_type):
    retrieved = [{"title": "Tech opportunity", "type": opportunity_type}]
    path_without_apply_item = {
        "steps": [
            {"stage": "Apply", "opportunity_titles": []},
        ]
    }
    path_with_apply_item = {
        "steps": [
            {"stage": "Apply", "opportunity_titles": ["Tech opportunity"]},
        ]
    }

    assert not check_apply_contains_retrieved_internship_job(
        path_without_apply_item, retrieved
    )[0]
    assert check_apply_contains_retrieved_internship_job(
        path_with_apply_item, retrieved
    )[0]


def test_apply_check_is_not_applicable_without_retrieved_internships_or_jobs():
    passed, detail = check_apply_contains_retrieved_internship_job(
        {"steps": [{"stage": "Apply", "opportunity_titles": []}]},
        [{"title": "Learning course", "type": "course"}],
    )

    assert passed
    assert "not applicable" in detail
