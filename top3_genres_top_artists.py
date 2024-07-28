import spotipy
from spotipy.oauth2 import SpotifyOAuth
from collections import Counter
import csv

# Load the CSV file and create a dictionary that maps subgenres to their genres
def map_subgenre_to_genre(csv_file_path):
    genres_dict = {}
    with open(csv_file_path, mode='r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        for row in csv_reader:
            genre, subgenre = row
            genres_dict[subgenre] = genre
    
    return genres_dict
    
# Initialize Spotipy with user authorization
def auth_spotify(client_id, client_secret, redirect_uri, scope):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope=scope))
    return sp

# Fetch all top artists
def get_top_artists(sp, limit=50):
    results = sp.current_user_top_artists(limit=limit)
    artists = results['items']
    
    while results['next']:
        results = sp.next(results)
        artists.extend(results['items'])
    
    return artists

# Extract genres from the artists
def get_genres_from_artists(artists):
    genres = []
    for artist in artists:
        genres.extend(artist['genres'])
    
    return genres

# Convert subgenres to main genres
def convert_to_genre(subgenres, mapping):
    genres = [mapping.get(subgenre, "unknown") for subgenre in subgenres]
    
    return genres

# Retrieve top 3 genres
def get_top_genres(genres, mapping, n):
    main_genres = convert_to_genre(genres, mapping)
    # print()
    # print(main_genres)
    filtered_genres = [genre for genre in main_genres if genre != "unknown"]
    genre_counts = Counter(filtered_genres)
    top_genres = genre_counts.most_common(n)
    top_genre_names = [genre for genre, count in top_genres]
    
    return top_genre_names

def get_top_genre_with_top_subgenres(genres, mapping, n):
    top_genre = get_top_genres(genres, mapping, 1)[0]
    subgenres = [subgenre for subgenre, main_genre in mapping.items() if main_genre == top_genre]
    top_genre_subgenres = [genre for genre in genres if genre in subgenres]
    subgenre_counts = Counter(top_genre_subgenres)
    top_subgenres = subgenre_counts.most_common(n)
    top_subgenre_names = [subgenre for subgenre, count in top_subgenres]
    
    return [top_genre] + top_subgenre_names


def top_3_genres():

    # Authorization code flow for Spotify
    client_id = "cea88769eddc49e0b7f7ed76ee197517"
    client_secret = "a7c55ba17fc94e7584175a25c93c2174"
    redirect_uri = "http://localhost:8080"
    scope = "user-top-read"

    csv_fp = "csv_files/genres.csv"
    genres_dict = map_subgenre_to_genre(csv_fp)
    sp = auth_spotify(client_id, client_secret, redirect_uri, scope)
    top_artists = get_top_artists(sp)
    subgenres = get_genres_from_artists(top_artists)
    # print(subgenres)
    result = get_top_genres(subgenres, genres_dict, 3)

    # Return a list: ['genre 1', 'genre 2', 'genre 3']
    return result

def top_genre_with_top_3_subgenres():
    # Authorization code flow for Spotify
    client_id = "cea88769eddc49e0b7f7ed76ee197517"
    client_secret = "a7c55ba17fc94e7584175a25c93c2174"
    redirect_uri = "http://localhost:8080"
    scope = "user-top-read"

    csv_fp = "csv_files/genres.csv"
    genres_dict = map_subgenre_to_genre(csv_fp)
    sp = auth_spotify(client_id, client_secret, redirect_uri, scope)
    top_artists = get_top_artists(sp)
    subgenres = get_genres_from_artists(top_artists)
    result = get_top_genre_with_top_subgenres(subgenres, genres_dict, 3)

    # Return a list: ['genre 1', 'sub genre 1', 'sub genre 2', 'sub genre 3']
    return result

print(top_3_genres())

print(top_genre_with_top_3_subgenres())