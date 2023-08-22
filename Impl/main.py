import xml.dom.minidom
import objects.speech as Speech
import objects.speaker as Speaker
import objects.comment as Comment
import objects.party as Party
import objects.prot as Prot
import objects.daytopics as Daytopics

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
    for daytopic in prot.daytopics: 
        for speech in daytopic.speeches:
            """ print("speech: " + speech.id + " from: " + speech.speaker.id + " " + speech.speaker.firstname + " " + speech.speaker.lastname + " von der: " + speech.speaker.party)
            for comment in speech.comments:
                print(comment.content) """
            
    print("daytopics amount: ", prot.daytopics[1].speeches[0].content)
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
            speaker.party = speaker_party

    return speaker














        
        
        




read_xml(doc, speaker_doc)
#complete_speaker(speaker_doc)




