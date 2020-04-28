import json
import urllib.request
import feedparser
from flask import request
from flask.views import MethodView

class SearchController(MethodView):
    def __init__(self):
        self.arxiv_url = "http://export.arxiv.org/api/query?"
        pass

    def post(self):
        data = request.get_json()

        if data:
            print(data)
            
            query = self.arxiv_url + "id_list=" + data["paperId"]
            print(query)

            with urllib.request.urlopen(query) as url:
                response = url.read()

            parse = feedparser.parse(response)

            if len(parse["entries"]) > 0:
                paper = {
                    "title": parse["entries"][0]["title"],
                    "abstract": parse["entries"][0]["summary"].replace("\n", " "),
                    "authors": ", ".join([a["name"] for a  in parse["entries"][0]["authors"]])
                }

                return paper, 206

            print(parse)

        return "", 204