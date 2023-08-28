from pymongo import MongoClient
import urllib.parse

def get_mongoconnec():
    
    file = open("data/pw.txt")
    content = file.readlines()
    name: str = content[0]
    code: str = content[1]
    file.close()
    user = urllib.parse.quote("Maxim")
    pw = urllib.parse.quote("Mongoserver1")
    client = MongoClient('mongodb://%s:%s@10.77.77.46' % (user, pw), 27017)
    print("connected")
    return client

def get_mongodb(client):
    db = client.bundestag
    return db

def get_mongocoll(db):
    coll = db.prots
    return coll

