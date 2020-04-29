from flask import render_template
from flask.views import MethodView
from flask_socketio import emit

class LibraryController(MethodView):
    def __init__(self, socket, database_service):
        self.socket = socket
        self.database = database_service
        
        self.socket.on_event("load_papers", self.load_papers)

    def get(self):
        return render_template("main.html", title="Papers Library")


    def load_papers(self):
        print("### Loading papers...")
        data = self.database.get_papers()

        print(data)
        self.socket.emit("papers_loaded", data)