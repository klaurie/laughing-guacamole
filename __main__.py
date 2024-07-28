import database
import json
from topmovies import movieDBset, songDBset

# Creating an instance of the database class
db = database.mongoData()

def init_database():
    db.connect()
    db.select_collection('laughing-guacamole', 'moviesandsongs')
    db.delete_all()
    db.create(songDBset)
    #db.delete({"performed_by": "NA"})
    #db.remove_uncredited()
    db.disconnect()

# init_database()

# Connecting to the database
db.connect()

# Selects the collection 'movies'
db.select_collection('laughing-guacamole', 'movies')

# text_file = open("output.txt", "w")

# text_file.write(f"[\n")

# for item in db.join_collections_on_title('laughing-guacamole', 'moviesandsongs'):
#     text_file.write(str(item))
#     text_file.write("\n")

# text_file.write(f"]")

# text_file.close

# Reading the example data
# db.read()

# Adding some example data
# db.create()

# Update documents
# db.update({"title": "Inception"}, {"$set": {"year": 2011}})

# Remove documents
# db.delete({"title": "The Godfather"})

# Reads all of the collections within the database
# db.read_all()

# Close the connection
db.disconnect()