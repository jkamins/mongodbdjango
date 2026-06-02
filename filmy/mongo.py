from pymongo import MongoClient

_client = None

def get_db():
    global _client
    if _client is None:
        _client = MongoClient('localhost', 27017)
    return _client['biblioteka_projekt']