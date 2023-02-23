from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap

import database

app = Flask(__name__)
bootstrap = Bootstrap(app)
db = database.Database()


@app.route('/')
def home():
    return render_template("home.html")


@app.route("/all")
def all():
    rows = db.select()
    return render_template("all.html", rows=rows)


@app.route("/search", methods=["GET", "POST"])
def search():
    rows = ""
    sources = db.select_sources()
    if request.method == "POST":
        rows = db.select(request.form.to_dict(flat=True))
    return render_template("search.html", rows=rows, sources=sources)


if __name__ == "__main__":
    app.run(port=8000, debug=True)
