import pymongo

def generate_mongodb_connection():
    return pymongo.MongoClient("localhost", 27017)


class MongoDBConnection:
    def __init__(self):
        pass

    def __enter__(self):
        self.conn = generate_mongodb_connection()
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()


class MongoDBDatabase:
    def __init__(self, dbname):
        assert dbname is not None
        self.dbname = dbname

    def __enter__(self):
        self.conn = generate_mongodb_connection()
        self.dbobj = self.conn.get_database(self.dbname)
        return self.dbobj

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()