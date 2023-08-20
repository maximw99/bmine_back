import xml.dom.minidom

doc = xml.dom.minidom.parse("Data/19001-data.xml")
speaker_list = doc.getElementsByTagName("rednerliste")
speakerlist_node = speaker_list.item(0)
speakers = speakerlist_node.getElementsByTagName("vorname")
print("speakerlist: ", speakers.length, " type of: ", type(speakers))



for speaker in speakers:
    print("vorname: ", speaker.firstChild.nodeValue)


#print(speaker_group.getElementsByTagName("vorname")[1].firstChild.nodeValue)


""" for speaker in speaker_group:
    speaker_id = speaker.getAttribute("id")
    speaker_name = speaker.getElementsByTagName("vorname")[0].childNodes[0].nodeValue
    print(speaker_group) """