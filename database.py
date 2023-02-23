import datetime
import sqlite3


class Database:

    def __init__(self):
        self.dbname = "./data/earthquake_data.db"

    # Execute SELECT query with given conditions
    def select(self, conditions={}):
        where = ""
        order_by = ""
        conn = sqlite3.connect(self.dbname)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        if conditions:
            # Create WHERE clause
            where = "WHERE 1 AND "
            where += ("e.place LIKE '%" + conditions["place"] + "%' AND ") if conditions["place"] else ''
            where += ("e.net = '" + conditions["source"] + "' AND ") if conditions["source"] else ''
            where += ("e.mag >= '" + conditions["min-mag"] + "' AND ") if conditions["min-mag"] else ''
            where += ("e.mag <= '" + conditions["max-mag"] + "' AND ") if conditions["max-mag"] else ''
            where += ("e.depth >= '" + conditions["min-depth"] + "' AND ") if conditions["min-depth"] else ''
            where += ("e.depth <= '" + conditions["max-depth"] + "' AND ") if conditions["max-depth"] else ''
            where += ("e.magType = '" + conditions["mag-type"] + "' AND ") if conditions["mag-type"] else ''

            # Remove unnecessary "AND " at the tail
            where = where.removesuffix("AND ")

            # Create ORDER BY clause
            order_by = (" ORDER BY " + conditions["order"]) if conditions["order"] else ''

        cur.execute(
            "SELECT e.time, e.depth, e.mag, e.magType, e.place, s.name " +
            "FROM earthquakes e LEFT JOIN sources s on e.net = s.id "
            + where + order_by
        )

        # Convert to dict type because Sqlite3 Row type does not allow values update
        rows = [dict(row) for row in cur]

        # return records and the number of record
        return map(self.cleansing_data, rows), len(rows)

    # Execute SELECT query to get TOP3 biggest magnitude
    def select_mag_top3(self):
        conn = sqlite3.connect(self.dbname)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        cur.execute(
            "SELECT e.time, e.depth, e.mag, e.magType, e.place, s.name " +
            "FROM earthquakes e LEFT JOIN sources s on e.net = s.id ORDER BY e.mag DESC LIMIT 3"
        )

        # Convert to dict type because Sqlite3 Row type does not allow values update
        rows = [dict(row) for row in cur]

        return map(self.cleansing_data, rows)

    # Execute SELECT query to get TOP3 deepest
    def select_depth_top3(self):
        conn = sqlite3.connect(self.dbname)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        cur.execute(
            "SELECT e.time, e.depth, e.mag, e.magType, e.place, s.name " +
            "FROM earthquakes e LEFT JOIN sources s on e.net = s.id ORDER BY e.depth DESC LIMIT 3"
        )

        # Convert to dict type because Sqlite3 Row type does not allow values update
        rows = [dict(row) for row in cur]

        return map(self.cleansing_data, rows)

    # Execute SELECT query to get TOP3 country
    def select_country_top5(self):
        conn = sqlite3.connect(self.dbname)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        cur.execute(
            "SELECT ROW_NUMBER() OVER(ORDER BY  COUNT(*) DESC) rank, country, COUNT(*) as count " +
            "FROM earthquakes e GROUP BY e.country ORDER BY COUNT(*) DESC LIMIT 5"
        )

        return cur.fetchall()

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

    # Execute SELECT query to magnitude_types table
    def select_mag_types(self):
        conn = sqlite3.connect(self.dbname)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT id, mag_range, distance_range, equation, comments FROM magnitude_types")

        return cur.fetchall()
