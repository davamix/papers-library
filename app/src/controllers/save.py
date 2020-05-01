import json
from flask import request
from flask.views import MethodView

class SaveController(MethodView):
    def __init__(self, socket, database_service):
        self.socket = socket
        self.database = database_service

    def post(self):
        data = request.get_json()

        # Notify when saved
        if data:
            try:
                self.database.save(data)
                self.socket.emit("saved", {"status": "ok", "message": "Paper saved corretly"})
            except:
                self.socket.emit("saved", {"status": "error", "message": "Error on saved"})



        return "", 204

    