"""Streamlit interface for the TechRoute Recommender."""

import csv
from contextlib import redirect_stdout
from datetime import date
from html import escape
from io import StringIO
from pathlib import Path
from urllib.parse import urlparse

import streamlit as st

from src.logging_config import configure_logging
from src.path_generator import (
    ALLOWED_FORMATS,
    ALLOWED_TRACKS,
    _load_gemini_config,
    format_agent_trace,
)
from src.pipeline import (
    DATASET_PATH,
    PipelineValidationError,
    run_pipeline,
)
from src.pdf_export import build_pdf
from src.profiles import DEFAULT_PROFILE_NAME, PROFILE_LABELS, PROFILE_PRESETS
from src.recommender import load_opportunities

PROJECT_ROOT = Path(__file__).resolve().parent

st.set_page_config(
    page_title="TechRoute Recommender",
    page_icon="🧭",
    layout="wide",
)

logger = configure_logging()
if not st.session_state.get("_app_start_logged", False):
    logger.info("app_start")
    st.session_state["_app_start_logged"] = True


@st.cache_data(show_spinner=False)
def load_cached_opportunities():
    with redirect_stdout(StringIO()):
        return load_opportunities(str(DATASET_PATH))


def _format_track(value: str) -> str:
    return value.replace("_", " ").title()


def _format_option(value):
    if value is None:
        return "Any format"
    return value.replace("_", " ").title()


def _apply_preset():
    preset_name = {
        label: name for name, label in PROFILE_LABELS.items()
    }.get(st.session_state.get("quick_start"))
    if preset_name is None:
        return
    for field, value in PROFILE_PRESETS[preset_name].items():
        st.session_state[field] = value.copy() if isinstance(value, list) else value


def _cost_label(opportunity):
    cost_type = opportunity.get("cost_type", "unknown")
    cost_usd = opportunity.get("cost_usd", 0)
    if cost_type == "free":
        return "Free"
    if cost_type == "freemium":
        return "Freemium"
    if cost_type == "paid":
        return f"Paid — ${cost_usd:.2f}"
    return str(cost_type).replace("_", " ").title()


def _hours_label(opportunity):
    hours = opportunity.get("hours_required")
    if hours is None:
        return "Not listed"
    return f"{hours:g} hours"


def _render_opportunity(opportunity):
    title = str(opportunity.get("title", "Untitled opportunity"))
    provider = str(opportunity.get("provider", "Provider not listed"))
    st.markdown(f"**{escape(title)}**")
    st.write(
        f"Provider: {provider} · Cost: {_cost_label(opportunity)} · "
        f"Hours: {_hours_label(opportunity)}"
    )
    url = opportunity.get("url")
    if isinstance(url, str) and urlparse(url).scheme in {"http", "https"}:
        st.link_button(
            f"Open {title} at {provider}",
            url,
            type="secondary",
        )


st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        color: #17324D;
        font-size: 16px;
    }
    [data-testid="stCaptionContainer"],
    [data-testid="stWidgetLabel"],
    [data-testid="stMarkdownContainer"] {
        color: #17324D !important;
    }
    [data-testid="stCaptionContainer"] { font-size: 16px; }
    [data-testid="stVerticalBlockBorderWrapper"] {
        border-color: #64788C;
        background-color: #FFFFFF;
    }
    .techroute-verified {
        color: #0B4F71;
        background-color: #EAF1F6;
        border-left: 4px solid #0B4F71;
        border-radius: 0.25rem;
        padding: 0.65rem 0.8rem;
    }
    .techroute-fallback {
        color: #873F0A;
        background-color: #FBE4D5;
        border-left: 4px solid #873F0A;
        border-radius: 0.25rem;
        padding: 0.65rem 0.8rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("TechRoute Recommender")
st.write("Find a free, step-by-step route into tech.")

try:
    opportunities = load_cached_opportunities()
except (OSError, UnicodeError, csv.Error, ValueError) as error:
    logger.error("dataset_load_failed reason=%s", type(error).__name__)
    st.markdown(
        "**⚠ Dataset unavailable** — could not load "
        "`data/opportunities.csv`. Check that the dataset exists and is readable."
    )
    st.stop()

skill_tags = sorted(
    {
        tag.strip().lower()
        for item in opportunities
        for tag in (item.get("skills") or "").split(";")
        if tag.strip()
    }
)

default_profile = PROFILE_PRESETS[DEFAULT_PROFILE_NAME]
if "quick_start" not in st.session_state:
    st.session_state["quick_start"] = PROFILE_LABELS[DEFAULT_PROFILE_NAME]
for field, value in default_profile.items():
    if field not in st.session_state:
        st.session_state[field] = value.copy() if isinstance(value, list) else value

api_key, _ = _load_gemini_config()
gemini_available = bool(api_key)
if not gemini_available:
    st.session_state["use_ai"] = False
elif "use_ai" not in st.session_state:
    st.session_state["use_ai"] = True

with st.sidebar:
    st.subheader("Your preferences")
    quick_start_options = ["Custom"] + [
        PROFILE_LABELS[name] for name in PROFILE_PRESETS
    ]
    st.selectbox(
        "Quick start",
        options=quick_start_options,
        key="quick_start",
        help="Choose a preset to fill the form, or Custom to edit your own preferences.",
        on_change=_apply_preset,
    )

    with st.form("preferences_form"):
        st.selectbox(
            "Target track",
            options=sorted(ALLOWED_TRACKS),
            format_func=_format_track,
            key="target_track",
            help="The technology career track you want to explore.",
        )
        st.selectbox(
            "Preferred format",
            options=[None] + sorted(ALLOWED_FORMATS),
            format_func=_format_option,
            key="preferred_format",
            help="Choose a learning format, or Any format to keep all formats eligible.",
        )
        st.slider(
            "Skill level",
            min_value=0.0,
            max_value=1.0,
            step=0.05,
            key="skill_level",
            help="Estimate your current experience: 0 is beginner and 1 is advanced.",
        )
        st.caption("Beginner (0) · Intermediate (0.5) · Advanced (1)")
        st.toggle(
            "Prefer free options",
            key="prefers_free",
            help="When enabled, free and freemium opportunities receive a score bonus.",
        )
        st.toggle(
            "Require remote options",
            key="needs_remote",
            help="When enabled, non-remote opportunities are filtered out.",
        )
        st.number_input(
            "Hours available per week",
            min_value=0.0,
            max_value=100.0,
            step=1.0,
            key="max_hours",
            help="Your available weekly learning time; this is a ranking preference, not a hard cap.",
        )
        st.multiselect(
            "Interests",
            options=skill_tags,
            key="interests",
            help="Select skill tags that match your interests.",
        )
        use_ai = st.toggle(
            "Use AI (Gemini)",
            key="use_ai",
            disabled=not gemini_available,
            help="When enabled, learning preferences and retrieved opportunities are sent to Google Gemini.",
        )
        if not gemini_available:
            st.caption("ℹ AI unavailable — using rule-based path.")
        submitted = st.form_submit_button("Find my route", type="primary")

    st.caption(
        "No login is required. Your profile and route remain in this session."
    )

if submitted:
    profile = {
        "target_track": st.session_state["target_track"],
        "preferred_format": st.session_state["preferred_format"],
        "skill_level": st.session_state["skill_level"],
        "prefers_free": st.session_state["prefers_free"],
        "needs_remote": st.session_state["needs_remote"],
        "max_hours": st.session_state["max_hours"],
        "interests": list(st.session_state["interests"]),
    }
    try:
        with st.spinner("Finding your route..."):
            with redirect_stdout(StringIO()):
                result = run_pipeline(
                    profile,
                    offline=not use_ai,
                    opportunities=opportunities,
                )
        st.session_state["route_result"] = result
        st.session_state["route_profile"] = profile
        st.session_state.pop("route_error", None)
    except PipelineValidationError as error:
        st.session_state.pop("route_result", None)
        st.session_state["route_error"] = f"⚠ Validation error — {error}"
    except (OSError, UnicodeError, csv.Error, ValueError) as error:
        logger.error("pipeline_failed reason=%s", type(error).__name__)
        st.session_state.pop("route_result", None)
        st.session_state["route_error"] = (
            "⚠ Could not build a route. Check the profile values and dataset, "
            "then try again."
        )

if st.session_state.get("route_error"):
    st.markdown(f"**{st.session_state['route_error']}**")

path_tab, recommendations_tab, privacy_tab = st.tabs(
    ["Learning Path", "Recommendations", "How it works & privacy"]
)

with path_tab:
    result = st.session_state.get("route_result")
    if result is None:
        st.write("Choose your preferences and select **Find my route** to begin.")
    else:
        source_label = result["source_label"]
        if source_label.startswith("Source: Gemini (verified"):
            verification = (
                source_label.removeprefix("Source: Gemini (")
                .removesuffix(")")
            )
            st.markdown(
                '<p class="techroute-verified">✓ AI-generated '
                f"({escape(verification)})</p>",
                unsafe_allow_html=True,
            )
        else:
            reason = escape(result["fallback_reason"] or "unspecified")
            st.markdown(
                '<p class="techroute-fallback">↺ Rule-based fallback — '
                f"reason: {reason}</p>",
                unsafe_allow_html=True,
            )

        opportunities_by_title = {}
        for opportunity in opportunities:
            opportunities_by_title.setdefault(opportunity["title"], opportunity)
        for step in result["learning_path"]["steps"]:
            with st.container(border=True):
                st.subheader(f"{step['step_number']}. {step['stage']}")
                st.write(step["goal"])
                titles = step["opportunity_titles"]
                if titles:
                    for title in titles:
                        opportunity = opportunities_by_title.get(title)
                        if opportunity is not None:
                            _render_opportunity(opportunity)
                elif step["stage"] == "Apply":
                    st.write(
                        "No internship or job opportunities are available in "
                        "the retrieved data for this route."
                    )
                else:
                    st.write("No retrieved opportunities were assigned to this stage.")
                st.markdown("**Why**")
                st.write(step["why"])

        with st.expander("How the AI built this path"):
            trace_lines = format_agent_trace(
                result["learning_path"].get("trace", [])
            )
            if trace_lines:
                for line in trace_lines:
                    st.write(line)
            else:
                st.write("No agent trace is available for this route.")

with recommendations_tab:
    result = st.session_state.get("route_result")
    if result is None:
        st.write("Your ranked opportunities will appear here after a search.")
    else:
        profile = st.session_state["route_profile"]
        if profile["needs_remote"] is True:
            st.write(
                "ℹ Remote filter: non-remote opportunities were removed before ranking."
            )
        for rank, (opportunity, score, explanation) in enumerate(
            result["recommendations"], start=1
        ):
            with st.container(border=True):
                st.subheader(f"{rank}. {opportunity['title']}")
                st.write(
                    f"Provider: {opportunity['provider']} · Score: {score:.2f}"
                )
                with st.expander("Why this score"):
                    st.write(explanation)
                    if "Penalty -1.0: requires prior experience" in explanation:
                        st.write(
                            "↘ Prerequisite penalty: this opportunity requires prior experience."
                        )

with privacy_tab:
    st.subheader("How recommendations are generated")
    st.write(
        "TechRoute validates your learning preferences, applies the existing "
        "remote and prerequisite guardrails, and ranks opportunities from the "
        "curated dataset. When AI is enabled, Gemini creates a path using "
        "retrieved opportunities only. TechRoute verifies the returned titles; "
        "if the response cannot be used, it shows a rule-based fallback and reason."
    )
    st.subheader("Privacy")
    st.write(
        "No login is required. The app uses learning preferences and does not "
        "save your submitted profile or route. Existing operational logs are "
        "the only app data written to disk. When AI is on, learning preferences "
        "and retrieved opportunity details are sent to Google Gemini. With AI "
        "off, no Gemini request is made."
    )
    st.subheader("Accessibility and color contrast")
    st.write(
        "Text uses blue or orange status styling together with explicit labels "
        "and symbols; color is never the only status cue. The interface uses "
        "native Streamlit controls for keyboard operation."
    )
    st.caption("Measured color pairs (foreground on background):")
    st.write(
        "- Body text #17324D on page #F5F8FC: **12.32:1**\n"
        "- White text #FFFFFF on primary blue #0B4F71: **8.86:1**\n"
        "- Blue #0B4F71 on light blue #EAF1F6: **7.76:1**\n"
        "- Orange #873F0A on peach #FBE4D5: **6.25:1**\n"
        "- Card border #64788C on white #FFFFFF: **4.56:1**"
    )

result = st.session_state.get("route_result")
if result is not None:
    pdf_bytes = build_pdf(
        st.session_state["route_profile"],
        result["recommendations"],
        result["learning_path"],
        result["source_label"],
        result["fallback_reason"],
        opportunities=opportunities,
    )
    st.download_button(
        "Download my route (PDF)",
        data=pdf_bytes,
        file_name=f"techroute-learning-path-{date.today().isoformat()}.pdf",
        mime="application/pdf",
        help="Download a personal copy. The PDF is generated in memory and is not saved by TechRoute.",
    )
