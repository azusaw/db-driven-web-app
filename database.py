import sqlite3


class Database:
    dbname = "./data/earthquake_data.db"

    def __init__(self):
        pass

    def select(self, where=""):
        print(where)
        conn = sqlite3.connect(self.dbname)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(
            "select e.time, e.latitude, e.longitude, e.depth, e.mag, e.magType, e.place, e.type, e.status, s.name " +
            "from earthquakes e left join sources s on e.net = s.id "
            + where
        )
        return cur.fetchall()
