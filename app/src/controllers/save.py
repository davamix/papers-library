import json
from flask import request
from flask.views import MethodView

class SaveController(MethodView):
    def __init__(self):
        pass

    def post(self):
        data = request.get_json()

        if data:
            print(f"Saving: {data}")

        return "", 204

    