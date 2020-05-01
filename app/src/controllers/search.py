import json
import urllib.request
import feedparser
from datetime import datetime
from flask import request
from flask.views import MethodView
from flask_socketio import emit

class SearchController(MethodView):
    def __init__(self, socket, database_service):
        self.arxiv_url = "http://export.arxiv.org/api/query?"
        self.socket = socket
        self.database = database_service
        pass

    def post(self):
        data = request.get_json()

        if data:
            self.socket.emit("searching", "Searching in database...")
            paper = self.get_from_database(data["paperId"])

            if paper is None:
                self.socket.emit("searching", "Searching in Arxiv...")
                paper = self.get_from_arxiv(data["paperId"])

            return paper, 206

        return "", 204

    def get_from_database(self, paper_id):
        print("### Searching in DB...")
        return self.database.get_paper(paper_id)

    def get_from_arxiv(self, paper_id):
        print("### Searching in Arxiv...")
        query = self.arxiv_url + "id_list=" + paper_id

        try:
            with urllib.request.urlopen(query) as url:
                response = url.read()
        except urllib.error.HTTPError as e:
            return {"error": "NotFound", "message": e.reason}

        parse = feedparser.parse(response)

        if len(parse["entries"]) > 0:
            paper = {
                "paper_id": paper_id,
                "title": parse["entries"][0]["title"],
                "abstract": parse["entries"][0]["summary"].replace("\n", " "),
                "authors": self.extract_authors(parse["entries"][0]),
                "link_pdf": self.extract_link_pdf(parse["entries"][0]),
                "published": self.extract_date(parse["entries"][0]["published"]),
                "updated": self.extract_date(parse["entries"][0]["updated"]),
                "data_from": "arxiv"
            }

        return paper

    def extract_date(self, string_datetime):
        if string_datetime:
            return string_datetime.split("T")[0]
        
        return None

    def extract_authors(self, data):
        return ", ".join([a["name"] for a  in data["authors"]])

    def extract_link_pdf(self, data):
        return next((x["href"] for x in data["links"] if x["type"] == "application/pdf"), None)