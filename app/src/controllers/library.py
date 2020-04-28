from flask import render_template
from flask.views import MethodView

class LibraryController(MethodView):
    def __init__(self):
        pass

    def get(self):
        return render_template("main.html", title="Papers Library")