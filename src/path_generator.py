"""Generate a learning path from retrieved TechRoute opportunities."""

import json
import logging
import math
import os
import re
import time
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple

from dotenv import load_dotenv

from src.guide_retriever import retrieve_guide_sections
from src.recommender import recommend_opportunities

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MODEL = "gemini-3.1-flash-lite"
GEMINI_SOURCE = "Source: Gemini (verified against retrieved data)"
FALLBACK_SOURCE = "Source: rule-based fallback"
EXPECTED_STAGES = ("Foundations", "Build Skills", "Prove Skills", "Apply")
MAX_STAGE_OPPORTUNITIES = 3
MAX_REPAIR_ATTEMPTS = 2
GEMINI_CALL_PAUSE_SECONDS = 1.0

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

    def __init__(self, errors):
        self.errors = [errors] if isinstance(errors, str) else list(errors)
        super().__init__("; ".join(self.errors))


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
    profile: Dict[str, object],
    retrieved: List[Dict[str, object]],
    plan: List[Dict[str, str]],
    track_context: List[Dict[str, str]],
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
    return GENERATE_PROMPT_TEMPLATE.format(
        apply_instruction=apply_instruction,
        profile_json=json.dumps(profile, sort_keys=True),
        plan_json=json.dumps(plan, sort_keys=True),
        retrieved_json=json.dumps(prompt_opportunities, sort_keys=True),
        track_context=_format_track_context(track_context),
    )


def _format_track_context(sections: List[Dict[str, str]]) -> str:
    if not sections:
        return "No track guide context is available."
    return "\n\n".join(
        f"## {section['name']}\n{section['content']}" for section in sections
    )


PLAN_PROMPT_TEMPLATE = """Create a short plan for a technology learning path. Return only valid JSON with one top-level "assignments" array. Each assignment must have exactly these keys: "title" (an exact retrieved title), "stage" (one of Foundations, Build Skills, Prove Skills, Apply), and "reason" (one concise sentence explaining the choice using learning preferences, track context, or opportunity type). Assign each retrieved opportunity at most once. Put internships and jobs in Apply when present. Do not invent titles or include any other fields. Use track context for track-specific planning, but select opportunity titles ONLY from the retrieved opportunities.

Student learning preferences:
{profile_json}

Retrieved opportunities (the only allowed resources):
{retrieved_json}

Track context (guidance only, never a source of opportunity titles):
{track_context}"""

GENERATE_PROMPT_TEMPLATE = """Create a practical beginner-aware technology learning path using the plan as guidance. Return only valid JSON as an array of exactly four steps in this order: Foundations, Build Skills, Prove Skills, Apply. Every step must have exactly these keys: step_number (integer, 1 through 4), stage (string), goal (string), opportunity_titles (array of exact titles), and why (string). Use track context to make goals and explanations specific to this track. Use opportunity titles ONLY from the retrieved opportunities list; track context is guidance, never a source of opportunity titles. Never invent or recommend resources, certifications, URLs, internships, or jobs. Each title may appear in only one stage, and each stage may contain at most 3 opportunities. Keep goals and reasons general; refer to specific resources only by listing their retrieved titles. {apply_instruction}

Student learning preferences:
{profile_json}

Agent plan:
{plan_json}

Retrieved opportunities (the only allowed resources):
{retrieved_json}

Track context (guidance only, never a source of opportunity titles):
{track_context}"""

REPAIR_PROMPT_TEMPLATE = """Correct the previous learning path so it passes every verifier check. Return only valid JSON as an array of exactly four steps in this order: Foundations, Build Skills, Prove Skills, Apply. Every step must have exactly these keys: step_number (integer, 1 through 4), stage (string), goal (string), opportunity_titles (array of exact titles), and why (string). Use track context for track-specific goals and explanations. Use ONLY titles from the retrieved opportunities; track context is guidance and never a source of opportunity titles. Do not repeat a title across stages, and include at most 3 opportunities per stage. Address every verifier error listed below; keep the Apply step consistent with the retrieved internship/job data.

Verifier errors:
{errors_json}

Previous path output:
{previous_output}

Student learning preferences:
{profile_json}

Agent plan:
{plan_json}

Retrieved opportunities (the only allowed resources):
{retrieved_json}

Track context (guidance only, never a source of opportunity titles):
{track_context}"""


def _prompt_opportunities(
    retrieved: List[Dict[str, object]],
) -> List[Dict[str, object]]:
    return [{key: item[key] for key in PROMPT_FIELDS} for item in retrieved]


def _build_plan_prompt(
    profile: Dict[str, object],
    retrieved: List[Dict[str, object]],
    track_context: List[Dict[str, str]],
) -> str:
    return PLAN_PROMPT_TEMPLATE.format(
        profile_json=json.dumps(profile, sort_keys=True),
        retrieved_json=json.dumps(_prompt_opportunities(retrieved), sort_keys=True),
        track_context=_format_track_context(track_context),
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


def _validate_plan(
    response_text: str, retrieved: List[Dict[str, object]]
) -> List[Dict[str, str]]:
    try:
        parsed = json.loads(response_text)
    except json.JSONDecodeError as error:
        raise AIOutputRejected("invalid plan JSON") from error
    if not isinstance(parsed, dict) or set(parsed) != {"assignments"}:
        raise AIOutputRejected("invalid plan structure")
    assignments = parsed["assignments"]
    if not isinstance(assignments, list):
        raise AIOutputRejected("invalid plan assignments")

    retrieved_titles = {item["title"] for item in retrieved}
    validated = []
    errors = []
    seen_titles = set()
    expected_keys = {"title", "stage", "reason"}
    for assignment in assignments:
        if not isinstance(assignment, dict) or set(assignment) != expected_keys:
            errors.append("invalid plan assignment structure")
            continue
        title = assignment["title"]
        stage = assignment["stage"]
        reason = assignment["reason"]
        if not isinstance(title, str) or title not in retrieved_titles:
            errors.append("plan referenced a non-retrieved opportunity")
            continue
        if title in seen_titles:
            errors.append("plan assigned an opportunity more than once")
            continue
        if not isinstance(stage, str) or stage not in EXPECTED_STAGES:
            errors.append("plan used an invalid stage")
            continue
        if not isinstance(reason, str) or not reason.strip():
            errors.append("plan assignment omitted its reason")
            continue
        if "\n" in reason or "\r" in reason:
            errors.append("plan assignment reason must be one line")
            continue
        seen_titles.add(title)
        validated.append(
            {"title": title, "stage": stage, "reason": reason.strip()}
        )
    if errors:
        raise AIOutputRejected(errors)
    return validated


def _validate_response(
    response_text: str, retrieved: List[Dict[str, object]]
) -> List[Dict[str, object]]:
    if not isinstance(response_text, str):
        raise AIOutputRejected("invalid JSON")
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
    errors = []
    expected_keys = {
        "step_number",
        "stage",
        "goal",
        "opportunity_titles",
        "why",
    }

    for index, step in enumerate(parsed, start=1):
        if not isinstance(step, dict) or set(step) != expected_keys:
            errors.append("invalid response structure")
            continue
        if (
            type(step["step_number"]) is not int
            or step["step_number"] != index
            or not isinstance(step["stage"], str)
            or step["stage"] not in ALLOWED_STAGES
        ):
            errors.append("invalid step number or stage")
        if not isinstance(step["goal"], str) or not step["goal"].strip():
            errors.append("missing step goal")
        if not isinstance(step["why"], str) or not step["why"].strip():
            errors.append("missing step reason")
        titles = step["opportunity_titles"]
        if not isinstance(titles, list):
            errors.append("invalid opportunity title list")
            titles = []
            validated_step = {**step, "opportunity_titles": titles}
        else:
            validated_step = step
        if len(titles) > MAX_STAGE_OPPORTUNITIES:
            stage = step["stage"] if isinstance(step["stage"], str) else "Unknown"
            errors.append(
                f"{stage} has {len(titles)} items; maximum is "
                f"{MAX_STAGE_OPPORTUNITIES}"
            )
        for title in titles:
            if not isinstance(title, str) or title not in allowed_titles:
                errors.append(
                    "AI output referenced an opportunity not in the retrieved data"
                )
                continue
            previous_stage = next(
                (
                    existing["stage"]
                    for existing in validated
                    if title in existing["opportunity_titles"]
                ),
                None,
            )
            if previous_stage is not None and previous_stage != step["stage"]:
                errors.append(
                    f"{title} appears in both {previous_stage} and {step['stage']}"
                )
        if step["stage"] == "Apply":
            valid_titles = {
                title for title in titles if isinstance(title, str)
            }
            if apply_titles and not valid_titles.intersection(apply_titles):
                errors.append("Apply step omitted retrieved internship/job")
            if not apply_titles:
                text = (
                    f"{step.get('goal', '')} {step.get('why', '')}"
                ).lower()
                if titles or "dataset" not in text or not (
                    "no " in text or "none" in text
                ):
                    errors.append("Apply step omitted no-items notice")
        validated.append(validated_step)

    actual_stages = [
        step["stage"]
        for step in validated
        if isinstance(step.get("stage"), str)
    ]
    if actual_stages != list(EXPECTED_STAGES):
        errors.append("path must contain exactly the 4 stages in order")
    if not any(step.get("stage") == "Apply" for step in validated):
        errors.append("missing Apply step")
    if errors:
        raise AIOutputRejected(list(dict.fromkeys(errors)))
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
            "opportunity_titles": foundations[:MAX_STAGE_OPPORTUNITIES],
            "why": "Begin with courses and other foundational learning resources.",
        },
        {
            "step_number": 2,
            "stage": "Build Skills",
            "goal": "Practice with retrieved tools and hands-on labs.",
            "opportunity_titles": build_skills[:MAX_STAGE_OPPORTUNITIES],
            "why": "These retrieved resources provide practical tool or lab experience.",
        },
        {
            "step_number": 3,
            "stage": "Prove Skills",
            "goal": "Demonstrate skills with retrieved projects and credentials.",
            "opportunity_titles": prove_skills[:MAX_STAGE_OPPORTUNITIES],
            "why": "Projects, certifications, and contributions can demonstrate progress.",
        },
        {
            "step_number": 4,
            "stage": "Apply",
            "goal": apply_goal,
            "opportunity_titles": apply_titles[:MAX_STAGE_OPPORTUNITIES],
            "why": apply_why,
        },
    ]


def _fallback(
    reason: str,
    retrieved: List[Dict[str, object]],
    target_track: Optional[str],
    trace: Optional[List[Dict[str, object]]] = None,
    repair_attempts: int = 0,
) -> LearningPath:
    logger.info(
        "fallback_used target_track=%s reason=%s",
        target_track or "unspecified",
        reason,
    )
    return {
        "source": f"{FALLBACK_SOURCE} (reason: {reason})",
        "steps": _fallback_path(retrieved),
        "trace": trace or [],
        "repair_attempts": repair_attempts,
    }


def _trace_entry(
    step_name: str,
    attempt_number: int,
    decision: str,
    verifier_errors: Optional[List[str]] = None,
    **details,
) -> Dict[str, object]:
    return {
        "step_name": step_name,
        "attempt_number": attempt_number,
        "decision": decision,
        "verifier_errors": verifier_errors or [],
        **details,
    }


def _redact_trace(
    trace: List[Dict[str, object]], api_key: Optional[str]
) -> List[Dict[str, object]]:
    if not api_key:
        return trace

    def redact(value):
        if isinstance(value, str):
            return value.replace(api_key, "[redacted]")
        if isinstance(value, list):
            return [redact(item) for item in value]
        if isinstance(value, dict):
            return {key: redact(item) for key, item in value.items()}
        return value

    return redact(trace)


def format_agent_trace(trace: List[Dict[str, object]]) -> List[str]:
    """Format trace records as concise, plain-language lines."""
    lines = []
    for entry in trace:
        step_name = str(entry.get("step_name", "Step"))
        attempt = entry.get("attempt_number", "n/a")
        decision = str(entry.get("decision", "recorded")).replace("_", " ")
        detail = entry.get("detail")
        line = f"{step_name} (attempt {attempt}): {decision}"
        if detail:
            line += f" - {detail}"
        lines.append(line)
        for assignment in entry.get("plan", []):
            lines.append(
                f"  {assignment['title']} -> {assignment['stage']}: "
                f"{assignment['reason']}"
            )
        for error in entry.get("verifier_errors", []):
            lines.append(f"  Verifier: {error}")
    return lines


def generate_learning_path(
    profile: Dict,
    opportunities: List[Dict],
    gemini_call: Optional[GeminiCall] = None,
    offline: bool = False,
    use_guides: bool = True,
) -> LearningPath:
    """Generate a verified Gemini path or a deterministic retrieved-data fallback."""
    safe_profile = validate_profile(profile)
    retrieved = _retrieve_opportunities(safe_profile, opportunities)
    target_track = safe_profile.get("target_track")
    trace: List[Dict[str, object]] = []
    if offline:
        trace.append(
            _trace_entry(
                "PLAN",
                1,
                "skipped",
                detail="Offline mode does not plan or call Gemini.",
            )
        )
        trace.append(
            _trace_entry(
                "DECIDE",
                1,
                "fallback",
                detail="Rule-based fallback selected: offline mode.",
            )
        )
        return _fallback("offline mode", retrieved, target_track, trace)

    api_key, model = _load_gemini_config()
    if not api_key and gemini_call is None:
        logger.warning("gemini_call_skipped reason=no API key")
        trace.extend(
            [
                _trace_entry(
                    "PLAN",
                    1,
                    "skipped",
                    detail="AI unavailable because no API key is configured.",
                ),
                _trace_entry(
                    "DECIDE",
                    1,
                    "fallback",
                    detail="Rule-based fallback selected: no API key.",
                ),
            ]
        )
        return _fallback("no API key", retrieved, target_track, trace)

    guide_sections = (
        retrieve_guide_sections(safe_profile) if use_guides else []
    )
    guide_section_names = [section["name"] for section in guide_sections]
    call_count = 0

    def call_model(prompt: str) -> str:
        nonlocal call_count
        if gemini_call is None and call_count:
            time.sleep(GEMINI_CALL_PAUSE_SECONDS)
        call_count += 1
        if gemini_call is not None:
            return gemini_call(prompt, model)
        return _call_gemini(prompt, api_key, model)

    logger.info(
        "gemini_call_started target_track=%s",
        target_track or "unspecified",
    )
    try:
        plan_response = call_model(
            _build_plan_prompt(safe_profile, retrieved, guide_sections)
        )
        plan = _validate_plan(plan_response, retrieved)
        trace.append(
            _trace_entry(
                "PLAN",
                1,
                "accepted",
                detail=f"Created a plan for {len(plan)} retrieved opportunities.",
                plan=plan,
                guide_sections=guide_section_names,
            )
        )
    except AIOutputRejected as error:
        trace.extend(
            [
                _trace_entry(
                    "PLAN",
                    1,
                    "rejected",
                    verifier_errors=error.errors,
                    guide_sections=guide_section_names,
                ),
                _trace_entry(
                    "DECIDE",
                    1,
                    "fallback",
                    detail="Rule-based fallback selected: AI plan failed verification.",
                ),
            ]
        )
        logger.warning("ai_plan_rejected verifier_error_count=%d", len(error.errors))
        return _fallback(
            "AI plan failed verification",
            retrieved,
            target_track,
            _redact_trace(trace, api_key),
        )
    except Exception:
        logger.warning("gemini_call_failed reason=Gemini API error")
        trace.extend(
            [
                _trace_entry(
                    "PLAN",
                    1,
                    "failed",
                    detail="Gemini request failed while creating the plan.",
                    guide_sections=guide_section_names,
                ),
                _trace_entry(
                    "DECIDE",
                    1,
                    "fallback",
                    detail="Rule-based fallback selected: Gemini API error.",
                ),
            ]
        )
        return _fallback(
            "Gemini API error",
            retrieved,
            target_track,
            _redact_trace(trace, api_key),
        )
    logger.info("gemini_call_succeeded target_track=%s", target_track or "unspecified")

    repair_attempts = 0
    try:
        response_text = call_model(
            _build_prompt(safe_profile, retrieved, plan, guide_sections)
        )
    except Exception:
        logger.warning("gemini_call_failed reason=Gemini API error")
        trace.extend(
            [
                _trace_entry(
                    "GENERATE",
                    1,
                    "failed",
                    detail="Gemini request failed while generating the path.",
                ),
                _trace_entry(
                    "DECIDE",
                    1,
                    "fallback",
                    detail="Rule-based fallback selected: Gemini API error.",
                ),
            ]
        )
        return _fallback(
            "Gemini API error",
            retrieved,
            target_track,
            _redact_trace(trace, api_key),
        )

    attempt_number = 1
    while True:
        trace.append(
            _trace_entry(
                "GENERATE",
                attempt_number,
                "draft_received",
                detail=(
                    "Received the initial path draft."
                    if attempt_number == 1
                    else "Received a corrected path draft."
                ),
            )
        )
        try:
            steps = _validate_response(response_text, retrieved)
        except AIOutputRejected as error:
            trace.append(
                _trace_entry(
                    "VERIFY",
                    attempt_number,
                    "rejected",
                    verifier_errors=error.errors,
                    detail="The path draft did not pass verification.",
                )
            )
            logger.warning(
                "ai_output_rejected verifier_error_count=%d", len(error.errors)
            )
            if repair_attempts >= MAX_REPAIR_ATTEMPTS:
                fallback_reason = (
                    "AI output failed verification after 2 repair attempts"
                )
                trace.append(
                    _trace_entry(
                        "DECIDE",
                        attempt_number,
                        "fallback",
                        verifier_errors=error.errors,
                        detail=f"Rule-based fallback selected: {fallback_reason}.",
                        repair_attempts=repair_attempts,
                    )
                )
                return _fallback(
                    fallback_reason,
                    retrieved,
                    target_track,
                    _redact_trace(trace, api_key),
                    repair_attempts,
                )

            repair_attempts += 1
            trace.append(
                _trace_entry(
                    "SELF-CORRECT",
                    repair_attempts,
                    "requested",
                    verifier_errors=error.errors,
                    detail="Sent the verifier errors and prior draft for correction.",
                )
            )
            repair_prompt = REPAIR_PROMPT_TEMPLATE.format(
                errors_json=json.dumps(error.errors, ensure_ascii=False),
                previous_output=response_text,
                profile_json=json.dumps(safe_profile, sort_keys=True),
                plan_json=json.dumps(plan, sort_keys=True),
                retrieved_json=json.dumps(
                    _prompt_opportunities(retrieved), sort_keys=True
                ),
                track_context=_format_track_context(guide_sections),
            )
            try:
                response_text = call_model(repair_prompt)
            except Exception:
                logger.warning("gemini_call_failed reason=Gemini API error")
                trace.extend(
                    [
                        _trace_entry(
                            "SELF-CORRECT",
                            repair_attempts,
                            "failed",
                            detail="Gemini request failed during self-correction.",
                        ),
                        _trace_entry(
                            "DECIDE",
                            attempt_number,
                            "fallback",
                            detail=(
                                "Rule-based fallback selected: Gemini API error."
                            ),
                            repair_attempts=repair_attempts,
                        ),
                    ]
                )
                return _fallback(
                    "Gemini API error",
                    retrieved,
                    target_track,
                    _redact_trace(trace, api_key),
                    repair_attempts,
                )
            attempt_number += 1
        except Exception:
            logger.warning("ai_output_rejected reason=invalid response structure")
            fallback_reason = "invalid response structure"
            trace.append(
                _trace_entry(
                    "VERIFY",
                    attempt_number,
                    "failed",
                    detail=f"Rule-based fallback selected: {fallback_reason}.",
                )
            )
            trace.append(
                _trace_entry(
                    "DECIDE",
                    attempt_number,
                    "fallback",
                    detail=f"Rule-based fallback selected: {fallback_reason}.",
                    repair_attempts=repair_attempts,
                )
            )
            return _fallback(
                fallback_reason,
                retrieved,
                target_track,
                _redact_trace(trace, api_key),
                repair_attempts,
            )
        else:
            trace.extend(
                [
                    _trace_entry(
                        "VERIFY",
                        attempt_number,
                        "accepted",
                        detail=(
                            "Valid JSON, retrieved titles, stage order, uniqueness, "
                            "and stage-size limits passed."
                        ),
                    ),
                    _trace_entry(
                        "DECIDE",
                        attempt_number,
                        "accepted",
                        detail=(
                            "AI-generated path accepted after "
                            f"{repair_attempts} self-correction(s)."
                        ),
                        repair_attempts=repair_attempts,
                    ),
                ]
            )
            logger.info(
                "ai_output_accepted target_track=%s reason=verified path",
                target_track or "unspecified",
            )
            source = (
                GEMINI_SOURCE
                if repair_attempts == 0
                else (
                    "Source: Gemini (verified after "
                    f"{repair_attempts} self-correction"
                    f"{'' if repair_attempts == 1 else 's'})"
                )
            )
            return {
                "source": source,
                "steps": steps,
                "trace": _redact_trace(trace, api_key),
                "repair_attempts": repair_attempts,
            }
