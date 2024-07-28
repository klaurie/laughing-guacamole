import database
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from collections import Counter
import csv

# Creating an instance of the database class
db = database.mongoData()

def init_database():
    db.connect()
    db.select_collection('laughing-guacamole', 'movies')
    db.remove_all()
    db.create(dbset)
    db.disconnect()

# Uncomment this if you need to initialize the database
# init_database()

# Connecting to the database
db.connect()

# Selects the collection 'movies'
db.select_collection('laughing-guacamole', 'movies')

# Export the DataFrame to a CSV file
csv_file_path = 'output.csv'
df.to_csv(csv_file_path, index=False)
# Close the connection
db.disconnect()