import datetime
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
            "select e.time, e.depth, e.mag, e.magType, e.place, s.name " +
            "from earthquakes e left join sources s on e.net = s.id "
            + where
        )
        rows = [dict(row) for row in cur]
        return map(self.cleansing_data, rows)

    @staticmethod
    def cleansing_data(row):
        d = datetime.datetime.fromisoformat(row["time"].replace('Z', ''))
        row["time"] = d.strftime('%d/%m/%Y %H:%M:%S')
        row["depth"] = format(float(row["depth"]), '.2f')
        row["mag"] = format(float(row["mag"]), '.2f')
        return row
