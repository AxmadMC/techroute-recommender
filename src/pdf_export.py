"""In-memory PDF export for TechRoute learning paths."""

from datetime import date
from io import BytesIO
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse

from fpdf import FPDF

from src.path_generator import validate_profile

PROJECT_ROOT = Path(__file__).resolve().parents[1]
FONT_DIR = PROJECT_ROOT / "assets" / "fonts"
STAGES = ("Foundations", "Build Skills", "Prove Skills", "Apply")
Recommendation = Tuple[Dict[str, object], float, str]


def _skill_label(skill_level: float) -> str:
    if skill_level < 0.4:
        return "Beginner"
    if skill_level < 0.7:
        return "Intermediate"
    return "Advanced"


def _format_track(value: Optional[str]) -> str:
    return value.replace("_", " ").title() if value else "Not specified"


def _format_option(value: Optional[str]) -> str:
    return value.replace("_", " ").title() if value else "Any format"


def _cost_label(opportunity: Dict[str, object]) -> str:
    cost_type = opportunity.get("cost_type")
    if cost_type == "free":
        return "Free"
    if cost_type == "freemium":
        return "Freemium"
    if cost_type == "paid":
        cost = opportunity.get("cost_usd")
        return f"Paid — ${cost:.2f}" if isinstance(cost, (int, float)) else "Paid"
    return "Not listed"


def _hours_label(opportunity: Dict[str, object]) -> str:
    hours = opportunity.get("hours_required")
    return f"{hours:g} hours" if isinstance(hours, (int, float)) else "Not listed"


def _write_line(pdf: FPDF, text: str, height: float = 6) -> None:
    pdf.multi_cell(0, height, str(text), new_x="LMARGIN", new_y="NEXT")


def _write_heading(pdf: FPDF, text: str, level: int = 2) -> None:
    sizes = {1: 20, 2: 15, 3: 12}
    pdf.ln(3)
    pdf.set_font("DejaVu", "B", sizes[level])
    _write_line(pdf, text, height=8 if level == 1 else 7)
    pdf.set_font("DejaVu", "", 11)


def _source_text(source_label: str, fallback_reason: Optional[str]) -> str:
    if "Gemini" in source_label or "AI-generated" in source_label:
        if "(verified after " in source_label:
            verification = source_label.split("Gemini (", 1)[1].rstrip(")")
            return f"AI-generated ({verification})"
        return "AI-generated (verified against retrieved data)"
    reason = fallback_reason
    if not reason and "(reason: " in source_label:
        reason = source_label.split("(reason: ", 1)[1].rstrip(")")
    return f"Rule-based fallback — reason: {reason or 'unspecified'}"


def _opportunity_lookup(
    recommendations: List[Recommendation],
    opportunities: Optional[List[Dict[str, object]]],
) -> Dict[str, Dict[str, object]]:
    lookup: Dict[str, Dict[str, object]] = {}
    for opportunity in opportunities or []:
        title = opportunity.get("title")
        if isinstance(title, str):
            lookup.setdefault(title, opportunity)
    for opportunity, _, _ in recommendations:
        title = opportunity.get("title")
        if isinstance(title, str):
            lookup.setdefault(title, opportunity)
    return lookup


def _write_path_opportunity(
    pdf: FPDF,
    title: str,
    opportunity: Optional[Dict[str, object]],
) -> None:
    pdf.set_font("DejaVu", "B", 11)
    _write_line(pdf, f"• {title}")
    pdf.set_font("DejaVu", "", 11)
    if opportunity is None:
        _write_line(pdf, "  Provider: Not listed · Cost: Not listed · Hours: Not listed")
        return

    provider = str(opportunity.get("provider") or "Not listed")
    _write_line(
        pdf,
        f"  Provider: {provider} · Cost: {_cost_label(opportunity)} · "
        f"Hours: {_hours_label(opportunity)}",
    )
    url = opportunity.get("url")
    if isinstance(url, str) and urlparse(url).scheme in {"http", "https"}:
        pdf.set_text_color(11, 79, 113)
        pdf.write(6, f"  Open {title} at {provider}", link=url)
        pdf.ln(6)
        pdf.set_text_color(0, 0, 0)


def build_pdf(
    profile: Dict[str, object],
    recommendations: List[Recommendation],
    learning_path: Dict[str, object],
    source_label: str,
    fallback_reason: Optional[str],
    opportunities: Optional[List[Dict[str, object]]] = None,
) -> bytes:
    """Build a selectable-text route PDF entirely in memory.

    ``opportunities`` supplies details for path items that are outside the top
    recommendations; it is optional for callers using only the required inputs.
    """
    safe_profile = validate_profile(profile)
    pdf = FPDF()
    pdf.set_margins(18, 16, 18)
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.add_font("DejaVu", "", str(FONT_DIR / "DejaVuSans.ttf"))
    pdf.add_font("DejaVu", "B", str(FONT_DIR / "DejaVuSans-Bold.ttf"))
    pdf.set_title("My TechRoute Learning Path")
    pdf.add_page()
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("DejaVu", "", 11)

    _write_heading(pdf, "My TechRoute Learning Path", level=1)
    _write_line(pdf, f"Generated: {date.today().isoformat()}")

    _write_heading(pdf, "My preferences")
    skill_level = safe_profile["skill_level"]
    _write_line(pdf, f"Target track: {_format_track(safe_profile['target_track'])}")
    _write_line(pdf, f"Format: {_format_option(safe_profile['preferred_format'])}")
    _write_line(
        pdf,
        f"Skill level: {skill_level:.2f} ({_skill_label(skill_level)})",
    )
    _write_line(pdf, f"Prefers free: {'Yes' if safe_profile['prefers_free'] else 'No'}")
    remote = safe_profile["needs_remote"]
    _write_line(
        pdf,
        f"Needs remote: {'Yes' if remote is True else 'No' if remote is False else 'No preference'}",
    )
    hours = safe_profile["max_hours"]
    _write_line(
        pdf,
        f"Weekly hours: {hours:g}" if isinstance(hours, (int, float)) else "Weekly hours: Not specified",
    )
    interests = safe_profile["interests"]
    _write_line(
        pdf,
        f"Interests: {', '.join(interests) if interests else 'None specified'}",
    )

    _write_heading(pdf, "Source")
    _write_line(pdf, _source_text(source_label, fallback_reason))

    _write_heading(pdf, "Learning path")
    steps = learning_path.get("steps", [])
    steps_by_stage = {
        step.get("stage"): step for step in steps if isinstance(step, dict)
    }
    opportunities_by_title = _opportunity_lookup(recommendations, opportunities)
    for index, stage in enumerate(STAGES, start=1):
        step = steps_by_stage.get(stage, {})
        _write_heading(pdf, f"{index}. {stage}", level=3)
        _write_line(pdf, f"Goal: {step.get('goal') or 'No goal provided.'}")
        titles = step.get("opportunity_titles") or []
        if titles:
            for title in titles:
                _write_path_opportunity(
                    pdf,
                    str(title),
                    opportunities_by_title.get(str(title)),
                )
        elif stage == "Apply":
            _write_line(
                pdf,
                "No internship or job opportunities are available in the retrieved data for this route.",
            )
        else:
            _write_line(pdf, "No opportunities were assigned to this stage.")
        _write_line(pdf, f"Why: {step.get('why') or 'No explanation provided.'}")

    _write_heading(pdf, "Top recommendations")
    for rank, (opportunity, score, explanation) in enumerate(
        recommendations[:5], start=1
    ):
        title = str(opportunity.get("title") or "Untitled opportunity")
        provider = str(opportunity.get("provider") or "Provider not listed")
        _write_line(pdf, f"{rank}. {title} — {provider} — Score: {score:.2f}")
        _write_line(pdf, f"   Score breakdown: {explanation}")

    _write_heading(pdf, "Note", level=3)
    _write_line(
        pdf,
        "Generated by TechRoute Recommender. No data was saved. Verify links, "
        "costs, and eligibility before enrolling. This is guidance, not a guarantee.",
    )

    output = BytesIO()
    output.write(pdf.output())
    return output.getvalue()
