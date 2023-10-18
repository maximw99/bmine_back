from pymongo import MongoClient



def get_mongoconnec():
    '''Gets the connection to db
        Returns client
    '''

    client = MongoClient('mongodb://10.77.77.46:27000/')
    print("connected")
    return client

def get_mongodb(client):
    '''Takes client and gets db
        Returns db
    '''

    db = client.bundestag
    return db

def get_mongocollprots(db):
    '''Takes a db and gets a collection 
        Returns coll:prots
    '''
    coll = db.prots
    return coll

def get_mongocollspeakers(db):
    '''Takes a db and gets a collection
        Returns coll:speakers
    '''

    coll = db.speakers
    return coll

def get_mongocollpartys(db):
    '''Takes a db and gets a collection
        Returns coll:partys
    '''
    
    coll = db.partys
    return coll

