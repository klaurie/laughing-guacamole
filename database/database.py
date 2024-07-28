import pymongo
from pymongo import MongoClient
from credentials import creds


#
# Python class to connect/disconnect and perform CRUD ops with a mongoDB database.
#
class mongoData():

    # Initializes some base variables, including the connection string and the client
    def __init__(self):
        self.connectstring = creds
        self.client = None
        self.db = None
        self.collection = None

    # Connects to the client. If there is no specified source, uses the default source
    def connect(self, source = None):
        if source is None:
            source = self.connectstring
        
        try:
            self.client = MongoClient(source)

        except pymongo.errors.ServerSelectionTimeoutError as err:
            print(f"Could not connect to MongoDB: {err}")

        except Exception as e:
            print(f"An error occurred: {e}")

        else:
            print(f"Connected successfully!")

    # Selects a collection. If there is no specified collection, defaults to 'movies' within 'laughing-guacamole'
    def select_collection(self, db = None, cl = None):
        
        if db is None:
            db = 'laughing-guacamole'
        if cl is None:
            cl = 'movies'

        self.db = self.client[db]
        self.collection = self.db[cl]

    # Disconnects from the client connection
    def disconnect(self):
        if self.client is not None:
            self.client.close
            print("Connection closed.")
        else:
            print("You never connected in the first place!")

    # Creates objects within the database
    def create(self, objects):
        result = self.collection.insert_many(objects)
        print(f"Created {len(result.inserted_ids)} documents.")

    # Reads all documents in the database
    def read_all(self):
        for collection_name in self.db.list_collection_names():
            print(f"Collection: {collection_name}")
            collection = self.db[collection_name]
            for document in collection.find():
                print(document)
            print("\n")

    def read(self):

        print(f"Collection: {self.collection.name}")

        for document in self.collection.find():
            print(document)

    # Removes documents from the collection based on a filter
    def delete(self, filter):
        result = self.collection.delete_many(filter)
        print(f"Deleted {result.deleted_count} documents.")

    # remove many entries
    def delete_many(self, query):
        result = self.collection.delete_many(query)
        return result.deleted_count

    # Updates documents in the collection based on a filter and update criteria
    def update(self, filter, update):
        result = self.collection.update_many(filter, update)
        print(f"Updated {result.modified_count} documents.")

    def remove_all(self):
        result = self.collection.delete_many({})
        print(f"Deleted {result.deleted_count} documents.")