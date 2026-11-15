import json
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from src.path_generator import FALLBACK_SOURCE, GEMINI_SOURCE
from src.pipeline import PipelineValidationError, run_pipeline


def make_profile(**updates):
    profile = {
        "target_track": "software_engineering",
        "preferred_format": "self_paced",
        "skill_level": 0.3,
        "prefers_free": True,
        "needs_remote": True,
        "max_hours": 10,
        "interests": ["python"],
    }
    profile.update(updates)
    return profile


def make_opportunities():
    return [
        {
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
            "skills": "python;programming",
            "eligibility": "",
            "url": "https://example.test/python",
        }
    ]


def make_gemini_response():
    return json.dumps(
        [
            {
                "step_number": 1,
                "stage": "Foundations",
                "goal": "Learn core programming concepts.",
                "opportunity_titles": ["Intro to Python"],
                "why": "The retrieved course introduces programming.",
            },
            {
                "step_number": 2,
                "stage": "Build Skills",
                "goal": "Practice programming.",
                "opportunity_titles": [],
                "why": "Continue with structured practice.",
            },
            {
                "step_number": 3,
                "stage": "Prove Skills",
                "goal": "Demonstrate practical skills.",
                "opportunity_titles": [],
                "why": "Build evidence of what you learned.",
            },
            {
                "step_number": 4,
                "stage": "Apply",
                "goal": "No internship or job opportunities are in the dataset yet.",
                "opportunity_titles": [],
                "why": "There are no internship or job opportunities in the dataset.",
            },
        ]
    )


def make_plan_response():
    return json.dumps(
        {
            "assignments": [
                {
                    "title": "Intro to Python",
                    "stage": "Foundations",
                    "reason": "It introduces the target skill.",
                }
            ]
        }
    )


def test_offline_pipeline_uses_fallback_without_calling_gemini(monkeypatch):
    monkeypatch.setattr(
        "src.path_generator._call_gemini",
        lambda *args: pytest.fail("offline pipeline must not call Gemini"),
    )
    monkeypatch.setattr(
        "src.path_generator._load_gemini_config",
        lambda: pytest.fail("offline pipeline must not load Gemini configuration"),
    )

    result = run_pipeline(
        make_profile(),
        offline=True,
        opportunities=make_opportunities(),
    )

    assert result["source_label"] == f"{FALLBACK_SOURCE} (reason: offline mode)"
    assert result["fallback_reason"] == "offline mode"
    assert result["recommendations"][0][0]["title"] == "Intro to Python"
    trace = result["learning_path"]["trace"]
    assert [entry["step_name"] for entry in trace] == ["PLAN", "DECIDE"]
    assert trace[0]["decision"] == "skipped"


def test_pipeline_uses_mocked_gemini_response(monkeypatch):
    calls = []
    monkeypatch.setattr(
        "src.path_generator._load_gemini_config",
        lambda: ("test-only-key", "gemini-test"),
    )

    def fake_gemini(prompt, api_key, model):
        calls.append((prompt, model))
        return make_plan_response() if len(calls) == 1 else make_gemini_response()

    monkeypatch.setattr("src.path_generator._call_gemini", fake_gemini)
    result = run_pipeline(
        make_profile(),
        opportunities=make_opportunities(),
    )

    assert result["source_label"] == GEMINI_SOURCE
    assert result["fallback_reason"] is None
    assert len(calls) == 2
    assert all("test-only-key" not in prompt for prompt, _ in calls)


def test_pipeline_rejects_invalid_profile():
    with pytest.raises(PipelineValidationError, match="supported career track"):
        run_pipeline(
            make_profile(target_track="not_a_track"),
            offline=True,
            opportunities=make_opportunities(),
        )


def test_streamlit_app_runs_an_offline_search(monkeypatch):
    monkeypatch.setattr(
        "src.path_generator._call_gemini",
        lambda *args: pytest.fail("offline AppTest must not call Gemini"),
    )
    app_path = Path(__file__).resolve().parents[1] / "app.py"
    app = AppTest.from_file(str(app_path)).run()

    assert not app.exception
    app.toggle(key="use_ai").set_value(False)
    app.button[0].click().run()

    assert not app.exception
    assert any(
        "Rule-based fallback" in markdown.value for markdown in app.markdown
    )
    assert len(app.download_button) == 1
    assert app.download_button[0].label == "Download my route (PDF)"
