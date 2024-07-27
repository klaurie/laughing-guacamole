import database
from topmovies import dbset

# Creating an instance of the database class
db = database.mongoData()

def init_database():
    db.connect()
    db.select_collection('laughing-guacamole', 'movies')
    db.remove_all()
    db.create(dbset)
    db.disconnect()

# init_database()

# # Connecting to the database
# db.connect()

# # Selects the collection 'movies'
# db.select_collection('laughing-guacamole', 'movies')

# # Reading the example data
# db.read()

# # Adding some example data
# db.create()

# # Update documents
# db.update({"title": "Inception"}, {"$set": {"year": 2011}})

# # Remove documents
# db.delete({"title": "The Godfather"})

# # Reads all of the collections within the database
# db.read_all()

# # Close the connection
# db.disconnect()