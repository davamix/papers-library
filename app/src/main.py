from pathlib import Path
from flask import Flask
from flask_socketio import SocketIO
# from pymongo import MongoClient

from controllers.library import LibraryController
from controllers.search import SearchController
from controllers.save import SaveController

from services.database import DatabaseService

templates_path = Path(Path.cwd(), "src", "templates")

app = Flask(__name__, template_folder=templates_path)
socketio = SocketIO(app)

database_service = DatabaseService()

# https://stackoverflow.com/a/45438226/844372
@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET, PUT, POST, DELETE, OPTIONS")

    return response

app.add_url_rule("/library", view_func=LibraryController.as_view("library", socket=socketio, database_service=database_service))
app.add_url_rule("/search", view_func=SearchController.as_view("search", socket=socketio, database_service=database_service))
app.add_url_rule("/save", view_func=SaveController.as_view("save", socket=socketio, database_service=database_service))

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", debug=True)