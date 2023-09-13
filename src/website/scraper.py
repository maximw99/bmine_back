import bs4
import urllib.request
from urllib.request import urlopen
from bs4 import BeautifulSoup

def get_imageurl(speaker_name):

    items = 0
    image = "no found"

    for i in range(0, 750, 10):
        url = "https://www.bundestag.de/ajax/filterlist/de/abgeordnete/862712-862712?limit=20&noFilterSet=true&offset=" + str(i)
        page = urlopen(url)
        page_soup = BeautifulSoup(page, "html.parser")
        img_items = page_soup.findAll("div",{"class" : "bt-bild-standard"})

        for div_obj in img_items:
            image_url = "bundestag.de" + str(div_obj.find("img")["data-img-md-normal"])
            scraper_name = div_obj.find("img")["title"]
            
            if speaker_name == scraper_name:
                image = image_url

    return image 

get_imageurl("Alice Weidel")