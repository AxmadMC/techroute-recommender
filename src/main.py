"""Command-line runner for the TechRoute Recommender."""

from src.recommender import load_opportunities, recommend_opportunities


def main() -> None:
    opportunities = load_opportunities("data/opportunities.csv")

    user_prefs = {
        "target_track": "software_engineering",
        "preferred_format": "self_paced",
        "skill_level": 0.3,
        "prefers_free": True,
        "needs_remote": True,
        "max_hours": 20,
        "interests": ["python", "git"],
    }

    recommendations = recommend_opportunities(user_prefs, opportunities, k=5)

    print("\nTop opportunities:\n")
    for opportunity, score, explanation in recommendations:
        print(f"{opportunity['title']} - Score: {score:.2f}")
        print(f"Because: {explanation}")
        print()


if __name__ == "__main__":
    main()
