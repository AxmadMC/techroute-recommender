"""Command-line runner for the TechRoute Recommender."""

from src.recommender import load_opportunities, recommend_opportunities
from src.path_generator import generate_learning_path


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

    print(
        "Privacy notice: only learning preferences (no personal data) and "
        "retrieved opportunity details are sent to Gemini."
    )
    learning_path = generate_learning_path(user_prefs, opportunities)
    print(f"\nGenerated learning path - {learning_path['source']}:\n")
    for step in learning_path["steps"]:
        print(f"{step['step_number']}. {step['stage']}: {step['goal']}")
        if step["opportunity_titles"]:
            print(f"   Opportunities: {', '.join(step['opportunity_titles'])}")
        print(f"   Why: {step['why']}")


if __name__ == "__main__":
    main()
