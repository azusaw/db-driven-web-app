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
    if request.method == "POST":
        where = "where " + \
                "place like '%" + request.form["location"] + "%'" if request.form["location"] else ''
        rows = db.select(where)
    return render_template("search.html", rows=rows)


if __name__ == "__main__":
    app.run(port=8000, debug=True)
