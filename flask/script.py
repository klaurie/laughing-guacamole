from flask import Flask, jsonify, request
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from collections import Counter
import csv

app = Flask(__name__)

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
    filtered_genres = [genre for genre in main_genres if genre != "unknown"]
    genre_counts = Counter(filtered_genres)
    top_genres = genre_counts.most_common(n)
    top_genre_names = [genre for genre, count in top_genres]
    
    return top_genre_names

@app.route('/', methods=['GET'])
def test():
    return jsonify({'message': 'success'})

@app.route('/top_genres', methods=['GET'])
def top_genres():
    data = request.json
    access_token = data.get('access_token')
    csv_fp = "csv_files/genres.csv"
    genres_dict = map_subgenre_to_genre(csv_fp)
    
    sp = spotipy.Spotify(auth=access_token)
    top_artists = get_top_artists(sp)
    subgenres = get_genres_from_artists(top_artists)
    result = get_top_genres(subgenres, genres_dict, 3)
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(port=5000)
