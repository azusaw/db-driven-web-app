from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap

import database

app = Flask(__name__)
bootstrap = Bootstrap(app)
db = database.Database()


@app.route('/')
def home():
    return render_template("home_page.html")


@app.route("/all")
def all():
    rows, cnt = db.select()
    return render_template("all_page.html", rows=rows, cnt=cnt)


@app.route("/search", methods=["GET", "POST"])
def search():
    rows = ""
    cnt = 0
    sources = db.select_sources()
    mag_types = db.select_mag_types()
    if request.method == "POST":
        rows, cnt = db.select(request.form.to_dict(flat=True))
    return render_template("search_page.html", rows=rows, cnt=cnt, sources=sources, mag_types=mag_types)


@app.route("/ranking")
def ranking():
    mag_rows = db.select_mag_top3()
    depth_rows = db.select_depth_top3()
    country_rows = db.select_country_top5()
    return render_template("ranking_page.html", mag_rows=mag_rows, depth_rows=depth_rows, country_rows=country_rows)


@app.route('/magnitude_type')
def magnitude_type():
    rows = db.select_mag_types()
    return render_template("magnitude_type_page.html", rows=rows)


if __name__ == "__main__":
    app.run(port=8000, debug=True)
