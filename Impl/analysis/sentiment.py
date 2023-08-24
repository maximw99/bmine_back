import sys
sys.path.append("impl")
from databank import mongoconnec
from objects import *
import spacy

client = mongoconnec.get_mongoconnec()
db = mongoconnec.get_mongodb(client)
coll = mongoconnec.get_mongocoll(db)

prot = coll.find_one()
daytopics = prot["daytopics"]
daytopic = daytopics[0]
speeches = daytopic["speeches"]
speech = speeches[0]["content"]

nlp = spacy.load("de_core_news_sm")
doc = nlp(speech)

print([(w.text, w.pos_) for w in doc])