#general imports
import sys
import os
sys.path.append("src")

#import dom parser
import xml.dom.minidom

#class objects import
from objects import speech as Speech
from objects import speaker as Speaker
from objects import comment as Comment
from objects import party as Party
from objects import prot as Prot
from objects import daytopics as Daytopics



def get_prots():
    '''Gets all prots als dicts
        Returns List
    '''

    prots = []
    speaker_doc = xml.dom.minidom.parse("data/MDB_STAMMDATEN.XML")
    all_speaker = get_allspeakers(speaker_doc)
    path = "data"
    counter = 1
    for file in os.listdir(path):
        print("now reading prot: ", counter)
        if not file.endswith("data.xml"): continue
        root = os.path.join(path, file)
        doc = xml.dom.minidom.parse(root)
        counter += 1
        prot = read_xml(doc, all_speaker)
        prots.append(prot)
    print("all prots assembeld")
    return prots


def read_xml(doc: xml.dom.minidom.Document, all_speaker):
    '''Reads xml file and fills class objects
        Returns dict
    '''

    # get prot with general info
    prot_list = doc.getElementsByTagName("dbtplenarprotokoll")
    prot_node = prot_list.item(0)
    prot: Prot.Prot = Prot.Prot()
    prot.date = prot_node.getAttribute("sitzung-datum")
    prot.begin = prot_node.getAttribute("sitzung-start-uhrzeit")
    prot.end = prot_node.getAttribute("sitzung-ende-uhrzeit")
    prot.nr = prot_node.getAttribute("sitzung-nr")
    prot.period = prot_node.getAttribute("wahlperiode")
    ivzblock_list = doc.getElementsByTagName("ivz-block")

    # get daytopics
    daytopics_array = []
    daytopic_list = doc.getElementsByTagName("tagesordnungspunkt")
    daytopic_counter = 1

    for daytopic_node in daytopic_list:
        ivz_block = ivzblock_list.item(daytopic_counter - 1)
        if ivz_block != None:
            topic_list = ivz_block.getElementsByTagName("ivz-eintrag-inhalt")
            top = ""
            for topic in topic_list:
                if topic.firstChild.nodeValue != None:
                    top += topic.firstChild.nodeValue
        else:
            top = "no title"
        daytopic = Daytopics.Daytopic()
        daytopic.nr = daytopic_counter
        daytopic.topic = top
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
                    if speech_content.firstChild != None:
                        speech_text += speech_content.firstChild.nodeValue
            speech.content = speech_text
            speech.vibe = 0

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
            speaker._firstname = "error"  
            speaker.lastname = "error"
            speaker.title = "error"
            speaker.bday = "error"
            speaker.religion = "error"
            speaker.jobs = "error"
            speaker.party = "error"
            
            for speaker_item in all_speaker:
                if speaker.id == speaker_item.id: 
                    speaker = speaker_item

            # fill speech
            speech.comments = comments
            speech.speaker = speaker
            speeches_array.append(speech)
            print("speech checked")

        # fill daytopic
        daytopic.speeches = speeches_array
        daytopics_array.append(daytopic)
        print("daytopic checked")

    # fill prot
    prot.daytopics = daytopics_array

    # check
    return prot
        
        
def get_allspeakers(doc: xml.dom.minidom.Document):
    '''Gets infos about all speakers from xml
        Returns list of objects
    '''

    speaker_list = doc.getElementsByTagName("MDB")
    all_speaker = []
    for speaker_node in speaker_list:
        speaker = Speaker.Speaker()

        #id
        speakerid_list = speaker_node.getElementsByTagName("ID")
        speaker_id = speakerid_list.item(0).firstChild.nodeValue
        speaker.id = speaker_id

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
        if speakerparty_list.item(0).firstChild != None:
            speaker.party = speakerparty_list.item(0).firstChild.nodeValue

        all_speaker.append(speaker)

    return all_speaker


def create_mongoprots(prots: []):
    '''Takes a prot and turns it into a dict for mongo
        Returns a dict
    '''

    mongo_prots = []
    for prot in prots:
    
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
                party = speaker.party

                # get comments
                mongo_commentlist = []
                for comment in speech.comments:
                    comment: Comment.Comment = comment
                    mongo_comment = comment.to_document()
                    mongo_commentlist.append(mongo_comment)

                # fill speaker
                mongo_speaker["party"] = party
                    
                # fill speech
                mongo_speech["speaker"] = mongo_speaker
                mongo_speech["comments"] = mongo_commentlist
                mongo_speecheslist.append(mongo_speech)

            # fill daytopic
            mongo_daytopic["speeches"] = mongo_speecheslist
            mongo_daytopiclist.append(mongo_daytopic)

        # fill prot
        mongo_prot["daytopics"] = mongo_daytopiclist
        mongo_prots.append(mongo_prot)
    
    print("mongoprots complete")
    return(mongo_prots)