import sys

import requests


class Imager:
    def __init__(self, title, artist):
        self.title = title
        self.artist = artist

    def get_data(self):
        url = self.get_url()
        return self.extract_image(url)

    def get_url(self):
        data = {"term": self.title, "media": "music", "entity": "song", "country": "RU", "limit": 50}
        r = requests.get("https://itunes.apple.com/search", params=data)

        for res in r.json()["results"]:
            if res["artistName"] in (self.artist, "Разные артисты"):
                return res["artworkUrl60"]

    def extract_image(self, url):
        if url is None:
            print("Can't find")
            sys.exit()
        url = url.replace("60x60bb", "1920x1080bb")
        r = requests.get(url)
        return r.content
