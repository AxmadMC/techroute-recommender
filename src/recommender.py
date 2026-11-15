import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict

# Scoring weights (Algorithm Recipe)
GENRE_WEIGHT = 2.0
MOOD_WEIGHT = 1.0
ACOUSTIC_BONUS = 0.5
ACOUSTIC_THRESHOLD = 0.5  # a song counts as "acoustic" if acousticness >= this

NO_MATCH_EXPLANATION = "No strong matches with your preferences."

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Returns the top k songs for the user, highest score first."""
        prefs = _profile_to_prefs(user)
        ranked = sorted(
            self.songs,
            key=lambda song: score_song(prefs, asdict(song))[0],
            reverse=True,
        )
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Returns a human-readable explanation of why the song was scored as it was."""
        _, reasons = score_song(_profile_to_prefs(user), asdict(song))
        return _build_explanation(reasons)

def _profile_to_prefs(user: UserProfile) -> Dict:
    """Converts a UserProfile into the user_prefs dict used by score_song."""
    return {
        "genre": user.favorite_genre,
        "mood": user.favorite_mood,
        "energy": user.target_energy,
        "likes_acoustic": user.likes_acoustic,
    }

def _normalize(value: Optional[str]) -> str:
    """Lowercases and strips a string so comparisons ignore case and whitespace."""
    return (value or "").strip().lower()

def _build_explanation(reasons: List[str]) -> str:
    """Joins scoring reasons into a single explanation string."""
    if not reasons:
        return NO_MATCH_EXPLANATION
    return "; ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    print(f"Loading songs from {csv_path}...")
    float_fields = ["energy", "tempo_bpm", "valence", "danceability", "acousticness"]
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            row["id"] = int(row["id"])
            for field in float_fields:
                row[field] = float(row[field])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    score = 0.0
    reasons: List[str] = []

    genre = user_prefs.get("genre")
    if genre and _normalize(genre) == _normalize(song.get("genre")):
        score += GENRE_WEIGHT
        reasons.append(f"genre matches '{song['genre']}' (+{GENRE_WEIGHT:.2f})")

    mood = user_prefs.get("mood")
    if mood and _normalize(mood) == _normalize(song.get("mood")):
        score += MOOD_WEIGHT
        reasons.append(f"mood matches '{song['mood']}' (+{MOOD_WEIGHT:.2f})")

    target_energy = user_prefs.get("energy")
    if target_energy is not None and song.get("energy") is not None:
        similarity = 1 - abs(target_energy - song["energy"])
        score += similarity
        reasons.append(
            f"energy {song['energy']:.2f} is close to your target {target_energy:.2f} (+{similarity:.2f})"
        )

    if user_prefs.get("likes_acoustic") and song.get("acousticness", 0) >= ACOUSTIC_THRESHOLD:
        score += ACOUSTIC_BONUS
        reasons.append(f"acoustic sound you prefer (+{ACOUSTIC_BONUS:.2f})")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, _build_explanation(reasons)))
    scored.sort(key=lambda item: item[1], reverse=True)
    return scored[:k]
