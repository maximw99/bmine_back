#general imports
import sys
import os
sys.path.append("src")

#import dom parser
import xml.dom.minidom

#import class objects
from objects import speech as Speech
from objects import speaker as Speaker
from objects import comment as Comment
from objects import party as Party
from objects import prot as Prot
from objects import daytopics as Daytopics
from databank import mongoconnec

#import core modules
from core import get_allspeakers
from core import read_xml


def debug_singleprot():
    '''Debugs a single prot
        Returns a dict
    '''

    print("starting")
    client = mongoconnec.get_mongoconnec()
    db = mongoconnec.get_mongodb(client)
    coll = mongoconnec.get_mongocoll(db)
    speaker_doc = xml.dom.minidom.parse("data/MDB_STAMMDATEN.XML")
    all_speaker = get_allspeakers(speaker_doc)
    path = "data"
    i = 1
    while i < 2:
        doc = xml.dom.minidom.parse("data/1900" + str(i) + "-data.xml")
        #test_prot = read_xml(doc, all_speaker)
        test = {"name": "test1"}
        coll.insert_one(test)
        print("success")
        i += 1


def get_speechesamount():
    '''Gets amount of speeches
        Returns int
    '''

    speeches_list = []

    # get prot
    print("starting")
    speaker_doc = xml.dom.minidom.parse("data/MDB_STAMMDATEN.XML")
    all_speaker = get_allspeakers(speaker_doc)
    i = 1


    path = "data"
    counter = 1
    for file in os.listdir(path):
        print("now reading prot: ", counter)
        if not file.endswith("data.xml"): continue
        root = os.path.join(path, file)
        doc = xml.dom.minidom.parse(root)
        counter += 1
        prot = read_xml(doc, all_speaker)
        # get daytopic
        daytopics = prot.daytopics
        for daytopic in daytopics:
            print("read daytopic: ", daytopic.nr)

        #get speech
            speeches = daytopic.speeches
            for speech in speeches:
                print("reading: ", speech.id)
                speeches_list.append(speech) 
    print("all prots assembeld")
    print(len(speeches_list))


def get_testspeech():
    '''Gets test speeches out of one prot
        Returns list
    '''

    speeches_list = []

    # get prot
    print("starting")
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
        # get daytopic
        daytopics = prot.daytopics
        for daytopic in daytopics:
            print("read daytopic: ", daytopic.nr)

        #get speech
            speeches = daytopic.speeches
            for speech in speeches:
                print("reading: ", speech.id)
                speeches_list.append(speech) 
    print("all prots assembeld")
    print(len(speeches_list))

    