"""Generate real Gemini agent traces for the three evidence profiles."""

import json
import logging
from contextlib import redirect_stdout
from datetime import date
from io import StringIO
from pathlib import Path
import sys
import time

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.path_generator import (
    DEFAULT_MODEL,
    _load_gemini_config,
    generate_learning_path,
)
from src.profiles import PROFILE_PRESETS
from src.recommender import load_opportunities

PROFILE_NAMES = (
    "ai_engineering_student",
    "cloud_career_changer",
    "software_engineering_student",
)
COMMAND = "python scripts/generate_agent_traces.py"
OUTPUT_PATH = PROJECT_ROOT / "assets" / "agent_traces.md"
CALL_PAUSE_SECONDS = 1.0


def main() -> int:
    api_key, model = _load_gemini_config()
    if not api_key:
        raise SystemExit(
            "GEMINI_API_KEY must be configured to generate real agent traces."
        )
    if not model:
        model = DEFAULT_MODEL
    del api_key

    logger = logging.getLogger("techroute")
    logger.addHandler(logging.NullHandler())
    logger.propagate = False

    with redirect_stdout(StringIO()):
        opportunities = load_opportunities(
            str(PROJECT_ROOT / "data" / "opportunities.csv")
        )

    traces = []
    for index, name in enumerate(PROFILE_NAMES):
        if index:
            time.sleep(CALL_PAUSE_SECONDS)
        result = generate_learning_path(PROFILE_PRESETS[name], opportunities)
        if not str(result["source"]).startswith("Source: Gemini (verified"):
            raise RuntimeError(
                f"Agent trace generation did not produce a verified Gemini path "
                f"for {name}: {result['source']}"
            )
        traces.append((name, result["trace"]))

    sections = [
        "# Agentic Workflow Traces",
        "",
        f"- Command: `{COMMAND}`",
        f"- Date: {date.today().isoformat()}",
        f"- Model: `{model}`",
        "",
        "Each fenced block contains the in-memory trace returned by a real "
        "Gemini-backed run; no API key or full profile is included.",
    ]
    for name, trace in traces:
        sections.extend(
            [
                "",
                f"## {name}",
                "",
                "```json",
                json.dumps(trace, ensure_ascii=False, indent=2),
                "```",
            ]
        )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text("\n".join(sections) + "\n", encoding="utf-8")
    print(f"Wrote real agent traces to assets/agent_traces.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
