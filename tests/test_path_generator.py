import json

from src.path_generator import (
    FALLBACK_SOURCE,
    GEMINI_SOURCE,
    generate_learning_path,
)


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
                "goal": "Practice building software.",
                "opportunity_titles": ["Build a Small API"],
                "why": "It offers hands-on practice.",
            },
            {
                "step_number": 3,
                "stage": "Apply",
                "goal": "Explore the retrieved internship.",
                "opportunity_titles": ["Example Software Internship"],
                "why": "It is available in the retrieved dataset.",
            },
        ]
    )


def test_made_up_title_is_rejected_and_falls_back(monkeypatch):
    monkeypatch.setattr(
        "src.path_generator._load_gemini_config",
        lambda: (None, "gemini-test"),
    )
    invented = json.loads(make_valid_response())
    invented[0]["opportunity_titles"] = ["Invented Course"]

    result = generate_learning_path(
        make_profile(),
        make_opportunities(),
        gemini_call=lambda prompt, model: json.dumps(invented),
    )

    assert result["source"] == FALLBACK_SOURCE
    retrieved_titles = {item["title"] for item in make_opportunities()}
    assert all(
        title in retrieved_titles
        for step in result["steps"]
        for title in step["opportunity_titles"]
    )


def test_invalid_json_falls_back(monkeypatch):
    monkeypatch.setattr(
        "src.path_generator._load_gemini_config",
        lambda: (None, "gemini-test"),
    )

    result = generate_learning_path(
        make_profile(),
        make_opportunities(),
        gemini_call=lambda prompt, model: "not valid JSON",
    )

    assert result["source"] == FALLBACK_SOURCE


def test_missing_api_key_uses_fallback(monkeypatch):
    monkeypatch.setattr(
        "src.path_generator._load_gemini_config",
        lambda: (None, "gemini-test"),
    )

    result = generate_learning_path(make_profile(), make_opportunities())

    assert result["source"] == FALLBACK_SOURCE


def test_valid_retrieved_titles_are_accepted(monkeypatch):
    monkeypatch.setattr(
        "src.path_generator._load_gemini_config",
        lambda: (None, "gemini-test"),
    )

    result = generate_learning_path(
        make_profile(),
        make_opportunities(),
        gemini_call=lambda prompt, model: make_valid_response(),
    )

    assert result["source"] == GEMINI_SOURCE
    assert result["steps"][0]["opportunity_titles"] == ["Intro to Python"]


def test_unexpected_profile_keys_are_dropped_before_prompt(monkeypatch):
    monkeypatch.setattr(
        "src.path_generator._load_gemini_config",
        lambda: (None, "gemini-test"),
    )
    captured = {}

    def fake_gemini_call(prompt, model):
        captured["prompt"] = prompt
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
    assert "UNEXPECTED_NAME" not in captured["prompt"]
    assert "UNEXPECTED_EMAIL" not in captured["prompt"]
    assert "UNEXPECTED_LOCATION" not in captured["prompt"]
    assert "target_track" in captured["prompt"]
    assert "Intro to Python" in captured["prompt"]


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
