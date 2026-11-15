"""Generate a learning path from retrieved TechRoute opportunities."""

import json
import math
import os
import re
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple

from dotenv import load_dotenv

from src.recommender import recommend_opportunities

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MODEL = "gemini-4-hydrogen"
GEMINI_SOURCE = "Source: Gemini (verified against retrieved data)"
FALLBACK_SOURCE = "Source: rule-based fallback"

ALLOWED_TRACKS = {
    "it_support",
    "networking",
    "cybersecurity",
    "software_engineering",
    "web_development",
    "ai_engineering",
    "cloud_computing",
    "hardware_repair",
    "general",
}
ALLOWED_FORMATS = {
    "self_paced",
    "cohort",
    "project_based",
    "mentored",
    "work_based",
}
ALLOWED_STAGES = {"Foundations", "Build Skills", "Prove Skills", "Apply"}
INTERNSHIP_TYPES = {"internship", "job"}
INTEREST_PATTERN = re.compile(r"[a-z0-9_+-]{1,50}")

GeminiCall = Callable[[str, str], str]
LearningPath = Dict[str, object]


def _sanitize_profile(profile: Dict) -> Dict[str, object]:
    """Keep only validated learning preferences and drop all unknown keys."""
    target_track = profile.get("target_track")
    if target_track not in ALLOWED_TRACKS:
        target_track = None

    preferred_format = profile.get("preferred_format")
    if preferred_format not in ALLOWED_FORMATS:
        preferred_format = None

    skill_level = profile.get("skill_level", 0.3)
    if (
        isinstance(skill_level, bool)
        or not isinstance(skill_level, (int, float))
        or not math.isfinite(skill_level)
        or not 0 <= skill_level <= 1
    ):
        skill_level = 0.3

    max_hours = profile.get("max_hours")
    if (
        isinstance(max_hours, bool)
        or not isinstance(max_hours, (int, float))
        or not math.isfinite(max_hours)
        or max_hours <= 0
    ):
        max_hours = None

    raw_interests = profile.get("interests", [])
    interests = []
    if isinstance(raw_interests, list):
        for value in raw_interests:
            if isinstance(value, str):
                tag = value.strip().lower()
                if INTEREST_PATTERN.fullmatch(tag) and tag not in interests:
                    interests.append(tag)

    return {
        "target_track": target_track,
        "preferred_format": preferred_format,
        "skill_level": skill_level,
        "prefers_free": profile.get("prefers_free")
        if isinstance(profile.get("prefers_free"), bool)
        else True,
        "needs_remote": profile.get("needs_remote")
        if isinstance(profile.get("needs_remote"), bool)
        else None,
        "max_hours": max_hours,
        "interests": interests,
    }


def _retrieve_opportunities(
    profile: Dict[str, object], opportunities: List[Dict]
) -> List[Dict[str, object]]:
    """Retrieve ranked recommendations and matching track internships/jobs."""
    with redirect_stdout(StringIO()):
        primary = recommend_opportunities(profile, opportunities, k=8)

    retrieved: List[Dict] = [item for item, _, _ in primary]
    target_track = profile.get("target_track")
    track_internships = [
        item
        for item in opportunities
        if item.get("career_track") == target_track
        and item.get("category") in INTERNSHIP_TYPES
    ]
    if track_internships:
        with redirect_stdout(StringIO()):
            additional = recommend_opportunities(profile, track_internships, k=2)
        seen_ids = {item.get("id") for item in retrieved}
        seen_titles = {item.get("title") for item in retrieved}
        for item, _, _ in additional:
            if item.get("id") not in seen_ids and item.get("title") not in seen_titles:
                retrieved.append(item)
                seen_ids.add(item.get("id"))
                seen_titles.add(item.get("title"))

    return [
        {
            "title": item["title"],
            "provider": item["provider"],
            "type": item["category"],
            "difficulty": item["difficulty"],
            "cost_type": item["cost_type"],
            "cost_usd": item["cost_usd"],
            "hours_required": item.get("hours_required"),
            "url": item["url"],
        }
        for item in retrieved
    ]


def _build_prompt(
    profile: Dict[str, object], retrieved: List[Dict[str, object]]
) -> str:
    has_apply_items = any(item["type"] in INTERNSHIP_TYPES for item in retrieved)
    apply_instruction = (
        "Include an Apply step using retrieved internship or job titles."
        if has_apply_items
        else (
            "Include an Apply step with an empty opportunity_titles list and state "
            "that no internship or job opportunities are in the dataset yet."
        )
    )
    return (
        "Create a practical beginner-aware technology learning path. Return only "
        "valid JSON as an array of steps. Every step must have exactly these keys: "
        "step_number (integer), stage (one of Foundations, Build Skills, "
        "Prove Skills, Apply), goal (string), opportunity_titles (array of exact "
        "titles), and why (string). Use ONLY the opportunities in the retrieved "
        "list. Never invent or recommend courses, projects, certifications, URLs, "
        "internships, or jobs. Each opportunity_titles entry must exactly match a "
        "retrieved title. Keep goals and reasons general; reference specific "
        "resources only by listing their retrieved titles. "
        f"{apply_instruction}\n\n"
        "Student learning preferences (the complete allowlisted profile):\n"
        f"{json.dumps(profile, sort_keys=True)}\n\n"
        "Retrieved opportunities (the only allowed resources):\n"
        f"{json.dumps(retrieved, sort_keys=True)}"
    )


def _load_gemini_config() -> Tuple[Optional[str], str]:
    load_dotenv(PROJECT_ROOT / ".env")
    return os.getenv("GEMINI_API_KEY"), os.getenv("GEMINI_MODEL", DEFAULT_MODEL)


def _call_gemini(prompt: str, api_key: str, model: str) -> str:
    from google import genai

    client = genai.Client(api_key=api_key)
    response = client.interactions.create(model=model, input=prompt)
    if not response.output_text:
        raise ValueError("Gemini returned an empty response")
    return response.output_text


def _validate_response(
    response_text: str, retrieved: List[Dict[str, object]]
) -> List[Dict[str, object]]:
    parsed = json.loads(response_text)
    if not isinstance(parsed, list) or not parsed:
        raise ValueError("Expected a non-empty JSON list of path steps")

    allowed_titles = {item["title"] for item in retrieved}
    apply_titles = {
        item["title"]
        for item in retrieved
        if item["type"] in INTERNSHIP_TYPES
    }
    validated = []
    expected_keys = {
        "step_number",
        "stage",
        "goal",
        "opportunity_titles",
        "why",
    }

    for index, step in enumerate(parsed, start=1):
        if not isinstance(step, dict) or set(step) != expected_keys:
            raise ValueError("Path step has an invalid shape")
        if step["step_number"] != index or step["stage"] not in ALLOWED_STAGES:
            raise ValueError("Path step has an invalid number or stage")
        if not isinstance(step["goal"], str) or not step["goal"].strip():
            raise ValueError("Path step is missing a goal")
        if not isinstance(step["why"], str) or not step["why"].strip():
            raise ValueError("Path step is missing a reason")
        titles = step["opportunity_titles"]
        if not isinstance(titles, list) or any(
            not isinstance(title, str) or title not in allowed_titles
            for title in titles
        ):
            raise ValueError("Path references an opportunity outside retrieved data")
        if step["stage"] == "Apply":
            if apply_titles and not set(titles).intersection(apply_titles):
                raise ValueError("Apply step does not use a retrieved internship or job")
            if not apply_titles:
                text = f"{step['goal']} {step['why']}".lower()
                if titles or "dataset" not in text or not (
                    "no " in text or "none" in text
                ):
                    raise ValueError("Apply step must state no items are in the dataset")
        validated.append(step)

    if not any(step["stage"] == "Apply" for step in validated):
        raise ValueError("Path is missing its Apply step")
    return validated


def _fallback_path(retrieved: List[Dict[str, object]]) -> List[Dict[str, object]]:
    ordered = sorted(
        retrieved,
        key=lambda item: (
            item["difficulty"] if item["difficulty"] is not None else 1.0,
            item["title"],
        ),
    )
    used = set()

    def choose(types):
        for item in ordered:
            if item["type"] in types and item["title"] not in used:
                used.add(item["title"])
                return [item["title"]]
        return []

    foundations = choose({"course"})
    if not foundations:
        foundations = choose({"career", "certification", "program", "project"})
    build_skills = choose({"project", "program", "course"})
    prove_skills = choose({"certification", "project", "course"})
    apply_titles = [
        item["title"]
        for item in ordered
        if item["type"] in INTERNSHIP_TYPES
    ][:2]

    if apply_titles:
        apply_goal = "Use the retrieved internship or job opportunities to apply."
        apply_why = "These are the available next-step opportunities in the retrieved data."
    else:
        apply_goal = (
            "No internship or job opportunities are in the dataset yet for this track."
        )
        apply_why = "No matching internship or job rows were retrieved."

    return [
        {
            "step_number": 1,
            "stage": "Foundations",
            "goal": "Build foundational knowledge from a retrieved learning resource.",
            "opportunity_titles": foundations,
            "why": "Start with an available lower-difficulty opportunity.",
        },
        {
            "step_number": 2,
            "stage": "Build Skills",
            "goal": "Practice by completing a retrieved hands-on opportunity.",
            "opportunity_titles": build_skills,
            "why": "Hands-on work helps turn foundational knowledge into practice.",
        },
        {
            "step_number": 3,
            "stage": "Prove Skills",
            "goal": "Demonstrate skills with a retrieved credential or portfolio item.",
            "opportunity_titles": prove_skills,
            "why": "Use an available opportunity to show progress.",
        },
        {
            "step_number": 4,
            "stage": "Apply",
            "goal": apply_goal,
            "opportunity_titles": apply_titles,
            "why": apply_why,
        },
    ]


def generate_learning_path(
    profile: Dict, opportunities: List[Dict], gemini_call: Optional[GeminiCall] = None
) -> LearningPath:
    """Generate a verified Gemini path or a deterministic retrieved-data fallback."""
    safe_profile = _sanitize_profile(profile)
    retrieved = _retrieve_opportunities(safe_profile, opportunities)
    fallback = {
        "source": FALLBACK_SOURCE,
        "steps": _fallback_path(retrieved),
    }
    api_key, model = _load_gemini_config()
    if not api_key and gemini_call is None:
        return fallback

    prompt = _build_prompt(safe_profile, retrieved)
    try:
        response_text = (
            gemini_call(prompt, model)
            if gemini_call is not None
            else _call_gemini(prompt, api_key, model)
        )
        steps = _validate_response(response_text, retrieved)
    except Exception:
        return fallback

    return {"source": GEMINI_SOURCE, "steps": steps}
