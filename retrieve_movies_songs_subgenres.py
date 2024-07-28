import spotipy
from spotipy.oauth2 import SpotifyOAuth
import csv

def initialize_spotify(client_id, client_secret, redirect_uri, scope):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                   client_secret=client_secret,
                                                   redirect_uri=redirect_uri,
                                                   scope=scope))
    return sp

def get_song_genres(sp, song_name):
    print(song_name)
    results = sp.search(q=song_name, type='track', limit=1)
    if results['tracks']['items']:
        track = results['tracks']['items'][0]
        artist_id = track['artists'][0]['id']
        artist = sp.artist(artist_id)
        return artist['genres']
    return ["Unknown"]

def add_genres_to_csv(input_csv_path, output_csv_path, sp):
    with open(input_csv_path, mode='r', encoding='utf-8-sig') as infile, \
         open(output_csv_path, mode='w', newline='', encoding='utf-8-sig') as outfile:
        
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        header = next(reader)  # Read the header row
        header.append('song_subgenre')  # Add a new column for genres
        writer.writerow(header)
        
        for row in reader:
            song_name = row[1]
            genres = get_song_genres(sp, song_name)
            row.append(', '.join(genres))
            writer.writerow(row)

def main():
    # Parameters for Spotipy
    client_id = "aa64f02127614f099dc0d4be625c7269"
    client_secret = "d6374a15263c446aa9602b3c0c7ab12c"
    redirect_uri = "http://localhost:8888"
    scope = "user-top-read"
    
    # Initialize Spotify
    sp = initialize_spotify(client_id, client_secret, redirect_uri, scope)
    
    # Paths to input and output CSV files
    input_csv_path = 'csv_files/movies.csv'
    output_csv_path = 'csv_files/movies_songs_subgenres.csv'
    
    # Add genres to CSV
    add_genres_to_csv(input_csv_path, output_csv_path, sp)

# Call the main function
if __name__ == "__main__":
    main()
