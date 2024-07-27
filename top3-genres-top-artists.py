import spotipy
from spotipy.oauth2 import SpotifyOAuth
from collections import Counter

# Initialize Spotipy with user authorization
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="cea88769eddc49e0b7f7ed76ee197517",
                                               client_secret="a7c55ba17fc94e7584175a25c93c2174",
                                               redirect_uri="http://localhost:8080",
                                               scope="user-top-read"))

def get_top_artists(sp, limit):
    results = sp.current_user_top_artists(limit=limit)
    artists = results['items']
    
    # while results['next']:
    #     results = sp.next(results)
    #     artists.extend(results['items'])
    
    return artists

def get_genres_from_artists(sp, artists):
    genres = []
    for artist in artists:
        genres.extend(artist['genres'])
    
    return genres

def get_top_genres(genres, top_n):
    genre_counts = Counter(genres)
    top_genres = genre_counts.most_common(top_n)
    top_genre_names = [genre for genre, count in top_genres]
    
    return top_genre_names

# Fetch the user's top artists
top_artists = get_top_artists(sp, limit=50)

# Extract genres from those artists
genres = get_genres_from_artists(sp, top_artists)

# Determine the top 3 genres
top_genres = get_top_genres(genres, top_n=3)

# Print the top 3 genres
print("\nTop 3 Genres:")
print(top_genres)