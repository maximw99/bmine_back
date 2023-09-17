import sys
sys.path.append("src")
from databank import mongoconnec
from website import scraper


def mongo_add():

    print("connecting...")
    client = mongoconnec.get_mongoconnec()
    db = mongoconnec.get_mongodb(client)
    coll = mongoconnec.get_mongocoll(db)

    curr =  coll.find({}).allow_disk_use(True)
    print("connected")

    """ for doc in curr:
        doc_id = doc["_id"]
        daytopic_inc = 0
        speeches_inc = 0
        for daytopic in doc["daytopics"]:
            for speech in daytopic["speeches"]:
                speaker_obj = speech["speaker"]
                speaker_name = speaker_obj["firstname"] + " " + speaker_obj["lastname"]
                print(speaker_name)
                url = scraper.get_imageurl(speaker_name)
                print(url)
                print("next")

                speeches_inc =+ 1 """

    doc = curr[0]
    doc_id = doc["_id"]
    daytopic_inc = 0
    speeches_inc = 0
    for daytopic in doc["daytopics"]:
        for speech in daytopic["speeches"]:
            speaker_obj = speech["speaker"]
            speaker_name = speaker_obj["firstname"] + " " + speaker_obj["lastname"]
            print(speaker_name)
            url = scraper.get_imageurl(speaker_name)
            print(url)
            coll.update_one({"_id" : doc_id}, {"$set": {"daytopics." + str(daytopic_inc) + ".speeches." + str(speeches_inc) + ".speaker.url":url}})
            print("next")

            speeches_inc =+ 1
        daytopic_inc =+ 1
            






    #test = coll.find_one({"_id" : "19-1"})

    #coll.update_one({"_id" : "19-1"}, {"$set": {"daytopics.0.speeches.0.speaker.test":1}})

    #coll.update_one({"_id" : "19-1"}, {"$unset": {"test":1}})

    client.close()
    print("done")


def add_url():
    print("connecting...")
    client = mongoconnec.get_mongoconnec()
    db = mongoconnec.get_mongodb(client)
    coll = mongoconnec.get_mongocoll(db)

    curr =  coll.find({}).allow_disk_use(True)
    print("connected")
    speakers = []

    for doc in curr:
        doc_id = doc["_id"]
        daytopic_inc = 0
        for daytopic in doc["daytopics"]:
            speeches_inc = 0
            for speech in daytopic["speeches"]:
                try:
                    speaker_obj = speech["speaker"]
                    speaker_name = speaker_obj["firstname"] + " " + speaker_obj["lastname"]
                except:
                    speaker_name = "no speaker"
                speakers.append((speaker_name, doc_id, daytopic_inc, speeches_inc))
                speeches_inc += 1
            daytopic_inc += 1
        print("doc done")
    print(len(speakers))

    pairs = scraper.get_imageurl(speakers)
    #f = open("test.txt", "a")
    update_counter = 0
    for pair in  pairs:
        print("update: " + str(update_counter) + " of: " + str(len(pairs)))
        #f.write(str(pair[0]) + " " + str(pair[1]) + " " + str(pair[2]) + " " + str(pair[3]) + " " + pair[4] + "\n")
        coll.update_one({"_id" : str(pair[1])}, {"$set": {"daytopics." + str(pair[2]) + ".speeches." + str(pair[3]) + ".speaker.url" : pair[4]}})
        update_counter += 1
    #f.close()


def add_urldummy():

    print("connecting...")
    client = mongoconnec.get_mongoconnec()
    db = mongoconnec.get_mongodb(client)
    coll = mongoconnec.get_mongocoll(db)

    curr =  coll.find({}).allow_disk_use(True)
    print("connected")
    z = 0

    for doc in curr:
        doc_id = doc["_id"]
        daytopic_inc = 0
        for daytopic in doc["daytopics"]:
            speeches_inc = 0
            for speech in daytopic["speeches"]:
                if daytopic_inc == 2:
                    print("holla")
                try:
                    coll.update_one({"_id" : doc_id}, {"$set": {"daytopics." + str(daytopic_inc) + ".speeches." + str(speeches_inc) + ".speaker.url":"no found"}})
                except:
                    print("error")
                print("next")
                speeches_inc += 1
            daytopic_inc += 1
        print("doc: " + str(z) + " " + "done")
        z += 1
            
#add_urldummy()
add_url()


