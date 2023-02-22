from flask import Flask, render_template, request
import database

app = Flask(__name__)
db = database.Database()


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/all")
def all():
    rows = db.select()
    return render_template("all.html", rows=rows)


@app.route("/search", methods=["GET", "POST"])
def search():
    # "where e.mag > 5.0"
    rows = ""
    if request.method == "POST":
        rows = db.select(request.form["where"])
    return render_template("search.html", rows=rows)


if __name__ == "__main__":
    app.run(debug=True)
