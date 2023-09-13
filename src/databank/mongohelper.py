import mongoconnec


client = mongoconnec.get_mongoconnec()
db = mongoconnec.get_mongodb(client)
coll = mongoconnec.get_mongocoll(db)

speeches = []
curr =  coll.find({}).allow_disk_use(True)

test = coll.find_one({"_id" : "19-1"})

coll.update_one({"_id" : "19-1"}, {"$set": {"daytopics.0.speeches.0.speaker.test":1}})

#coll.update_one({"_id" : "19-1"}, {"$unset": {"test":1}})

print("done")





""" for doc in curr:
    for daytopic in doc["daytopics"]:
        for speech in daytopic["speeches"]:
            speaker = speech["speaker"]
            print(speaker["firstname"]) """