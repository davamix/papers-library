from pathlib import Path
from flask import Flask

from pymongo import MongoClient

from controllers.library import LibraryController
from controllers.search import SearchController

templates_path = Path(Path.cwd(), "src", "templates")

app = Flask(__name__, template_folder=templates_path)

## Testing db connection
# client_db = MongoClient("mongodb://mongodb:27017") # mongodb://service_name_in_docker_compose:27017
# database = client_db.papers_db
# papers = database.papers_collection
# print(f"## All papers: {papers.count_documents({})}")
# paper = {
#     "paper_id": "1111.1111",
#     "title": "Paper title",
#     "abstract": "A lot of words in the abstract",
#     "authors": "My cat",
#     "link_pdf": "http://server.com/paper"
# }
# paper_mongo_id = papers.insert_one(paper).inserted_id
# print(f"## INSERTED PAPER: {paper_mongo_id}")
# print(papers.count_documents({}))


# https://stackoverflow.com/a/45438226/844372
@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET, PUT, POST, DELETE, OPTIONS")

    return response

app.add_url_rule("/library", view_func=LibraryController.as_view("library"))
app.add_url_rule("/search", view_func=SearchController.as_view("search"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)