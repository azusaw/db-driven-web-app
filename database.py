import datetime
import sqlite3


class Database:
    dbname = "./data/earthquake_data.db"

    def __init__(self):
        pass

    # Execute SELECT query with given conditions
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

        # Convert to dict type because Sqlite3 Row type does not allow values update
        rows = [dict(row) for row in cur]

        return map(self.cleansing_data, rows)

    # Clean original opensource data to make easy to understand
    @staticmethod
    def cleansing_data(row):
        # Remove 'Z' which causes the ISO date format conversion error
        d = datetime.datetime.fromisoformat(row["time"].replace('Z', ''))

        row["time"] = d.strftime('%d/%m/%Y %H:%M:%S')
        row["depth"] = format(float(row["depth"]), '.2f')
        row["mag"] = format(float(row["mag"]), '.2f')

        return row
