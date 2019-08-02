from pymongo import MongoClient

class MongoClientFactory:

    @staticmethod
    def build(username, password, dbHost) -> MongoClient:
        connection = f"mongodb+srv://{username}:{password}@{dbHost}.mongodb.net/test?retryWrites=true&w=majority"
        return MongoClient(connection)
