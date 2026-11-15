"""Command-line runner for the TechRoute Recommender."""

from src.recommender import load_opportunities, recommend_opportunities


def main() -> None:
    opportunities = load_opportunities("data/opportunities.csv")

    user_prefs = {
        "career_track": "software_engineering",
        "format": "self_paced",
        "skill_level": 0.3,
        "max_hours": 20,
        "remote": True,
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
