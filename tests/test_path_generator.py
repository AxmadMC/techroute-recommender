import json
import logging
import secrets

import pytest

from src.path_generator import (
    FALLBACK_SOURCE,
    GEMINI_SOURCE,
    generate_learning_path,
    validate_profile,
)
from src.logging_config import configure_logging


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
        },
        {
            "id": 2,
            "title": "Build a Small API",
            "provider": "Example Projects",
            "category": "project",
            "career_track": "software_engineering",
            "format": "project_based",
            "difficulty": 0.3,
            "hours_required": 8.0,
            "cost_type": "free",
            "cost_usd": 0.0,
            "remote": True,
            "career_value": 0.5,
            "skills": "python;apis",
            "eligibility": "",
            "url": "https://example.test/api",
        },
        {
            "id": 3,
            "title": "Example Software Internship",
            "provider": "Example Employer",
            "category": "internship",
            "career_track": "software_engineering",
            "format": "mentored",
            "difficulty": 0.4,
            "hours_required": None,
            "cost_type": "free",
            "cost_usd": 0.0,
            "remote": True,
            "career_value": 0.7,
            "skills": "programming;git",
            "eligibility": "",
            "url": "https://example.test/internship",
        },
        {
            "id": 4,
            "title": "Home Lab: Local Environment",
            "provider": "Example Labs",
            "category": "project",
            "career_track": "software_engineering",
            "format": "project_based",
            "difficulty": 0.25,
            "hours_required": 4.0,
            "cost_type": "free",
            "cost_usd": 0.0,
            "remote": True,
            "career_value": 0.5,
            "skills": "home_lab;virtualization",
            "eligibility": "",
            "url": "https://example.test/lab",
        },
    ]


def make_profile(**extra):
    profile = {
        "target_track": "software_engineering",
        "preferred_format": "self_paced",
        "skill_level": 0.3,
        "prefers_free": True,
        "needs_remote": True,
        "max_hours": 10,
        "interests": ["python"],
    }
    profile.update(extra)
    return profile


def make_valid_response():
    return json.dumps(
        [
            {
                "step_number": 1,
                "stage": "Foundations",
                "goal": "Learn programming basics.",
                "opportunity_titles": ["Intro to Python"],
                "why": "It is an introductory retrieved course.",
            },
            {
                "step_number": 2,
                "stage": "Build Skills",
                "goal": "Practice with a hands-on environment.",
                "opportunity_titles": ["Home Lab: Local Environment"],
                "why": "It offers a practical learning environment.",
            },
            {
                "step_number": 3,
                "stage": "Prove Skills",
                "goal": "Practice building software.",
                "opportunity_titles": ["Build a Small API"],
                "why": "It offers hands-on practice.",
            },
            {
                "step_number": 4,
                "stage": "Apply",
                "goal": "Explore the retrieved internship.",
                "opportunity_titles": ["Example Software Internship"],
                "why": "It is available in the retrieved dataset.",
            },
        ]
    )


def make_plan_response(opportunities=None):
    opportunities = opportunities or make_opportunities()
    assignments = []
    for opportunity in opportunities:
        category = opportunity["category"]
        if category in {"internship", "job"}:
            stage = "Apply"
        elif category == "project" and opportunity["title"] != "Build a Small API":
            stage = "Build Skills"
        elif category in {"project", "certification", "volunteer"}:
            stage = "Prove Skills"
        else:
            stage = "Foundations"
        assignments.append(
            {
                "title": opportunity["title"],
                "stage": stage,
                "reason": f"Matches the {stage.lower()} learning goal.",
            }
        )
    return json.dumps({"assignments": assignments})


def make_agent_call(*responses):
    remaining = list(responses)
    calls = []

    def fake_gemini_call(prompt, model):
        assert remaining, "unexpected Gemini call"
        calls.append(prompt)
        return remaining.pop(0)

    fake_gemini_call.calls = calls
    return fake_gemini_call


def test_made_up_title_is_repaired_on_attempt_two(monkeypatch):
    monkeypatch.setattr(
        "src.path_generator._load_gemini_config",
        lambda: (None, "gemini-test"),
    )
    invented = json.loads(make_valid_response())
    invented[0]["opportunity_titles"] = ["Invented Course"]
    agent_call = make_agent_call(
        make_plan_response(),
        json.dumps(invented),
        make_valid_response(),
    )

    result = generate_learning_path(
        make_profile(),
        make_opportunities(),
        gemini_call=agent_call,
    )

    assert result["source"] == (
        "Source: Gemini (verified after 1 self-correction)"
    )
    assert result["repair_attempts"] == 1
    assert len(agent_call.calls) == 3
    assert "AI output referenced an opportunity not in the retrieved data" in (
        agent_call.calls[2]
    )
    assert json.dumps(invented) in agent_call.calls[2]
    assert result["trace"][-1]["step_name"] == "DECIDE"
    assert result["trace"][-1]["decision"] == "accepted"
    assert result["trace"][-1]["attempt_number"] == 2
    assert any(
        entry["step_name"] == "SELF-CORRECT"
        and "AI output referenced an opportunity not in the retrieved data"
        in entry["verifier_errors"]
        for entry in result["trace"]
    )
    retrieved_titles = {item["title"] for item in make_opportunities()}
    assert all(
        title in retrieved_titles
        for step in result["steps"]
        for title in step["opportunity_titles"]
    )


def test_failing_all_repair_attempts_uses_required_fallback_reason(monkeypatch):
    monkeypatch.setattr(
        "src.path_generator._load_gemini_config",
        lambda: (None, "gemini-test"),
    )

    result = generate_learning_path(
        make_profile(),
        make_opportunities(),
        gemini_call=make_agent_call(
            make_plan_response(),
            "not valid JSON",
            "not valid JSON",
            "not valid JSON",
        ),
    )

    assert result["source"] == (
        f"{FALLBACK_SOURCE} "
        "(reason: AI output failed verification after 2 repair attempts)"
    )
    assert result["repair_attempts"] == 2


def test_missing_api_key_uses_fallback(monkeypatch):
    monkeypatch.setattr(
        "src.path_generator._load_gemini_config",
        lambda: (None, "gemini-test"),
    )

    result = generate_learning_path(make_profile(), make_opportunities())

    assert result["source"] == f"{FALLBACK_SOURCE} (reason: no API key)"


def test_gemini_api_error_uses_fallback_reason(monkeypatch):
    monkeypatch.setattr(
        "src.path_generator._load_gemini_config",
        lambda: (None, "gemini-test"),
    )

    def failed_call(prompt, model):
        raise RuntimeError("private API failure details")

    result = generate_learning_path(
        make_profile(),
        make_opportunities(),
        gemini_call=failed_call,
    )

    assert result["source"] == f"{FALLBACK_SOURCE} (reason: Gemini API error)"


def test_valid_retrieved_titles_are_accepted(monkeypatch):
    monkeypatch.setattr(
        "src.path_generator._load_gemini_config",
        lambda: (None, "gemini-test"),
    )

    result = generate_learning_path(
        make_profile(),
        make_opportunities(),
        gemini_call=make_agent_call(make_plan_response(), make_valid_response()),
    )

    assert result["source"] == GEMINI_SOURCE
    assert result["steps"][0]["opportunity_titles"] == ["Intro to Python"]
    assert result["repair_attempts"] == 0


def test_unexpected_profile_keys_are_dropped_before_prompt(monkeypatch):
    monkeypatch.setattr(
        "src.path_generator._load_gemini_config",
        lambda: (None, "gemini-test"),
    )
    captured = {}

    def fake_gemini_call(prompt, model):
        captured.setdefault("prompts", []).append(prompt)
        if len(captured["prompts"]) == 1:
            return make_plan_response()
        return make_valid_response()

    profile = make_profile(
        name="UNEXPECTED_NAME",
        email="UNEXPECTED_EMAIL",
        location="UNEXPECTED_LOCATION",
    )
    result = generate_learning_path(
        profile,
        make_opportunities(),
        gemini_call=fake_gemini_call,
    )

    assert result["source"] == GEMINI_SOURCE
    prompts = "\n".join(captured["prompts"])
    assert "UNEXPECTED_NAME" not in prompts
    assert "UNEXPECTED_EMAIL" not in prompts
    assert "UNEXPECTED_LOCATION" not in prompts
    assert "target_track" in prompts
    assert "Intro to Python" in prompts


def test_four_opportunities_in_a_stage_trigger_repair(monkeypatch):
    monkeypatch.setattr(
        "src.path_generator._load_gemini_config",
        lambda: (None, "gemini-test"),
    )
    oversized = json.loads(make_valid_response())
    oversized[0]["opportunity_titles"] = [
        "Intro to Python",
        "Build a Small API",
        "Home Lab: Local Environment",
        "Intro to Python",
    ]
    oversized[1]["opportunity_titles"] = []
    oversized[2]["opportunity_titles"] = []

    result = generate_learning_path(
        make_profile(),
        make_opportunities(),
        gemini_call=make_agent_call(
            make_plan_response(),
            json.dumps(oversized),
            make_valid_response(),
        ),
    )

    assert result["source"] == (
        "Source: Gemini (verified after 1 self-correction)"
    )
    assert any(
        "Foundations has 4 items; maximum is 3" in entry["verifier_errors"]
        for entry in result["trace"]
    )


def test_duplicate_title_across_stages_triggers_repair(monkeypatch):
    monkeypatch.setattr(
        "src.path_generator._load_gemini_config",
        lambda: (None, "gemini-test"),
    )
    duplicate = json.loads(make_valid_response())
    duplicate[1]["opportunity_titles"] = ["Intro to Python"]

    result = generate_learning_path(
        make_profile(),
        make_opportunities(),
        gemini_call=make_agent_call(
            make_plan_response(),
            json.dumps(duplicate),
            make_valid_response(),
        ),
    )

    assert result["source"] == (
        "Source: Gemini (verified after 1 self-correction)"
    )
    assert any(
        "Intro to Python appears in both Foundations and Build Skills"
        in entry["verifier_errors"]
        for entry in result["trace"]
    )


def test_fallback_apply_step_says_when_no_internships_exist(monkeypatch):
    monkeypatch.setattr(
        "src.path_generator._load_gemini_config",
        lambda: (None, "gemini-test"),
    )
    opportunities = make_opportunities()[:2]

    result = generate_learning_path(make_profile(), opportunities)

    apply_step = next(step for step in result["steps"] if step["stage"] == "Apply")
    assert "no internship or job opportunities are in the dataset yet" in apply_step[
        "goal"
    ].lower()
    assert apply_step["opportunity_titles"] == []


def test_fallback_groups_projects_and_internships_by_stage(monkeypatch):
    monkeypatch.setattr(
        "src.path_generator._load_gemini_config",
        lambda: (None, "gemini-test"),
    )

    result = generate_learning_path(make_profile(), make_opportunities())

    stages = {step["stage"]: step["opportunity_titles"] for step in result["steps"]}
    assert stages["Foundations"] == ["Intro to Python"]
    assert stages["Build Skills"] == ["Home Lab: Local Environment"]
    assert stages["Prove Skills"] == ["Build a Small API"]
    assert stages["Apply"] == ["Example Software Internship"]


@pytest.mark.parametrize(
    ("changes", "message"),
    [
        ({"target_track": "unknown_track"}, "target_track"),
        ({"skill_level": -0.1}, "skill_level"),
        ({"skill_level": 1.1}, "skill_level"),
        ({"max_hours": -1}, "max_hours"),
    ],
)
def test_invalid_profile_values_raise_validation_errors(changes, message):
    profile = make_profile(**changes)

    with pytest.raises(ValueError, match=message):
        validate_profile(profile)


def test_api_key_and_full_profile_are_never_logged(monkeypatch, tmp_path):
    secret_key = secrets.token_urlsafe(24)
    log_path = tmp_path / "logs" / "techroute.log"
    logger = configure_logging(log_path)
    monkeypatch.setattr(
        "src.path_generator._load_gemini_config",
        lambda: (secret_key, "gemini-test"),
    )
    private_marker = "profile-private-marker"
    profile = make_profile(private_interest=private_marker)

    result = generate_learning_path(
        profile,
        make_opportunities(),
        gemini_call=make_agent_call(make_plan_response(), make_valid_response()),
    )
    for handler in logger.handlers:
        handler.flush()
        handler.close()
        logger.removeHandler(handler)

    log_text = log_path.read_text(encoding="utf-8")
    assert result["source"] == GEMINI_SOURCE
    assert secret_key not in log_text
    assert secret_key not in json.dumps(result["trace"])
    assert repr(profile) not in log_text
    assert private_marker not in log_text
    assert private_marker not in json.dumps(result["trace"])
    assert "target_track=software_engineering" in log_text
    assert "reason=verified path" in log_text
