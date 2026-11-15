"""Generate a learning path from retrieved TechRoute opportunities."""

import json
import logging
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
DEFAULT_MODEL = "gemini-3.1-flash-lite"
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
PROMPT_FIELDS = (
    "title",
    "provider",
    "type",
    "difficulty",
    "cost_type",
    "cost_usd",
    "hours_required",
    "url",
)

GeminiCall = Callable[[str, str], str]
LearningPath = Dict[str, object]
logger = logging.getLogger("techroute")


class AIOutputRejected(ValueError):
    """AI output failed a source-data or response-shape check."""


def validate_profile(profile: Dict) -> Dict[str, object]:
    """Validate and return only the supported learning preferences."""
    target_track = profile.get("target_track")
    if target_track is not None and (
        not isinstance(target_track, str) or target_track not in ALLOWED_TRACKS
    ):
        raise ValueError("target_track must be a supported career track.")

    preferred_format = profile.get("preferred_format")
    if preferred_format is not None and (
        not isinstance(preferred_format, str)
        or preferred_format not in ALLOWED_FORMATS
    ):
        raise ValueError("preferred_format must be a supported learning format.")

    skill_level = profile.get("skill_level", 0.3)
    if (
        isinstance(skill_level, bool)
        or not isinstance(skill_level, (int, float))
        or not math.isfinite(skill_level)
        or not 0 <= skill_level <= 1
    ):
        raise ValueError("skill_level must be a number from 0 to 1.")

    max_hours = profile.get("max_hours")
    if max_hours is not None and (
        isinstance(max_hours, bool)
        or not isinstance(max_hours, (int, float))
        or not math.isfinite(max_hours)
        or max_hours < 0
    ):
        raise ValueError("max_hours must be a non-negative number.")

    prefers_free = profile.get("prefers_free", True)
    if not isinstance(prefers_free, bool):
        raise ValueError("prefers_free must be true or false.")

    needs_remote = profile.get("needs_remote")
    if needs_remote is not None and not isinstance(needs_remote, bool):
        raise ValueError("needs_remote must be true, false, or unset.")

    raw_interests = profile.get("interests", [])
    if not isinstance(raw_interests, list):
        raise ValueError("interests must be a list of learning tags.")
    interests = []
    for value in raw_interests:
        if isinstance(value, str):
            tag = value.strip().lower()
            if INTEREST_PATTERN.fullmatch(tag) and tag not in interests:
                interests.append(tag)

    return {
        "target_track": target_track,
        "preferred_format": preferred_format,
        "skill_level": skill_level,
        "prefers_free": prefers_free,
        "needs_remote": needs_remote,
        "max_hours": max_hours,
        "interests": interests,
    }


def _retrieve_opportunities(
    profile: Dict[str, object], opportunities: List[Dict]
) -> List[Dict[str, object]]:
    """Retrieve ranked recommendations and matching track internships/jobs."""
    needs_remote = profile.get("needs_remote") is True
    eligible = [
        item
        for item in opportunities
        if not needs_remote or item.get("remote") is True
    ]
    filtered_count = len(opportunities) - len(eligible)
    skill_level = profile["skill_level"]
    penalized_count = sum(
        skill_level < 0.5
        and "prior_experience"
        in set((item.get("eligibility") or "").split(";"))
        for item in eligible
    )
    target_track = profile.get("target_track") or "unspecified"
    logger.info(
        "guardrails_applied target_track=%s filtered=%d penalized=%d",
        target_track,
        filtered_count,
        penalized_count,
    )

    with redirect_stdout(StringIO()):
        primary = recommend_opportunities(profile, opportunities, k=8)

    retrieved: List[Dict] = [item for item, _, _ in primary]
    track_internships = [
        item
        for item in opportunities
        if item.get("career_track") == profile.get("target_track")
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

    logger.info(
        "retrieval_complete target_track=%s count=%d",
        target_track,
        len(retrieved),
    )
    return [
        {
            "id": item.get("id"),
            "title": item["title"],
            "provider": item["provider"],
            "type": item["category"],
            "difficulty": item["difficulty"],
            "cost_type": item["cost_type"],
            "cost_usd": item["cost_usd"],
            "hours_required": item.get("hours_required"),
            "url": item["url"],
            "skills": item.get("skills", ""),
        }
        for item in retrieved
    ]


def _build_prompt(
    profile: Dict[str, object], retrieved: List[Dict[str, object]]
) -> str:
    prompt_opportunities = [
        {key: item[key] for key in PROMPT_FIELDS}
        for item in retrieved
    ]
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
        f"{json.dumps(prompt_opportunities, sort_keys=True)}"
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
    try:
        parsed = json.loads(response_text)
    except json.JSONDecodeError as error:
        raise AIOutputRejected("invalid JSON") from error
    if not isinstance(parsed, list) or not parsed:
        raise AIOutputRejected("invalid response structure")

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
            raise AIOutputRejected("invalid response structure")
        if (
            type(step["step_number"]) is not int
            or step["step_number"] != index
            or not isinstance(step["stage"], str)
            or step["stage"] not in ALLOWED_STAGES
        ):
            raise AIOutputRejected("invalid step number or stage")
        if not isinstance(step["goal"], str) or not step["goal"].strip():
            raise AIOutputRejected("missing step goal")
        if not isinstance(step["why"], str) or not step["why"].strip():
            raise AIOutputRejected("missing step reason")
        titles = step["opportunity_titles"]
        if not isinstance(titles, list):
            raise AIOutputRejected("invalid opportunity title list")
        if any(not isinstance(title, str) or title not in allowed_titles for title in titles):
            raise AIOutputRejected(
                "AI output referenced an opportunity not in the retrieved data"
            )
        if step["stage"] == "Apply":
            if apply_titles and not set(titles).intersection(apply_titles):
                raise AIOutputRejected("Apply step omitted retrieved internship/job")
            if not apply_titles:
                text = f"{step['goal']} {step['why']}".lower()
                if titles or "dataset" not in text or not (
                    "no " in text or "none" in text
                ):
                    raise AIOutputRejected("Apply step omitted no-items notice")
        validated.append(step)

    if not any(step["stage"] == "Apply" for step in validated):
        raise AIOutputRejected("missing Apply step")
    return validated


def _is_tool_or_lab(item: Dict[str, object]) -> bool:
    title = item["title"].lower()
    skills = set((item.get("skills") or "").split(";"))
    tool_tags = {"home_lab", "packet_tracer", "wireshark", "virtualization"}
    return (
        item["type"] == "project" and ("lab" in title or "home_lab" in skills)
    ) or bool(skills & tool_tags - {"home_lab"}) or any(
        tool in title for tool in ("packet tracer", "wireshark", "virtualbox")
    )


def _fallback_path(retrieved: List[Dict[str, object]]) -> List[Dict[str, object]]:
    ordered = sorted(
        retrieved,
        key=lambda item: (
            item["difficulty"] if item["difficulty"] is not None else 1.0,
            item["title"],
        ),
    )
    foundations = [
        item["title"]
        for item in ordered
        if item["type"] in {"course", "program", "career"}
        and not _is_tool_or_lab(item)
    ]
    build_skills = [
        item["title"] for item in ordered if _is_tool_or_lab(item)
    ]
    prove_skills = [
        item["title"]
        for item in ordered
        if item["type"] in {"project", "certification", "volunteer"}
        and item["title"] not in build_skills
    ]
    apply_titles = [
        item["title"] for item in ordered if item["type"] in INTERNSHIP_TYPES
    ]

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
            "goal": "Build foundational knowledge from retrieved learning resources.",
            "opportunity_titles": foundations,
            "why": "Begin with courses and other foundational learning resources.",
        },
        {
            "step_number": 2,
            "stage": "Build Skills",
            "goal": "Practice with retrieved tools and hands-on labs.",
            "opportunity_titles": build_skills,
            "why": "These retrieved resources provide practical tool or lab experience.",
        },
        {
            "step_number": 3,
            "stage": "Prove Skills",
            "goal": "Demonstrate skills with retrieved projects and credentials.",
            "opportunity_titles": prove_skills,
            "why": "Projects, certifications, and contributions can demonstrate progress.",
        },
        {
            "step_number": 4,
            "stage": "Apply",
            "goal": apply_goal,
            "opportunity_titles": apply_titles,
            "why": apply_why,
        },
    ]


def _fallback(
    reason: str, retrieved: List[Dict[str, object]], target_track: Optional[str]
) -> LearningPath:
    logger.info(
        "fallback_used target_track=%s reason=%s",
        target_track or "unspecified",
        reason,
    )
    return {
        "source": f"{FALLBACK_SOURCE} (reason: {reason})",
        "steps": _fallback_path(retrieved),
    }


def generate_learning_path(
    profile: Dict, opportunities: List[Dict], gemini_call: Optional[GeminiCall] = None
) -> LearningPath:
    """Generate a verified Gemini path or a deterministic retrieved-data fallback."""
    safe_profile = validate_profile(profile)
    retrieved = _retrieve_opportunities(safe_profile, opportunities)
    target_track = safe_profile.get("target_track")
    api_key, model = _load_gemini_config()
    if not api_key and gemini_call is None:
        logger.warning("gemini_call_skipped reason=no API key")
        return _fallback("no API key", retrieved, target_track)

    prompt = _build_prompt(safe_profile, retrieved)
    logger.info(
        "gemini_call_started target_track=%s",
        target_track or "unspecified",
    )
    try:
        response_text = (
            gemini_call(prompt, model)
            if gemini_call is not None
            else _call_gemini(prompt, api_key, model)
        )
    except Exception:
        logger.warning("gemini_call_failed reason=Gemini API error")
        return _fallback("Gemini API error", retrieved, target_track)
    logger.info("gemini_call_succeeded target_track=%s", target_track or "unspecified")

    try:
        steps = _validate_response(response_text, retrieved)
    except AIOutputRejected as error:
        logger.warning("ai_output_rejected reason=%s", error)
        return _fallback(str(error), retrieved, target_track)
    except Exception:
        logger.warning("ai_output_rejected reason=invalid response structure")
        return _fallback("invalid response structure", retrieved, target_track)

    logger.info(
        "ai_output_accepted target_track=%s reason=valid JSON and retrieved titles verified",
        target_track or "unspecified",
    )
    return {"source": GEMINI_SOURCE, "steps": steps}
