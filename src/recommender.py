import csv
from dataclasses import asdict, dataclass, field
from typing import Dict, List, Optional, Tuple

TRACK_WEIGHT = 2.0
FORMAT_WEIGHT = 1.0
DIFFICULTY_WEIGHT = 1.0
FREE_PRIORITY_WEIGHT = 1.0
REMOTE_WEIGHT = 0.5
TIME_WEIGHT = 0.5
INTEREST_WEIGHT = 0.5

NO_MATCH_EXPLANATION = "No strong matches with your preferences."


@dataclass
class Opportunity:
    """Represents an opportunity and its attributes."""

    id: int
    title: str
    provider: str
    category: str
    career_track: str
    format: Optional[str]
    difficulty: float
    hours_required: Optional[float]
    cost_type: str
    cost_usd: float
    remote: bool
    career_value: float
    skills: str
    eligibility: Optional[str]
    leads_to: str
    description: str
    url: str
    last_verified: Optional[str]


@dataclass
class UserProfile:
    """Represents a user's technology career preferences."""

    career_track: Optional[str] = None
    preferred_format: Optional[str] = None
    skill_level: float = 0.3
    max_hours: Optional[float] = None
    remote: Optional[bool] = None
    interests: List[str] = field(default_factory=list)


class Recommender:
    """OOP implementation of the recommendation logic."""

    def __init__(self, opportunities: List[Opportunity]):
        self.opportunities = opportunities

    def recommend(self, user: UserProfile, k: int = 5) -> List[Opportunity]:
        """Returns the top k opportunities for the user, highest score first."""
        prefs = _profile_to_prefs(user)
        ranked = sorted(
            self.opportunities,
            key=lambda opportunity: _rank_key(
                score_opportunity(prefs, asdict(opportunity))[0],
                asdict(opportunity),
            ),
            reverse=True,
        )
        return ranked[:k]

    def explain_recommendation(
        self, user: UserProfile, opportunity: Opportunity
    ) -> str:
        """Explains why an opportunity was scored as it was."""
        _, reasons = score_opportunity(_profile_to_prefs(user), asdict(opportunity))
        return _build_explanation(reasons)


def _profile_to_prefs(user: UserProfile) -> Dict:
    """Converts a UserProfile into the user_prefs dict used by score_opportunity."""
    return {
        "career_track": user.career_track,
        "format": user.preferred_format,
        "skill_level": user.skill_level,
        "max_hours": user.max_hours,
        "remote": user.remote,
        "interests": user.interests,
    }


def _normalize(value: Optional[str]) -> str:
    """Lowercases and strips a string so comparisons ignore case and whitespace."""
    return (value or "").strip().lower()


def _build_explanation(reasons: List[str]) -> str:
    """Joins scoring reasons into a single explanation string."""
    if not reasons:
        return NO_MATCH_EXPLANATION
    return "; ".join(reasons)


def _rank_key(score: float, opportunity: Dict) -> Tuple[float, int, float, int]:
    cost_rank = {"free": 2, "freemium": 1, "paid": 0}
    return (
        score,
        cost_rank.get(opportunity.get("cost_type"), 0),
        opportunity.get("career_value") or 0.0,
        -(opportunity.get("id") or 0),
    )


def load_opportunities(csv_path: str) -> List[Dict]:
    """Loads opportunities from a CSV file."""
    print(f"Loading opportunities from {csv_path}...")
    opportunities = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            row["id"] = int(row["id"])
            for field_name in ("difficulty", "cost_usd", "career_value"):
                row[field_name] = float(row[field_name])
            row["hours_required"] = (
                float(row["hours_required"]) if row["hours_required"] else None
            )
            remote_value = row["remote"].strip().lower()
            if remote_value not in {"true", "false"}:
                raise ValueError(
                    f"Invalid remote value for opportunity {row['id']}: "
                    f"{row['remote']!r}"
                )
            row["remote"] = remote_value == "true"
            for field_name in ("format", "eligibility", "last_verified"):
                row[field_name] = row[field_name] or None
            opportunities.append(row)
    return opportunities


def score_opportunity(
    user_prefs: Dict, opportunity: Dict
) -> Tuple[float, List[str]]:
    """Scores one opportunity against a user's career preferences."""
    score = 0.0
    reasons: List[str] = []

    career_track = user_prefs.get("career_track")
    if career_track:
        opportunity_track = _normalize(opportunity.get("career_track"))
        if _normalize(career_track) == opportunity_track:
            track_match = 1.0
        elif opportunity_track == "general":
            track_match = 0.5
        else:
            track_match = 0.0
        if track_match:
            points = TRACK_WEIGHT * track_match
            score += points
            reasons.append(f"career track match (+{points:.2f})")

    preferred_format = user_prefs.get("format")
    opportunity_format = opportunity.get("format")
    if preferred_format and opportunity_format:
        if _normalize(preferred_format) == _normalize(opportunity_format):
            score += FORMAT_WEIGHT
            reasons.append(f"format matches '{opportunity_format}' (+{FORMAT_WEIGHT:.2f})")

    skill_level = user_prefs.get("skill_level")
    difficulty = opportunity.get("difficulty")
    if skill_level is not None and difficulty is not None:
        similarity = 1 - abs(skill_level - difficulty)
        score += DIFFICULTY_WEIGHT * similarity
        reasons.append(f"difficulty fit (+{DIFFICULTY_WEIGHT * similarity:.2f})")

    free_priority = {"free": 1.0, "freemium": 0.5, "paid": 0.0}.get(
        opportunity.get("cost_type"), 0.0
    )
    score += FREE_PRIORITY_WEIGHT * free_priority
    if free_priority:
        reasons.append(f"free priority (+{FREE_PRIORITY_WEIGHT * free_priority:.2f})")

    preferred_remote = user_prefs.get("remote")
    opportunity_remote = opportunity.get("remote")
    if preferred_remote is not None and opportunity_remote is not None:
        if preferred_remote == opportunity_remote:
            score += REMOTE_WEIGHT
            reasons.append(f"remote preference match (+{REMOTE_WEIGHT:.2f})")

    max_hours = user_prefs.get("max_hours")
    hours_required = opportunity.get("hours_required")
    if max_hours is not None and hours_required is not None and hours_required > 0:
        time_fit = min(1.0, max_hours / hours_required)
        score += TIME_WEIGHT * time_fit
        reasons.append(f"time fit (+{TIME_WEIGHT * time_fit:.2f})")

    interests = {
        _normalize(interest)
        for interest in user_prefs.get("interests", [])
        if _normalize(interest)
    }
    skills = {
        _normalize(skill)
        for skill in (opportunity.get("skills") or "").split(";")
        if _normalize(skill)
    }
    if interests:
        interest_overlap = len(interests & skills) / len(interests)
        if interest_overlap:
            points = INTEREST_WEIGHT * interest_overlap
            score += points
            reasons.append(f"interest overlap (+{points:.2f})")

    return score, reasons


def recommend_opportunities(
    user_prefs: Dict, opportunities: List[Dict], k: int = 5
) -> List[Tuple[Dict, float, str]]:
    """Returns the top k opportunities with their scores and explanations."""
    scored = []
    for opportunity in opportunities:
        score, reasons = score_opportunity(user_prefs, opportunity)
        scored.append((opportunity, score, _build_explanation(reasons)))
    scored.sort(key=lambda item: _rank_key(item[1], item[0]), reverse=True)
    return scored[:k]
