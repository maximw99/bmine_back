from pymongo import MongoClient
import urllib.parse

def get_mongoconnec():
    user = urllib.parse.quote_plus("Maxim")
    pw = urllib.parse.quote_plus("Mongoserver1")
    client = MongoClient('mongodb://%s:%s@10.77.77.46' % (user, pw), 27017)
    print("connected")
    return client

def get_mongodb(client):
    db = client.bundestag
    return db

def get_mongocoll(db):
    coll = db.prots
    return coll

