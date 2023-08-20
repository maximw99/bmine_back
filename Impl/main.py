import xml.dom.minidom

doc = xml.dom.minidom.parse("Data/19001-data.xml")


def get_allspeaker(doc):
    speaker_list = doc.getElementsByTagName("rednerliste")
    speaker_node = speaker_list.item(0)
    speakers = speaker_node.getElementsByTagName("vorname")
    for speaker in speakers:
        print("vorname: ", speaker.firstChild.nodeValue)

def get_speeches(doc):
    daytopic_list = doc.getElementsByTagName("tagesordnungspunkt")
    daytopic = daytopic_list.item(0)
    speeches_list = daytopic.getElementsByTagName("rede")
    speech_node = speeches_list.item(0)
    speech_id = speech_node.getAttribute("id")
    speechescontent_list = speech_node.getElementsByTagName("p")
    for speech_content in speechescontent_list:
        print(speech_content.firstChild.nodeValue)
    print(speechescontent_list.length)




get_speeches(doc)





