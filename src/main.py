"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def print_recommendations(title: str, recommendations: list) -> None:
    """Print a clean, readable list of song recommendations."""
    print(f"\n{title}:\n")
    for index, rec in enumerate(recommendations, start=1):
        song, score, explanation = rec
        print(f"{index}. {song['title']}")
        print(f"   Artist: {song['artist']}")
        print(f"   Score: {score:.3f}")
        print("   Reasons:")
        for reason in explanation.split("; "):
            print(f"     - {reason}")
        print()


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # Example taste profile for content-based recommendations
    user_prefs_1 = {
    "genre": "rock",
    "mood": "sad",
    "energy": 0.8,
    "acousticness": 0.2
}

    user_prefs_2 = {
    "genre": "zzzz_unknown",
    "mood": "zzzz_unknown",
    "energy": 0.5,
    "acousticness": 0.5
}

    user_prefs_3 = {
    "genre": "pop",
    "mood": "happy",
    "energy": 1.5,
    "acousticness": -0.2
}
    
    user_prefs_4 = {
    "genre": "pop",
    "mood": "happy",
    "energy": 0.0,
    "acousticness": 1.0
}
    
    user_prefs_5 = {
    "genre": "rock",
    "mood": "chill",
    "energy": 0.9,
    "acousticness": 0.1
}
    
    user_prefs_6 = {
    "genre": "pop",
    "mood": "happy",
    "energy": 0.5,
    "acousticness": 0.5
}

    recommendations_1 = recommend_songs(user_prefs_1, songs, k=5)
    recommendations_2 = recommend_songs(user_prefs_2, songs, k=5)
    recommendations_3 = recommend_songs(user_prefs_3, songs, k=5)
    recommendations_4 = recommend_songs(user_prefs_4, songs, k=5)
    recommendations_5 = recommend_songs(user_prefs_5, songs, k=5)
    recommendations_6 = recommend_songs(user_prefs_6, songs, k=5)


    print_recommendations("Profile 1 recommendations", recommendations_1)
    print_recommendations("Profile 2 recommendations", recommendations_2)
    print_recommendations("Profile 3 recommendations", recommendations_3)
    print_recommendations("Profile 4 recommendations", recommendations_4)
    print_recommendations("Profile 5 recommendations", recommendations_5)
    print_recommendations("Profile 6 recommendations", recommendations_6)



if __name__ == "__main__":
    main()
