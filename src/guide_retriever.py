"""Load and rank track-guide sections for retrieval-augmented generation."""

import logging
import re
from pathlib import Path
from typing import Dict, List, Optional, Set

GUIDE_DIR = Path(__file__).resolve().parents[1] / "data" / "track_guides"
STAGE_SECTION = "What each stage means for this track"
EXPECTED_STAGES = ("Foundations", "Build Skills", "Prove Skills", "Apply")
MAX_GUIDE_SECTIONS = 3
MAX_GUIDE_CHARACTERS = 1500
SECTION_HEADER = re.compile(r"^##\s+(.+?)\s*$")
TOKEN_PATTERN = re.compile(r"[a-z0-9]+")
logger = logging.getLogger("techroute")

GuideSection = Dict[str, str]


def _tokens(text: str) -> Set[str]:
    return set(TOKEN_PATTERN.findall(text.casefold()))


def load_guide_sections(
    target_track: Optional[str],
    guide_dir: Path = GUIDE_DIR,
) -> List[GuideSection]:
    """Load all named sections from one track guide, or return an empty list."""
    if not isinstance(target_track, str) or not re.fullmatch(
        r"[a-z0-9_]+", target_track
    ):
        logger.info("guide_missing target_track=%s", target_track or "unspecified")
        return []

    guide_path = guide_dir / f"{target_track}.md"
    try:
        contents = guide_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        logger.info("guide_missing target_track=%s", target_track)
        return []
    except (OSError, UnicodeError) as error:
        logger.warning(
            "guide_load_failed target_track=%s reason=%s",
            target_track,
            type(error).__name__,
        )
        return []

    sections: List[GuideSection] = []
    current_name = None
    current_lines: List[str] = []
    for line in contents.splitlines():
        match = SECTION_HEADER.match(line)
        if match:
            if current_name is not None:
                body = "\n".join(current_lines).strip()
                if body:
                    sections.append({"name": current_name, "content": body})
            current_name = match.group(1).strip()
            current_lines = []
        elif current_name is not None:
            current_lines.append(line)
    if current_name is not None:
        body = "\n".join(current_lines).strip()
        if body:
            sections.append({"name": current_name, "content": body})
    return sections


def retrieve_guide_sections(
    profile: Dict[str, object],
    guide_dir: Path = GUIDE_DIR,
) -> List[GuideSection]:
    """Return up to three relevant sections within the guide context budget."""
    sections = load_guide_sections(profile.get("target_track"), guide_dir)
    if not sections:
        return []

    interest_values = profile.get("interests", [])
    interests = [
        value.replace("_", " ")
        for value in interest_values
        if isinstance(value, str)
    ] if isinstance(interest_values, list) else []
    interest_terms = set()
    for interest in interests:
        interest_terms.update(_tokens(interest))
    stage_terms = _tokens(" ".join(EXPECTED_STAGES))
    keywords = interest_terms | stage_terms

    scored = []
    for index, section in enumerate(sections):
        section_terms = _tokens(f"{section['name']} {section['content']}")
        score = len(keywords & section_terms)
        scored.append((score, index, section))
    ranked = sorted(scored, key=lambda item: (-item[0], item[1]))

    stage_item = next(
        (item for item in ranked if item[2]["name"] == STAGE_SECTION),
        None,
    )
    other_section_count = MAX_GUIDE_SECTIONS - (1 if stage_item else 0)
    selected = [item for item in ranked if item[2]["name"] != STAGE_SECTION][
        :other_section_count
    ]
    if stage_item is not None:
        selected.append(stage_item)
    selected.sort(key=lambda item: (-item[0], item[1]))

    limited: List[GuideSection] = []
    remaining = MAX_GUIDE_CHARACTERS
    for _, _, section in selected:
        heading_size = len(section["name"]) + len("## \n")
        available = remaining - heading_size
        if available <= 0:
            continue
        content = section["content"][:available].rstrip()
        if not content:
            continue
        limited.append({"name": section["name"], "content": content})
        remaining -= heading_size + len(content)
    return limited


def core_skill_terms(target_track: str, guide_dir: Path = GUIDE_DIR) -> List[str]:
    """Read the semicolon-separated core-skill terms from a track guide."""
    core_section = next(
        (
            section
            for section in load_guide_sections(target_track, guide_dir)
            if section["name"] == "Core skills"
        ),
        None,
    )
    if core_section is None:
        return []
    return [
        re.sub(r"^[^\w]+|[^\w]+$", "", term.strip())
        for term in core_section["content"].replace("\n", " ").split(";")
        if term.strip()
    ]
