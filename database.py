import datetime
import sqlite3


class Database:

    def __init__(self):
        self.dbname = "./data/earthquake_data.db"

    # Execute SELECT query with given conditions
    def select(self, conditions=[]):
        print(conditions)
        where = ""
        conn = sqlite3.connect(self.dbname)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        # Create where clause
        if len(conditions) > 0:
            where = "WHERE "
            where += ("e.place LIKE '%" + conditions["location"] + "%' AND ") if conditions["location"] else ''
            where += ("e.net = '" + conditions["source"] + "' AND ") if conditions["source"] else ''
            # Remove unnecessary 'AND' at the tail
            where = where.removesuffix("AND ")

        cur.execute(
            "SELECT e.time, e.depth, e.mag, e.magType, e.place, s.name " +
            "FROM earthquakes e LEFT JOIN sources s on e.net = s.id "
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

    # Execute SELECT query to sources table
    def select_sources(self):
        conn = sqlite3.connect(self.dbname)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT id, name FROM sources")

        return cur.fetchall()
