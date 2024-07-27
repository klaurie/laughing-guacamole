import spotipy
from spotipy.oauth2 import SpotifyOAuth
from collections import Counter
import csv

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="cea88769eddc49e0b7f7ed76ee197517",
                                               client_secret="a7c55ba17fc94e7584175a25c93c2174",
                                               redirect_uri="http://localhost:8080",
                                               scope="user-library-read"))

# Load the CSV file and create a mapping dictionary
genres_dict = {}
csv_file_path = 'subgenres.csv'

with open(csv_file_path, mode='r', encoding='utf-8-sig') as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        genre, subgenre = row
        genres_dict[subgenre] = genre

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

def convert_to_genre(subgenres, mapping):
    genres = [mapping.get(subgenre, "unknown") for subgenre in subgenres]
    
    return genres

def get_top_genres(subgenres, top_n):
    genres = convert_to_genre(subgenres, genres_dict)
    # print()
    # print(genres)
    filtered_genres = [genre for genre in genres if genre != "unknown"]
    genre_counts = Counter(filtered_genres)
    top_genres = genre_counts.most_common(top_n)
    top_genre_names = [genre for genre, count in top_genres]

    return top_genre_names

# Fetch all liked tracks
# all_tracks = get_all_saved_tracks(sp)

results = sp.current_user_saved_tracks()
all_tracks = results['items']

# Extract genres from those tracks
subgenres = get_genres_from_tracks(sp, all_tracks)
# print(subgenres)

# Determine the top 3 genres
top3_genres = get_top_genres(subgenres, top_n=3)

# Print the top 3 genres
print("\nTop 3 Genres:")
print(top3_genres)