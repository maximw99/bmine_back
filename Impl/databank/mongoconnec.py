from pymongo import MongoClient
import urllib.parse
from itertools import islice


file = open("data/pw.txt")
content = file.readlines()
user = content[0]
pw = content[1]


def get_mongoconnec():
    
    file = open("data/pw.txt")
    content = file.readlines()
    name = content[0]
    code = content[1]
    file.close()
    user = urllib.parse.quote_plus(name)
    pw = urllib.parse.quote_plus(code)
    client = MongoClient('mongodb://%s:%s@10.77.77.46' % (user, pw), 27017)
    print("connected")
    return client

def get_mongodb(client):
    db = client.bundestag
    return db

def get_mongocoll(db):
    coll = db.prots
    return coll

