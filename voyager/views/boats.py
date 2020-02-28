
from collections import namedtuple

from flask import render_template
from flask import request
from flask import escape

from voyager.db import get_db, execute

def boats(conn):
    return execute(conn, "SELECT b.bid, b.name, b.color FROM Boats AS b")

def boatSearch(conn, sName):
    return execute(conn, "SELECT DISTINCT b.name FROM Boats AS b INNER JOIN Voyages AS v ON v.bid=b.bid INNER JOIN Sailors AS s ON s.sid=v.sid WHERE s.name="+sName)

def boatPopularity(conn):
    return execute(conn, "SELECT DISTINCT b.name, count(*) FROM Boats AS b INNER JOIN Voyages AS v ON v.bid=b.bid GROUP BY b.name ORDER BY count() DESC")

def views(bp):
    @bp.route("/boats")
    def _boats():
        with get_db() as conn:
            rows = boats(conn)
        return render_template("table.html", name="boats", rows=rows)
    @bp.route("/boats/sailed-by")
    def _boatSailed():
        with get_db() as conn:
            sName = '\'' + request.args.get("sailor-name") + '\''
            rows = boatSearch(conn, sName)
        return render_template("table.html", name="What boat did they sail?", rows=rows)
    @bp.route("/boats/by-popularity")
    def _boatPop():
        with get_db() as conn:
            rows = boatPopularity(conn)
        return render_template("table.html", name="Most Popular Boats", rows=rows)
    @bp.route("/boats/add")
    def _addBoat():
        with get_db() as conn:
            rows = boatSearch(conn, "'k'")
        return render_template("table.html", name="Add a Boat", rows=rows)
