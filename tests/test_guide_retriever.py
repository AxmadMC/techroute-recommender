import logging
from pathlib import Path

from src.guide_retriever import (
    MAX_GUIDE_CHARACTERS,
    STAGE_SECTION,
    core_skill_terms,
    retrieve_guide_sections,
)


def test_retriever_selects_matching_guide_and_respects_character_budget(tmp_path):
    software_guide = tmp_path / "software_engineering.md"
    networking_guide = tmp_path / "networking.md"
    software_guide.write_text(
        "Curated by Ahmed Ali.\n"
        "## Overview\n"
        + ("Software engineering python practice. " * 30)
        + "\n## Core skills\n"
        + ("Python programming and testing. " * 30)
        + f"\n## {STAGE_SECTION}\n"
        + ("Foundations Build Skills Prove Skills Apply. " * 30),
        encoding="utf-8",
    )
    networking_guide.write_text(
        "## Overview\nNetworking-only marker.\n"
        f"## {STAGE_SECTION}\nNetworking stages.",
        encoding="utf-8",
    )

    sections = retrieve_guide_sections(
        {
            "target_track": "software_engineering",
            "interests": ["python"],
        },
        guide_dir=tmp_path,
    )

    assert len(sections) <= 3
    assert any(section["name"] == STAGE_SECTION for section in sections)
    assert any(section["name"] == "Core skills" for section in sections)
    assert all("Networking-only marker" not in section["content"] for section in sections)
    skill_terms = core_skill_terms("software_engineering", tmp_path)
    assert len(skill_terms) == 1
    assert skill_terms[0].endswith("testing")
    assert sum(
        len(section["name"]) + len("## \n") + len(section["content"])
        for section in sections
    ) <= MAX_GUIDE_CHARACTERS


def test_retriever_returns_no_sections_and_logs_when_guide_is_missing(
    tmp_path, caplog
):
    caplog.set_level(logging.INFO, logger="techroute")
    sections = retrieve_guide_sections(
        {"target_track": "networking", "interests": ["routing"]},
        guide_dir=Path(tmp_path),
    )

    assert sections == []
    assert "guide_missing target_track=networking" in caplog.text
