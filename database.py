import datetime
import sqlite3
from flask import flash


class Database:

    def __init__(self):
        self.dbname = "./data/earthquake_data.db"

    def select(self, conditions={}):
        """Execute SELECT query with given conditions"""
        where = ""
        order_by = ""
        conn = sqlite3.connect(self.dbname)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        if conditions:
            # Create WHERE clause
            try:
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

            except Exception as e:
                flash(f"ERROR: Failed to set conditions - {e}", "error")

        try:
            cur.execute(
                "SELECT e.time, e.depth, e.mag, e.magType, e.place, s.name " +
                "FROM earthquakes e LEFT JOIN sources s on e.net = s.id "
                + where + order_by
            )
        except Exception as e:
            flash(f"ERROR: Failed to execute SQL - {e}", "error")

        # Convert to dict type because Sqlite3 Row type does not allow values update
        rows = [dict(row) for row in cur]

        # return records and the number of record
        return map(self.cleansing_data, rows), len(rows)

    #
    def select_mag_top5(self):
        """Execute SELECT query to get TOP5 biggest magnitude"""
        conn = sqlite3.connect(self.dbname)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        try:
            cur.execute(
                "SELECT e.time, e.depth, e.mag, e.magType, e.place, s.name " +
                "FROM earthquakes e LEFT JOIN sources s on e.net = s.id ORDER BY e.mag DESC LIMIT 5"
            )
        except Exception as e:
            flash(f"ERROR: Failed to execute SQL - {e}", "error")

        # Convert to dict type because Sqlite3 Row type does not allow values update
        rows = [dict(row) for row in cur]

        return map(self.cleansing_data, rows)

    def select_depth_top5(self):
        """Execute SELECT query to get TOP5 deepest"""
        conn = sqlite3.connect(self.dbname)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        try:
            cur.execute(
                "SELECT e.time, e.depth, e.mag, e.magType, e.place, s.name " +
                "FROM earthquakes e LEFT JOIN sources s on e.net = s.id ORDER BY e.depth DESC LIMIT 5"
            )
        except Exception as e:
            flash(f"ERROR: Failed to execute SQL - {e}", "error")

        # Convert to dict type because Sqlite3 Row type does not allow values update
        rows = [dict(row) for row in cur]

        return map(self.cleansing_data, rows)

    def select_country_top5(self):
        """Execute SELECT query to get TOP3 country"""
        conn = sqlite3.connect(self.dbname)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        try:
            cur.execute(
                "SELECT ROW_NUMBER() OVER(ORDER BY  COUNT(*) DESC) rank, country, COUNT(*) as count " +
                "FROM earthquakes e GROUP BY e.country ORDER BY COUNT(*) DESC LIMIT 5"
            )
        except Exception as e:
            flash(f"ERROR: Failed to execute SQL - {e}", "error")

        return cur.fetchall()

    def select_sources(self):
        """Execute SELECT query to sources table"""
        conn = sqlite3.connect(self.dbname)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        try:
            cur.execute("SELECT id, name FROM sources")
        except Exception as e:
            flash(f"ERROR: Failed to execute SQL - {e}", "error")

        return cur.fetchall()

    def select_mag_types(self):
        """Execute SELECT query to magnitude_types table"""
        conn = sqlite3.connect(self.dbname)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        try:
            cur.execute("SELECT id, mag_range, distance_range, equation, comments FROM magnitude_types")
        except Exception as e:
            flash(f"ERROR: Failed to execute SQL - {e}", "error")

        return cur.fetchall()

    @staticmethod
    def cleansing_data(row):
        """Clean original opensource data to make easy to understand"""
        try:
            # Remove 'Z' which causes the ISO date format conversion error
            d = datetime.datetime.fromisoformat(row["time"].replace('Z', ''))
        except RuntimeError as e:
            flash(f"ERROR: Failed to convert ISO time - {e}", "error")

        try:
            # Set cleaned value to a original object
            row["time"] = d.strftime('%d/%m/%Y %H:%M:%S')
            row["depth"] = format(float(row["depth"]), '.2f')
            row["mag"] = format(float(row["mag"]), '.2f')
        except Exception as e:
            flash(f"ERROR: Failed to access value - {e}", "error")

        return row
