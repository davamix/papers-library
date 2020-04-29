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
                    "authors": self.get_authors(parse["entries"][0]),
                    "link_pdf": self.get_link_pdf(parse["entries"][0])
                }

                return paper, 206

            print(parse)

        return "", 204

    def get_authors(self, data):
        return ", ".join([a["name"] for a  in data["authors"]])

    def get_link_pdf(self, data):
        return next((x["href"] for x in data["links"] if x["type"] == "application/pdf"), None)