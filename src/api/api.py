import sys
sys.path.append("src")
from databank import mongoconnec
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
client = mongoconnec.get_mongoconnec()
db = mongoconnec.get_mongodb(client)
coll = mongoconnec.get_mongocoll(db)

@app.route("/get-speaker", methods=["Get"])
def home():
    curr =  coll.find({"_id" : "19-3"})
    response = curr[0]["daytopics"][0]["speeches"][0]["speaker"]
    

    return response


def start_api():
    app.run(debug=True)

print(type(coll.find_one()))

print(type(coll.find({})))