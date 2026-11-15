"""Shared sample profiles for the CLI and reliability evaluator."""

from typing import Dict, Tuple

Profile = Dict[str, object]

PROFILE_PRESETS: Dict[str, Profile] = {
    "it_support_beginner": {
        "target_track": "it_support",
        "preferred_format": "self_paced",
        "skill_level": 0.2,
        "prefers_free": True,
        "needs_remote": True,
        "max_hours": 10,
        "interests": ["hardware", "troubleshooting", "windows"],
    },
    "networking_student": {
        "target_track": "networking",
        "preferred_format": "project_based",
        "skill_level": 0.35,
        "prefers_free": True,
        "needs_remote": True,
        "max_hours": 8,
        "interests": ["networking", "ip_addressing", "packet_tracer"],
    },
    "cybersecurity_beginner": {
        "target_track": "cybersecurity",
        "preferred_format": "self_paced",
        "skill_level": 0.2,
        "prefers_free": True,
        "needs_remote": True,
        "max_hours": 5,
        "interests": ["security_fundamentals", "linux", "networking"],
    },
    "cloud_career_changer": {
        "target_track": "cloud_computing",
        "preferred_format": "self_paced",
        "skill_level": 0.3,
        "prefers_free": True,
        "needs_remote": True,
        "max_hours": 10,
        "interests": ["azure", "cloud", "linux"],
    },
    "ai_engineering_student": {
        "target_track": "ai_engineering",
        "preferred_format": "project_based",
        "skill_level": 0.35,
        "prefers_free": True,
        "needs_remote": True,
        "max_hours": 12,
        "interests": ["python", "machine_learning", "data_analysis"],
    },
    "software_engineering_student": {
        "target_track": "software_engineering",
        "preferred_format": "self_paced",
        "skill_level": 0.3,
        "prefers_free": True,
        "needs_remote": True,
        "max_hours": 20,
        "interests": ["python", "git"],
    },
}

PROFILE_LABELS: Dict[str, str] = {
    "it_support_beginner": "IT Support beginner",
    "networking_student": "Networking student",
    "cybersecurity_beginner": "Cybersecurity beginner",
    "cloud_career_changer": "Cloud career changer",
    "ai_engineering_student": "AI Engineering student",
    "software_engineering_student": "Software Engineering student",
}

DEFAULT_PROFILE_NAME = "software_engineering_student"
EVALUATION_PROFILE_NAMES: Tuple[str, ...] = (
    "it_support_beginner",
    "networking_student",
    "cybersecurity_beginner",
    "cloud_career_changer",
    "ai_engineering_student",
    "software_engineering_student",
)
