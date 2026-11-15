from pathlib import Path

from src.recommender import (
    Opportunity,
    Recommender,
    UserProfile,
    load_opportunities,
    recommend_opportunities,
    score_opportunity,
)


def make_small_recommender() -> Recommender:
    opportunities = [
        Opportunity(
            id=1,
            title="Python Backend Course",
            provider="Test Provider",
            category="course",
            career_track="software_engineering",
            format="self_paced",
            difficulty=0.2,
            hours_required=10,
            cost_type="free",
            cost_usd=0,
            remote=True,
            career_value=0.5,
            skills="python;apis",
            eligibility=None,
            leads_to="Software engineering roles",
            description="Learn backend development with Python.",
            url="https://example.com/python",
            last_verified=None,
        ),
        Opportunity(
            id=2,
            title="Linux Security Lab",
            provider="Test Provider",
            category="project",
            career_track="cybersecurity",
            format="project_based",
            difficulty=0.4,
            hours_required=10,
            cost_type="free",
            cost_usd=0,
            remote=True,
            career_value=0.5,
            skills="linux;security_fundamentals;home_lab",
            eligibility=None,
            leads_to="Security analyst skills",
            description="Practice security skills in a small lab.",
            url="https://example.com/security",
            last_verified=None,
        ),
    ]
    return Recommender(opportunities)


def test_recommend_returns_opportunities_sorted_by_score():
    user = UserProfile(
        career_track="software_engineering",
        preferred_format="self_paced",
        skill_level=0.2,
        max_hours=10,
        remote=True,
        interests=["python"],
    )
    recommender = make_small_recommender()
    results = recommender.recommend(user, k=2)

    assert len(results) == 2
    assert results[0].career_track == "software_engineering"
    assert results[0].title == "Python Backend Course"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(career_track="software_engineering")
    recommender = make_small_recommender()

    explanation = recommender.explain_recommendation(
        user, recommender.opportunities[0]
    )
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


def test_opportunity_score_uses_techroute_preferences():
    recommender = make_small_recommender()
    opportunity = recommender.opportunities[0]
    user_prefs = {
        "career_track": "software_engineering",
        "format": "self_paced",
        "skill_level": 0.2,
        "max_hours": 10,
        "remote": True,
        "interests": ["python"],
    }

    score, _ = score_opportunity(user_prefs, opportunity.__dict__)

    assert score == 6.5


def test_functional_api_returns_scored_opportunities():
    recommender = make_small_recommender()
    results = recommend_opportunities(
        {"career_track": "software_engineering"},
        [opportunity.__dict__ for opportunity in recommender.opportunities],
        k=1,
    )

    assert len(results) == 1
    assert results[0][0]["title"] == "Python Backend Course"
    assert isinstance(results[0][1], float)
    assert results[0][2]


def test_loader_parses_opportunities_csv_schema():
    csv_path = Path(__file__).resolve().parents[1] / "data" / "opportunities.csv"
    opportunities = load_opportunities(str(csv_path))

    assert len(opportunities) == 87
    first = opportunities[0]
    assert first["id"] == 1
    assert first["career_track"] == "it_support"
    assert first["remote"] is True
    assert first["format"] is None
    assert first["hours_required"] is None
    assert first["last_verified"] is None
