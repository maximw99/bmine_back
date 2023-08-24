import xml.dom.minidom
import objects.speech as Speech
import objects.speaker as Speaker
import objects.comment as Comment
import objects.party as Party
import objects.prot as Prot
import objects.daytopics as Daytopics
from mongo import *
import pymongo
from pymongo.collection import Collection
import bson


doc = xml.dom.minidom.parse("Data/19001-data.xml")
speaker_doc = xml.dom.minidom.parse("data/MDB_STAMMDATEN.XML")
prot_array = []


def read_xml(doc: xml.dom.minidom.Document, speaker_doc: xml.dom.minidom.Document):

    # get prot with general info
    prot_list = doc.getElementsByTagName("dbtplenarprotokoll")
    prot_node = prot_list.item(0)
    prot: Prot.Prot = Prot.Prot()
    prot.date = prot_node.getAttribute("sitzung-datum")
    prot.begin = prot_node.getAttribute("sitzung-start-uhrzeit")
    prot.end = prot_node.getAttribute("sitzung-ende-uhrzeit")
    prot.nr = prot_node.getAttribute("sitzung-nr")
    prot.period = prot_node.getAttribute("wahlperiode")

    # get daytopics
    daytopics_array = []
    daytopic_list = doc.getElementsByTagName("tagesordnungspunkt")
    daytopic_counter = 0
    for daytopic_node in daytopic_list:
        daytopic = Daytopics.Daytopic()
        if daytopic_counter > 9:
            dummy_1 = daytopic_node.getAttribute("top-id")[19]
            dummy_2 = daytopic_node.getAttribute("top-id")[20]
            daytopic.nr = dummy_1 + dummy_2
            daytopic_counter += 1
        else:
            daytopic.nr = daytopic_node.getAttribute("top-id")[19]
            daytopic_counter += 1
        
        # get speeches
        speeches_array = []
        speeches_list = daytopic_node.getElementsByTagName("rede")
        for speech_node in speeches_list:
            speech = Speech.Speech()
            speech_id = speech_node.getAttribute("id") # get the speech id
            speech.id = speech_id
            speechescontent_list = speech_node.getElementsByTagName("p") # get all content of a speech
            speech_text = ""
            for speech_content in speechescontent_list:
                if speech_content.getAttribute("klasse") == "J" or speech_content.getAttribute("klasse") == "J_1" or speech_content.getAttribute("klasse") == "O" or speech_content.getAttribute("klasse") == "T":
                    speech_text += speech_content.firstChild.nodeValue
            speech.content = speech_text

            # get comments
            comments = []
            comment_list = speech_node.getElementsByTagName("kommentar") # get all comments of a speech
            for comment_node in comment_list:
                comment = Comment.Comment()
                comment.content = comment_node.firstChild.nodeValue
                comments.append(comment)

            # get speaker
            speaker = Speaker.Speaker()
            speaker_list = speech_node.getElementsByTagName("redner")   
            speaker_node = speaker_list.item(0)
            speaker.id = speaker_node.getAttribute("id") 
            speaker = complete_speaker(speaker_doc, speaker)        

            # fill speech
            speech.comments = comments
            speech.speaker = speaker
            speeches_array.append(speech)

        # fill daytopic
        daytopic.speeches = speeches_array
        daytopics_array.append(daytopic)

    # fill prot
    prot.daytopics = daytopics_array

    # check
    return prot
        
        
def complete_speaker(doc: xml.dom.minidom.Document, speaker: Speaker.Speaker):
    speaker_list = doc.getElementsByTagName("MDB")
    for speaker_node in speaker_list:
        if speaker_node.getElementsByTagName("ID").item(0).firstChild.nodeValue == speaker.id:

            # first name
            speakerfirstname_list = speaker_node.getElementsByTagName("VORNAME")
            speaker_firstname = speakerfirstname_list.item(0).firstChild.nodeValue
            speaker.firstname = speaker_firstname

            # last name
            speakerlastname_list = speaker_node.getElementsByTagName("NACHNAME")
            speaker_lastname = speakerlastname_list.item(0).firstChild.nodeValue
            speaker.lastname = speaker_lastname

            # titel
            speakertitle_list = speaker_node.getElementsByTagName("AKAD_TITEL")
            speaker_title = "keinen Titel"
            if speakertitle_list.item(0).firstChild != None:
                speaker_title = speakertitle_list.item(0).firstChild.nodeValue
            speaker.title = speaker_title

            # bday
            speakerbday_list = speaker_node.getElementsByTagName("GEBURTSDATUM")
            speaker_bday = speakerbday_list.item(0).firstChild.nodeValue
            speaker.bday = speaker_bday

            # religion
            speakerreligion_list = speaker_node.getElementsByTagName("RELIGION")
            speaker_religion = "keine Angabe"
            if speakerreligion_list.item(0).firstChild != None:
                speaker_religion = speakerreligion_list.item(0).firstChild.nodeValue
            speaker.religion = speaker_religion

            # jobs
            speakerjobs_list = speaker_node.getElementsByTagName("BERUF")
            speaker_jobs = "keine Angabe"
            if speakerjobs_list.item(0).firstChild != None:
                speaker_jobs = speakerjobs_list.item(0).firstChild.nodeValue
            speaker.jobs = speaker_jobs

            # party
            speakerparty_list = speaker_node.getElementsByTagName("PARTEI_KURZ")
            speaker_party = speakerparty_list.item(0).firstChild.nodeValue
            party = Party.Party()
            party.name = speaker_party
            speaker.party = party

    return speaker

def insert_prot(prot: Prot.Prot, coll: Collection):
    
    # get prot info
    mongo_prot: {}  = prot.to_document()
    
    # get daytopics
    mongo_daytopiclist = []
    for daytopic in prot.daytopics:
        daytopic: Daytopics.Daytopic = daytopic
        mongo_daytopic = daytopic.to_document()

        # get speeches
        mongo_speecheslist = []
        for speech in daytopic.speeches:
            speech: Speech.Speech = speech
            mongo_speech = speech.to_document()

            # get speaker
            speaker: Speaker.Speaker = speech.speaker
            mongo_speaker = speaker.to_document()

            # get party
            party: Party.Party = speaker.party
            mongo_party = party.to_document()

            # get comments
            mongo_commentlist = []
            for comment in speech.comments:
                comment: Comment.Comment = comment
                mongo_comment = comment.to_document()
                mongo_commentlist.append(mongo_comment)

            # fill speaker
            mongo_speaker["party"] = mongo_party
                
            # fill speech
            mongo_speech["speaker"] = mongo_speaker
            mongo_speech["comments"] = mongo_commentlist
            mongo_speecheslist.append(mongo_speech)

        # fill daytopic
        mongo_daytopic["speeches"] = mongo_speecheslist
        mongo_daytopiclist.append(mongo_daytopic)

    # fill prot
    mongo_prot["daytopics"] = mongo_daytopiclist
    
    print("inserting...")
    coll.insert_one(mongo_prot)




# Mongo connec
client = get_mongoconnec()
db = get_mongodb(client)
coll = get_mongocoll(db)



test_prot = read_xml(doc, speaker_doc)
#complete_speaker(speaker_doc)
insert_prot(test_prot, coll)




