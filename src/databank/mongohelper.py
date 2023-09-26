import sys
sys.path.append("src")
from databank import mongoconnec
from website import scraper
from main import get_allspeakers
import xml.dom.minidom




def mongoadd_url():
    print("connecting...")
    client = mongoconnec.get_mongoconnec()
    db = mongoconnec.get_mongodb(client)
    coll = mongoconnec.get_mongocollprots(db)

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


def mongoadd_urldummy():
    print("connecting...")
    client = mongoconnec.get_mongoconnec()
    db = mongoconnec.get_mongodb(client)
    coll = mongoconnec.get_mongocollspeakers(db)

    curr =  coll.find({}).allow_disk_use(True)
    print("connected")
    speakers = []

    for speaker in curr:

        #add dummy url
        coll.update_one({"_id" : str(speaker["_id"])}, {"$set": {"url" : "no"}})


def mongoadd_speakers():
    speaker_doc = xml.dom.minidom.parse("data/MDB_STAMMDATEN.XML")
    speakers = get_allspeakers(speaker_doc)
    mongo_speakers = []
    i = 0
    for speaker in speakers:
        mongo_speaker = speaker.to_document()
        mongo_speakers.append(mongo_speaker)
        print(i)
        i += 1


    client = mongoconnec.get_mongoconnec()
    db = mongoconnec.get_mongodb(client)
    coll = mongoconnec.get_mongocollspeakers(db)
    coll.insert_many(mongo_speakers)


def mongoadd_speakersentiment():
    client = mongoconnec.get_mongoconnec()
    db = mongoconnec.get_mongodb(client)
    coll_speakers = mongoconnec.get_mongocollspeakers(db)
    coll_prots = mongoconnec.get_mongocoll(db)

    prots = []

    for doc in coll_prots.find({}).allow_disk_use(True): 
        prots.append(doc)

    for speaker in coll_speakers.find({}).allow_disk_use(True):
        positive = 0
        negative = 0
        neutral = 0
        speech_count = 0
        for prot in prots:
            for daytopic in prot["daytopics"]:
                for speech in daytopic["speeches"]:
                    try:
                        if speaker["_id"] == speech["speaker"]["_id"]:
                            speech_count += 1
                            try:
                                if speech["vibe"] < -0.1:
                                    negative += 1
                                elif speech["vibe"] > 0.1:
                                    positive += 1
                                else:
                                    neutral += 1
                            except:
                                pass
                    except:
                        pass
                        
        coll_speakers.update_one({"_id" : str(speaker["_id"])}, {"$set": {"speeches" : speech_count}})
        coll_speakers.update_one({"_id" : str(speaker["_id"])}, {"$set": {"positive" : positive}})
        coll_speakers.update_one({"_id" : str(speaker["_id"])}, {"$set": {"negative" : negative}})
        coll_speakers.update_one({"_id" : str(speaker["_id"])}, {"$set": {"neutral" : neutral}})


def mongoadd_speakersurl():
    client = mongoconnec.get_mongoconnec()
    db = mongoconnec.get_mongodb(client)
    coll_speakers = mongoconnec.get_mongocollspeakers(db)
    coll_prots = mongoconnec.get_mongocoll(db)

    prots = []

    for doc in coll_prots.find({}).allow_disk_use(True): 
        prots.append(doc)

    for speaker in coll_speakers.find({}).allow_disk_use(True):
        positive = 0
        negative = 0
        neutral = 0
        speech_count = 0
        for prot in prots:
            for daytopic in prot["daytopics"]:
                for speech in daytopic["speeches"]:
                    try:
                        if speaker["_id"] == speech["speaker"]["_id"]:
                            url = speech["speaker"]["url"]
                            coll_speakers.update_one({"_id" : str(speaker["_id"])}, {"$set": {"url" : url}})
                            continue
                    except:
                        pass
                