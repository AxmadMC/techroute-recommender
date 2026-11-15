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
        target_track="software_engineering",
        preferred_format="self_paced",
        skill_level=0.2,
        prefers_free=True,
        needs_remote=True,
        max_hours=10,
        interests=["python"],
    )
    recommender = make_small_recommender()
    results = recommender.recommend(user, k=2)

    assert len(results) == 2
    assert results[0].career_track == "software_engineering"
    assert results[0].title == "Python Backend Course"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(target_track="software_engineering")
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
        "target_track": "software_engineering",
        "preferred_format": "self_paced",
        "skill_level": 0.2,
        "prefers_free": True,
        "needs_remote": True,
        "max_hours": 10,
        "interests": ["python"],
    }

    score, _ = score_opportunity(user_prefs, opportunity.__dict__)

    assert score == 6.5


def test_functional_api_returns_scored_opportunities():
    recommender = make_small_recommender()
    results = recommend_opportunities(
        {"target_track": "software_engineering"},
        [opportunity.__dict__ for opportunity in recommender.opportunities],
        k=1,
    )

    assert len(results) == 1
    assert results[0][0]["title"] == "Python Backend Course"
    assert isinstance(results[0][1], float)
    assert results[0][2]


def test_recommender_requires_remote_and_reports_shortfall(capsys):
    recommender = make_small_recommender()
    recommender.opportunities[1].remote = False
    user = UserProfile(needs_remote=True)

    results = recommender.recommend(user, k=5)
    explanation = recommender.explain_recommendation(user, results[0])

    assert [opportunity.id for opportunity in results] == [1]
    assert "Remote requirement met" in explanation
    assert "Remote requirement matched 1 opportunities" in capsys.readouterr().out


def test_functional_recommender_requires_remote_and_reports_shortfall(capsys):
    recommender = make_small_recommender()
    opportunities = [
        opportunity.__dict__.copy() for opportunity in recommender.opportunities
    ]
    opportunities[1]["remote"] = False

    results = recommend_opportunities(
        {"needs_remote": True}, opportunities, k=5
    )

    assert [opportunity["id"] for opportunity, _, _ in results] == [1]
    assert "Remote requirement met" in results[0][2]
    assert "Remote requirement matched 1 opportunities" in capsys.readouterr().out


def test_remote_false_keeps_both_and_rewards_nonremote_match(capsys):
    recommender = make_small_recommender()
    opportunities = [
        opportunity.__dict__.copy() for opportunity in recommender.opportunities
    ]
    opportunities[1]["remote"] = False

    results = recommend_opportunities(
        {"needs_remote": False}, opportunities, k=5
    )

    assert len(results) == 2
    assert results[0][0]["id"] == 2
    assert "remote preference match (+0.50)" in results[0][2]
    assert capsys.readouterr().out == ""


def test_prefers_free_controls_free_priority_and_explanation():
    opportunity = make_small_recommender().opportunities[0].__dict__.copy()
    expected_points = {"free": 1.0, "freemium": 0.5, "paid": 0.0}

    for cost_type, points in expected_points.items():
        opportunity["cost_type"] = cost_type
        preferred_score, preferred_reasons = score_opportunity(
            {"prefers_free": True}, opportunity
        )
        ignored_score, ignored_reasons = score_opportunity(
            {"prefers_free": False}, opportunity
        )

        assert preferred_score == points
        assert ignored_score == 0
        assert f"free priority (+{points:.2f})" in preferred_reasons
        assert "Free preference disabled (+0.00)" in ignored_reasons


def test_prior_experience_penalty_applies_only_below_threshold():
    opportunity = make_small_recommender().opportunities[0].__dict__.copy()
    opportunity["eligibility"] = "prior_experience"
    low_skill = {"skill_level": 0.49, "prefers_free": False}
    threshold_skill = {"skill_level": 0.5, "prefers_free": False}

    penalized_score, penalized_reasons = score_opportunity(low_skill, opportunity)
    baseline_score, _ = score_opportunity(
        low_skill, {**opportunity, "eligibility": ""}
    )
    threshold_score, threshold_reasons = score_opportunity(
        threshold_skill, opportunity
    )
    threshold_baseline, _ = score_opportunity(
        threshold_skill, {**opportunity, "eligibility": ""}
    )

    assert penalized_score == baseline_score - 1.0
    assert "Penalty -1.0: requires prior experience" in penalized_reasons
    assert threshold_score == threshold_baseline
    assert "Penalty -1.0: requires prior experience" not in threshold_reasons


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
