import bs4
import urllib.request
from urllib.request import urlopen
from bs4 import BeautifulSoup

def get_imageurl(speakers):

    pairs = []
    image = "no found"
    search_counter = 0

    for i in range(0, 750, 12):
        print("connecting with: ", i)

        try:
            url = "https://www.bundestag.de/ajax/filterlist/de/abgeordnete/862712-862712?limit=20&noFilterSet=true&offset=" + str(i)
            page = urlopen(url)
            page_soup = BeautifulSoup(page, "html.parser")
            img_items = page_soup.findAll("div",{"class" : "bt-bild-standard"})
            counter_divblocks = 0

            for div_obj in img_items:
                pair = ()
                image_url = str(div_obj.find("img")["data-img-md-normal"])
                scraper_name = div_obj.find("img")["title"]

                counter_speaker = 0
                for speaker in speakers:
                    if speaker[0] == scraper_name:
                        pair = (speaker[0], speaker[1], speaker[2], speaker[3], image_url)
                        pairs.append(pair)
                    print("speaker: " + str(counter_speaker) + " in: " + str(counter_divblocks) + " of: " + "12 div blocks with: " + str(search_counter) + " of 62 done")
                    counter_speaker += 1
                counter_divblocks += 1

        except:
            print("Error")

        search_counter += 1

    return pairs

def get_imageurlsecond(speakers):

    pairs = []
    image = "no found"
    search_counter = 0

    for i in range(0, 750, 12):
        print("connecting with: ", i)

        try:
            url = "https://www.bundestag.de/ajax/filterlist/de/abgeordnete/862712-862712?limit=20&noFilterSet=true&offset=" + str(i)
            page = urlopen(url)
            page_soup = BeautifulSoup(page, "html.parser")
            img_items = page_soup.findAll("div",{"class" : "bt-bild-standard"})
            counter_divblocks = 0

            for div_obj in img_items:
                pair = ()
                image_url = str(div_obj.find("img")["data-img-md-normal"])
                scraper_name = div_obj.find("img")["title"]

                counter_speaker = 0
                for speaker in speakers:
                    if speaker[1] == scraper_name:
                        pair = (speaker[0], image_url)
                        pairs.append(pair)
                    print("speaker: " + str(counter_speaker) + " in: " + str(counter_divblocks) + " of: " + "12 div blocks with: " + str(search_counter) + " of 62 done")
                    counter_speaker += 1
                counter_divblocks += 1

        except:
            print("Error")

        search_counter += 1

    return pairs
