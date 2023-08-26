import sys
sys.path.append("impl")
from databank import mongoconnec
from objects import *
import spacy
from spacy_sentiws import spaCySentiWS

def test():
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


def test_analysis(speech: speech.Speech):

    # start analysis

    nlp = spacy.load("de_core_news_sm")
    nlp.add_pipe("sentiws", config={'sentiws_path': 'data/SentiWS_v2.0'})
    text = "Hello you little pig"
    doc = nlp(speech.content)


    # pos
    #print([(w.text, w.pos_) for w in doc])


    #print(speech.content)

    # sentiment
    vibe = 0
    for token in doc:
        #print(token.text.replace(",", ""))
        #print('{}, {}'.format(token.text.replace(",", ""), token._.sentiws))
        if token._.sentiws != None:
            vibe += token._.sentiws
    
    print("")
    print("vibe is: ", vibe)