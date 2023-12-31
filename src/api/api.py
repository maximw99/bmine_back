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
    coll = mongoconnec.get_mongocollprots(db)
    curr =  coll.find({"_id" : prot_id})
    response = curr[0]
    client.close()

    return jsonify(response)


@app.route("/get-allprot", methods=["Get"])
def all_prot():
    client = mongoconnec.get_mongoconnec()
    db = mongoconnec.get_mongodb(client)
    coll = mongoconnec.get_mongocollprots(db)

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
    coll = mongoconnec.get_mongocollprots(db)


    speeches = []
    curr =  coll.find({}).allow_disk_use(True)

    for doc in curr:
        for daytopic in doc["daytopics"]:
            for speech in daytopic["speeches"]:
                speeches.append(speech)

    speeches_json = {"speeches" : speeches}
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

    speakers = []

    for speaker in coll_speakers.find({}).allow_disk_use(True): 
        speakers.append(speaker)

    speakers_json = {"speakers" : speakers}
    client.close()

    return(jsonify(speakers_json))


def start_api():
    app.run(debug=True)
