"""Run repeatable reliability checks against the TechRoute opportunities dataset."""

from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
import sys
from typing import Callable, Dict, List, Tuple

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.recommender import load_opportunities, recommend_opportunities


Profile = Dict[str, object]
Recommendation = Tuple[Dict, float, str]
Check = Callable[[Profile, List[Recommendation], str], Tuple[bool, str]]


PROFILES: List[Tuple[str, Profile]] = [
    (
        "IT Support beginner",
        {
            "target_track": "it_support",
            "preferred_format": "self_paced",
            "skill_level": 0.2,
            "prefers_free": True,
            "needs_remote": True,
            "max_hours": 10,
            "interests": ["hardware", "troubleshooting", "windows"],
        },
    ),
    (
        "Networking student",
        {
            "target_track": "networking",
            "preferred_format": "project_based",
            "skill_level": 0.35,
            "prefers_free": True,
            "needs_remote": True,
            "max_hours": 8,
            "interests": ["networking", "ip_addressing", "packet_tracer"],
        },
    ),
    (
        "Cybersecurity beginner",
        {
            "target_track": "cybersecurity",
            "preferred_format": "self_paced",
            "skill_level": 0.2,
            "prefers_free": True,
            "needs_remote": True,
            "max_hours": 5,
            "interests": ["security_fundamentals", "linux", "networking"],
        },
    ),
    (
        "Cloud career changer",
        {
            "target_track": "cloud_computing",
            "preferred_format": "self_paced",
            "skill_level": 0.3,
            "prefers_free": True,
            "needs_remote": True,
            "max_hours": 10,
            "interests": ["azure", "cloud", "linux"],
        },
    ),
    (
        "AI Engineering student",
        {
            "target_track": "ai_engineering",
            "preferred_format": "project_based",
            "skill_level": 0.35,
            "prefers_free": True,
            "needs_remote": True,
            "max_hours": 12,
            "interests": ["python", "machine_learning", "data_analysis"],
        },
    ),
]


def check_track_relevance(
    profile: Profile, results: List[Recommendation], _: str
) -> Tuple[bool, str]:
    target = profile["target_track"]
    matches = sum(
        opportunity.get("career_track") == target
        for opportunity, _, _ in results
    )
    return matches >= 4, f"{matches}/{len(results)} recommendations match {target}"


def check_remote_guardrail(
    profile: Profile, results: List[Recommendation], _: str
) -> Tuple[bool, str]:
    if profile["needs_remote"] is not True:
        return True, "Remote requirement is not enabled"
    non_remote = [
        opportunity["title"]
        for opportunity, _, _ in results
        if opportunity.get("remote") is not True
    ]
    return not non_remote, (
        "all results are remote"
        if not non_remote
        else f"non-remote results: {', '.join(non_remote)}"
    )


def check_prerequisite_guardrail(
    profile: Profile, results: List[Recommendation], _: str
) -> Tuple[bool, str]:
    if profile["skill_level"] >= 0.5 or not results:
        return True, "no low-skill prerequisite violation at rank #1"
    first = results[0][0]
    tags = set(filter(None, (first.get("eligibility") or "").split(";")))
    has_prerequisite = "prior_experience" in tags
    return not has_prerequisite, (
        f"rank #1: {first['title']}"
        + (
            " requires prior experience"
            if has_prerequisite
            else " has no prior_experience tag"
        )
    )


def check_result_count(
    _: Profile, results: List[Recommendation], recommender_output: str
) -> Tuple[bool, str]:
    if len(results) == 5:
        return True, "returned 5 recommendations"
    has_shortfall_message = "fewer than 5" in recommender_output
    return has_shortfall_message, (
        f"returned {len(results)}; "
        + (
            "recommender printed a clear fewer-than-5 message"
            if has_shortfall_message
            else "no clear fewer-than-5 message was printed"
        )
    )


CHECKS: List[Tuple[str, Check]] = [
    ("Track relevance", check_track_relevance),
    ("Remote guardrail", check_remote_guardrail),
    ("Prerequisite guardrail", check_prerequisite_guardrail),
    ("Result count", check_result_count),
]


def main() -> None:
    opportunities_path = PROJECT_ROOT / "data" / "opportunities.csv"
    opportunities = load_opportunities(str(opportunities_path))
    total_checks = 0
    passed_checks = 0

    for profile_name, profile in PROFILES:
        print(f"\n=== {profile_name} ===")
        print(f"Input profile: {profile}")

        captured = StringIO()
        with redirect_stdout(captured):
            results = recommend_opportunities(profile, opportunities, k=5)
        recommender_output = captured.getvalue()
        if recommender_output:
            print(recommender_output, end="")

        for rank, (opportunity, score, explanation) in enumerate(results, start=1):
            print(
                f"{rank}. {opportunity['title']} | {opportunity['provider']} "
                f"| score={score:.2f}"
            )
            print(f"   {explanation}")

        for check_name, check in CHECKS:
            passed, detail = check(profile, results, recommender_output)
            total_checks += 1
            passed_checks += int(passed)
            status = "PASS" if passed else "FAIL"
            print(f"{status}: {check_name}: {detail}")

    failed_checks = total_checks - passed_checks
    pass_rate = (passed_checks / total_checks * 100) if total_checks else 0.0
    print("\n=== Final summary ===")
    print(f"Total checks: {total_checks}")
    print(f"Passed: {passed_checks}")
    print(f"Failed: {failed_checks}")
    print(f"Pass rate: {pass_rate:.1f}%")


if __name__ == "__main__":
    main()
