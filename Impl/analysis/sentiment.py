import sys
sys.path.append("impl")
from databank import mongoconnec
from objects import *
import spacy
from spacy_sentiws import spaCySentiWS
from googletrans import Translator

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


def vibe_analysis(content: str):
    translator = Translator()
    nlp = spacy.load("de_core_news_sm")
    nlp.add_pipe("sentiws", config={'sentiws_path': 'data/SentiWS_v2.0'})
    text = translator.translate(content, dest="en")
    print(text)

    # start analysis
    doc = nlp(content)

    # pos
    #print([(w.text, w.pos_, w.dep_) for w in doc])

    # sentiment
    vibe = 0
    """ biggest_plus = 0
    plus = ""
    biggest_minus = 0
    minus = "" """
    correct_checked = 0
    total_checked = 0
    for token in doc:
        #print('{}, {}'.format(token.text.replace(",", ""), token._.sentiws))
        total_checked += 1
        if token._.sentiws != None:
            correct_checked += 1
            vibe += token._.sentiws
            """ if token._.sentiws > biggest_plus:
                plus = token.text.replace(",", "")
                biggest_plus = token._.sentiws
            if token._.sentiws < biggest_minus:
                minus = token.text.replace(",", "")
                biggest_minus = token._.sentiws
    print("")
    print("vibe is: ", vibe)
    print("total checked: ", total_checked, " correct checked: ", correct_checked, " missed checked", total_checked - correct_checked)
    print("biggest + : ", plus, " with:", biggest_plus)
    print("biggest - : ", minus, " with:", biggest_minus)
    print("") """
    return vibe
    