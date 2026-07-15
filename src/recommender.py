import csv
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass

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
        """Initialize the recommender with a list of songs."""
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top-k songs for a user using the current recommendation logic."""
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a short explanation for why a song is recommended to a user."""
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict[str, Any]]:
    """Load songs from a CSV file and return them as a list of dictionaries."""
    path = Path(csv_path)
    if not path.is_absolute():
        path = Path(__file__).resolve().parent.parent / path

    with open(path, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        songs = []
        for row in reader:
            song = {
                "id": int(row["id"]),
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "mood": row["mood"],
                "energy": float(row["energy"]),
                "tempo_bpm": float(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            }
            songs.append(song)

    print(f"Loaded songs: {len(songs)}")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a single song against a user preference profile and return the score with reasons."""
    # Feature weights (priority order: genre, mood, energy, acousticness)
    weights = {
        "genre": 0.40,
        "mood": 0.25,
        "energy": 0.20,
        "acousticness": 0.15,
    }

    reasons: List[str] = []

    # Helper for numeric similarity in [0,1]
    def num_sim(s_val: float, u_val: float) -> float:
        return max(0.0, 1.0 - abs(s_val - u_val))

    total = 0.0

    # Genre (categorical exact match)
    user_genre = user_prefs.get("genre")
    if user_genre is not None and song.get("genre") == user_genre:
        contrib = weights["genre"] * 1.0
        reasons.append(f"genre match (+{contrib:.2f})")
    else:
        contrib = 0.0
        reasons.append(f"genre mismatch (+{contrib:.2f})")
    total += contrib

    # Mood (categorical exact match)
    user_mood = user_prefs.get("mood")
    if user_mood is not None and song.get("mood") == user_mood:
        contrib = weights["mood"] * 1.0
        reasons.append(f"mood match (+{contrib:.2f})")
    else:
        contrib = 0.0
        reasons.append(f"mood mismatch (+{contrib:.2f})")
    total += contrib

    # Energy (numeric, assumed in [0,1])
    if "energy" in user_prefs and song.get("energy") is not None:
        sim = num_sim(float(song["energy"]), float(user_prefs["energy"]))
        contrib = weights["energy"] * sim
        reasons.append(f"energy similarity {sim:.2f} -> +{contrib:.2f}")
        total += contrib

    # Acousticness (numeric, assumed in [0,1])
    if "acousticness" in user_prefs and song.get("acousticness") is not None:
        sim = num_sim(float(song["acousticness"]), float(user_prefs["acousticness"]))
        contrib = weights["acousticness"] * sim
        reasons.append(f"acousticness similarity {sim:.2f} -> +{contrib:.2f}")
        total += contrib

    # Ensure score is within [0,1]
    score = min(max(total, 0.0), 1.0)
    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Return the top-k songs ranked by their similarity to the user's taste profile."""
    # Score each song using score_song, then sort by score desc and return top-k
    scored: List[Tuple[Dict, float, str]] = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons)
        scored.append((song, score, explanation))

    # Sort by score descending
    scored.sort(key=lambda tup: tup[1], reverse=True)

    # Return top k (or all if fewer)
    return scored[:k]
