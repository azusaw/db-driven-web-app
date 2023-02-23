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
    mag_types = db.select_mag_types()
    if request.method == "POST":
        rows = db.select(request.form.to_dict(flat=True))
    return render_template("search.html", rows=rows, sources=sources, mag_types=mag_types)


@app.route('/magnitude_type')
def magnitude_type():
    rows = db.select_mag_types()
    return render_template("magnitude_type.html", rows=rows)


if __name__ == "__main__":
    app.run(port=8000, debug=True)
