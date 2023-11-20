import sys
sys.path.append("src")
from databank import mongoconnec
from databank import core
import xml.dom.minidom
from objects import party as Party




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

    pairs = get_imageurl(speakers)
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
    speakers = core.get_allspeakers(speaker_doc)
    mongo_speakers = []
    i = 0
    for speaker in speakers:
        try:
            mongo_speaker = speaker.to_document()
            mongo_speakers.append(mongo_speaker)
        except:
            pass
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


def mongoadd_partys():
    client = mongoconnec.get_mongoconnec()
    db = mongoconnec.get_mongodb(client)
    coll_prots = mongoconnec.get_mongocollprots(db)
    coll_speakers = mongoconnec.get_mongocollspeakers(db)
    coll_partys = mongoconnec.get_mongocollpartys(db)
    partys = []
    
    curr = coll_prots.find({}).allow_disk_use(True)
    for prot in curr:
        for daytopic in prot["daytopics"]:
            for speech in daytopic["speeches"]:
                try:
                    party = speech["speaker"]["party"]
                    partys.append(party)
                except:
                    pass

    #print(list(dict.fromkeys(partys)))
    partys_solo = list(dict.fromkeys(partys))
    partys_fixed = []
    mongo_partys = []
    
    for party in partys_solo:
        counter = 0
        vibe = 0
        vibe_counter = 0
        curr_2 = coll_prots.find({}).allow_disk_use(True)
        for prot in curr_2:
            for daytopic in prot["daytopics"]:
                for speech in daytopic["speeches"]:
                    try:
                        if party == speech["speaker"]["party"]:
                            print("hit!")
                            counter += 1
                            vibe += speech["vibe"]
                            vibe_counter += 1
                    except:
                        print("error")
        mongo_party = Party.Party(party, round(vibe/vibe_counter,4), counter)
        partys_fixed.append(mongo_party)

    for party in partys_fixed:
        mongo_partys.append(party.to_document())
    
    coll_partys.insert_many(mongo_partys)
        


    #coll.insert_many(mongo_speakers)


def mongoadd_prots():
    prots = core.get_prots()
    mongo_prots = core.create_mongoprots(prots)
    client = mongoconnec.get_mongoconnec()
    db = mongoconnec.get_mongodb(client)
    coll = mongoconnec.get_mongocollprots(db)
    coll.insert_many(mongo_prots)


def get_imageurl(speakers):

    pairs = []
    image = "no found"
    search_counter = 0

    for i in range(0, 750, 12):
        print("connecting with: ", i)

        try:
            url = "https://www.bundestag.de/ajax/filterlist/de/abgeordnete/862712-862712?limit=20&noFilterSet=true&offset=" + str(i)
            page = urlopen(url)
            page_soup = BeautifulSoup(page, "html.parser")
            img_items = page_soup.findAll("div",{"class" : "bt-bild-standard"})
            counter_divblocks = 0

            for div_obj in img_items:
                pair = ()
                image_url = str(div_obj.find("img")["data-img-md-normal"])
                scraper_name = div_obj.find("img")["title"]

                counter_speaker = 0
                for speaker in speakers:
                    if speaker[0] == scraper_name:
                        pair = (speaker[0], speaker[1], speaker[2], speaker[3], image_url)
                        pairs.append(pair)
                    print("speaker: " + str(counter_speaker) + " in: " + str(counter_divblocks) + " of: " + "12 div blocks with: " + str(search_counter) + " of 62 done")
                    counter_speaker += 1
                counter_divblocks += 1

        except:
            print("Error")

        search_counter += 1

    return pairs

