from collections import namedtuple

from flask import g
from flask import escape
from flask import render_template
from flask import request

from voyager.db import get_db, execute
from voyager.validate import validate_field, render_errors
from voyager.validate import NAME_RE, INT_RE, DATE_RE


def sailors(conn):
    return execute(conn, "SELECT s.sid, s.name, s.age, s.experience  FROM Sailors AS s")

def search(conn, bName):
    return execute(conn, "SELECT DISTINCT s.name FROM Sailors AS s INNER JOIN Voyages AS v ON v.sid=s.sid INNER JOIN Boats AS b ON b.bid=v.bid WHERE b.name="+bName)

def dateSearch(conn, date):
    return execute(conn, "SELECT DISTINCT s.name FROM Sailors AS s INNER JOIN Voyages AS v ON v.sid=s.sid WHERE v.date_of_voyage="+date)

def colorSearch(conn, color):
    return execute(conn, "SELECT DISTINCT s.name FROM Sailors AS s INNER JOIN Voyages AS v ON v.sid=s.sid INNER JOIN Boats AS b ON b.bid=v.bid WHERE b.color="+color)

def views(bp):
    @bp.route("/sailors")
    def _get_all_sailors():
        with get_db() as conn:
            rows = sailors(conn)
        return render_template("table.html", name="sailors", rows=rows)
    @bp.route("/sailors/who-sailed")
    def _boatSailors():
        with get_db() as conn:
            bName = '\'' + request.args.get("boat-name") + '\''
            rows = search(conn, bName)
        return render_template("table.html", name="Who sailed that boat?", rows=rows)
    @bp.route("/sailors/who-sailed-on-date")
    def _dateSailed():
        with get_db() as conn:
            date = '\'' + request.args.get("date") + '\''
            rows = dateSearch(conn, date)
        return render_template("table.html", name="Who sailed that day?", rows=rows)
    @bp.route("/sailors/who-sailed-on-boat-of-color")
    def _colorSailed():
        with get_db() as conn:
            color = '\'' + request.args.get("color") + '\''
            rows = colorSearch(conn, color)
        return render_template("table.html", name="Who sailed that color of boat?", rows=rows)
    @bp.route("/sailors/add")
    def _addSailor():
        with get_db() as conn:
            rows = search(conn, "'k'")
        return render_template("table.html", name="Add a Sailor", rows=rows)