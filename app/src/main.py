from pathlib import Path
from flask import Flask

from controllers.library import LibraryController
from controllers.search import SearchController

templates_path = Path(Path.cwd(), "src", "templates")

app = Flask(__name__, template_folder=templates_path)

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