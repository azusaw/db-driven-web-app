from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    conn = sqlite3.connect("./data/earthquake_data.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("select e.time, e.latitude, e.longitude, e.depth, e.mag, e.magType,  e.place, e.type, e.status, s.name from earthquakes e left join sources s on e.net = s.id ")
    rows = cur.fetchall()
    return render_template('index.html', rows=rows)

if __name__ == "__main__":
    app.run(debug=True)