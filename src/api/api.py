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



def test():
    client = mongoconnec.get_mongoconnec()
    db = mongoconnec.get_mongodb(client)
    coll = mongoconnec.get_mongocoll(db)

    curr =  coll.find({}).allow_disk_use(True)
    for doc in curr:
        prot_obj: prot.Prot = doc
        print(prot_obj["_id"])
    client.close()


def start_api():
    app.run(debug=True)
