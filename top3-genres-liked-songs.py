import spotipy
from spotipy.oauth2 import SpotifyOAuth
from collections import Counter

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="cea88769eddc49e0b7f7ed76ee197517",
                                               client_secret="a7c55ba17fc94e7584175a25c93c2174",
                                               redirect_uri="http://localhost:8080",
                                               scope="user-library-read"))

def get_all_saved_tracks(sp):
    results = sp.current_user_saved_tracks()
    tracks = results['items']
    
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    
    return tracks

def get_genres_from_tracks(sp, tracks):
    genres = []
    for item in tracks:
        track = item['track']
        artist_id = track['artists'][0]['id']
        artist = sp.artist(artist_id)
        genres.extend(artist['genres'])
    
    return genres

def get_top_genres(genres, top_n):
    genre_counts = Counter(genres)
    top_genres = genre_counts.most_common(top_n)
    top_genre_names = [genre for genre, count in top_genres]
    
    return top_genre_names

# Fetch all liked tracks
all_tracks = get_all_saved_tracks(sp)

# results = sp.current_user_saved_tracks()
# all_tracks = results['items']

# Extract genres from those tracks
genres = get_genres_from_tracks(sp, all_tracks)

# # Determine the top 3 genres
top_genres = get_top_genres(genres, top_n=3)

# Print the top 3 genres
print("\nTop 3 Genres:")
print(top_genres)