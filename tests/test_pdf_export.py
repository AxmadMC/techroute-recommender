from pathlib import Path

import pytest

from src.pdf_export import _source_text, build_pdf


def sample_profile():
    return {
        "target_track": "software_engineering",
        "preferred_format": "self_paced",
        "skill_level": 0.3,
        "prefers_free": True,
        "needs_remote": True,
        "max_hours": 10,
        "interests": ["python"],
        "api_key": "test-secret-must-not-be-included",
    }


def sample_opportunity():
    return {
        "id": 1,
        "title": "Intro to Python",
        "provider": "Example Learning",
        "category": "course",
        "career_track": "software_engineering",
        "format": "self_paced",
        "difficulty": 0.2,
        "hours_required": 5.0,
        "cost_type": "free",
        "cost_usd": 0.0,
        "remote": True,
        "career_value": 0.5,
        "skills": "python",
        "eligibility": "",
        "url": "https://example.test/python",
    }


def sample_path():
    return {
        "steps": [
            {
                "step_number": 1,
                "stage": "Foundations",
                "goal": "Learn programming basics.",
                "opportunity_titles": ["Intro to Python"],
                "why": "It is an introductory course.",
            },
            {
                "step_number": 2,
                "stage": "Build Skills",
                "goal": "Practice programming.",
                "opportunity_titles": [],
                "why": "Practice helps build confidence.",
            },
            {
                "step_number": 3,
                "stage": "Prove Skills",
                "goal": "Demonstrate your skills.",
                "opportunity_titles": [],
                "why": "Projects can show what you learned.",
            },
            {
                "step_number": 4,
                "stage": "Apply",
                "goal": "No internship or job opportunities are in the dataset yet.",
                "opportunity_titles": [],
                "why": "No matching internship or job rows were retrieved.",
            },
        ]
    }


def test_pdf_source_label_preserves_self_correction_count():
    assert _source_text(
        "Source: Gemini (verified after 1 self-correction)",
        None,
    ) == "AI-generated (verified after 1 self-correction)"


@pytest.mark.parametrize(
    ("source_label", "fallback_reason"),
    [
        ("Source: Gemini (verified against retrieved data)", None),
        ("Source: rule-based fallback (reason: offline mode)", "offline mode"),
    ],
)
def test_build_pdf_returns_memory_pdf_without_api_key(
    tmp_path, source_label, fallback_reason
):
    opportunity = sample_opportunity()
    pdf = build_pdf(
        sample_profile(),
        [(opportunity, 5.5, "career track match (+2.00); difficulty fit (+1.00)")],
        sample_path(),
        source_label,
        fallback_reason,
        opportunities=[opportunity],
    )

    assert isinstance(pdf, bytes)
    assert pdf.startswith(b"%PDF-")
    assert b"test-secret-must-not-be-included" not in pdf
    assert b"My TechRoute Learning Path" in pdf
    assert b"https://example.test/python" in pdf
    assert list(Path(tmp_path).iterdir()) == []
