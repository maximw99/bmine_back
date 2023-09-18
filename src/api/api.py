import sys
sys.path.append("src")
from databank import mongoconnec
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from objects import *
app = Flask(__name__)
CORS(app)

@app.route("/get-oneprot/<prot_id>", methods=["Get"])
def one_prot(prot_id):
    client = mongoconnec.get_mongoconnec()
    db = mongoconnec.get_mongodb(client)
    coll = mongoconnec.get_mongocoll(db)
    curr =  coll.find({"_id" : prot_id})
    response = curr[0]
    client.close()

    return jsonify(response)


@app.route("/get-allprot", methods=["Get"])
def all_prot():
    client = mongoconnec.get_mongoconnec()
    db = mongoconnec.get_mongodb(client)
    coll = mongoconnec.get_mongocoll(db)

    counter = 0
    prots = []
    curr =  coll.find({}).allow_disk_use(True)
    for doc in curr:
        print(curr)
        print(counter)
        counter += 1
        prots.append(doc)
    client.close()
    prots_json = {"prots" : prots}

    return jsonify(prots_json)


@app.route("/get-speechesov", methods=["Get"])
def speeches_ov():
    client = mongoconnec.get_mongoconnec()
    db = mongoconnec.get_mongodb(client)
    coll = mongoconnec.get_mongocoll(db)

    speeches = []
    curr =  coll.find({}).allow_disk_use(True)

    for doc in curr:
        for daytopic in doc["daytopics"]:
            for speech in daytopic["speeches"]:
                speeches.append(speech)

    speeches_json = {"speeches" : speeches}
    client.close()

    return(jsonify(speeches_json))


@app.route("/get-test", methods=["Get"])
def test():
    client = mongoconnec.get_mongoconnec()
    db = mongoconnec.get_mongodb(client)
    coll = mongoconnec.get_mongocoll(db)

    speakers = []
    curr =  coll.find({}).allow_disk_use(True)

    for doc in curr:
        for daytopic in doc["daytopics"]:
            for speech in daytopic["speeches"]:

                #get vibe
                positive = 0
                negative = 0
                neutral = 0
                try:
                    if speech["vibe"] > 0.5:
                        positiv += 1
                    elif speech["vibe"] < -0.5:
                        negativ += 1
                    else:
                        neutral += 1
                except:
                    pass

                # get speaker
                try:
                    speaker = speech["speaker"]
                    speaker["sui"] = "suiiii"
                    speaker["positive"] = positive
                    speaker["negative"] = negative
                    speaker["neutral"] = neutral
                    speakers.append(speaker)
                except:
                    pass

    speeches_json = {"speakers" : speakers}
    client.close()

    return(jsonify(speeches_json))


@app.route("/get-speakersovtest", methods=["Get"])
def speakers_ovtest():
    client = mongoconnec.get_mongoconnec()
    db = mongoconnec.get_mongodb(client)
    coll = mongoconnec.get_mongocoll(db)

    speakers = []
    curr =  coll.find({}).allow_disk_use(True)

    for doc in curr:
        for daytopic in doc["daytopics"]:
            for speech in daytopic["speeches"]:
                try:
                    speaker = speech["speaker"]
                    speakers.append(speaker)
                except:
                    pass

    speakers_solo = [i for n, i in enumerate(speakers)
                    if i not in speakers[:n]]
    speakers_json = {"speakers" : speakers_solo}
    print("before: " + str(len(speakers)) + " after: " + str(len(speakers_solo)))
    client.close()

    return(jsonify(speakers_json))


@app.route("/get-speakersov", methods=["Get"])
def speakers_ov():
    client = mongoconnec.get_mongoconnec()
    db = mongoconnec.get_mongodb(client)
    coll_speakers = mongoconnec.get_mongocollspeakers(db)
    coll_prots = mongoconnec.get_mongocoll(db)

    speakers = []
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
                                if speech["vibe"] < -0.5:
                                    negative += 1
                                elif speech["vibe"] > 0.5:
                                    positive += 1
                                else:
                                    neutral += 1
                            except:
                                pass
                    except:
                        pass
                    
        print("speaker done")
        speaker["speeches"] = speech_count
        speaker["positive"] = positive
        speaker["negative"] = negative
        speaker["neutral"] = neutral
        speakers.append(speaker)





    speakers_json = {"speakers" : speakers}
    client.close()

    return(jsonify(speakers_json))

def start_api():
    app.run(debug=True)
