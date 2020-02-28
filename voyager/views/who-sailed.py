from collections import namedtuple

from flask import g
from flask import escape
from flask import render_template
from flask import request

from voyager.db import get_db, execute
from voyager.validate import validate_field, render_errors
from voyager.validate import NAME_RE, INT_RE, DATE_RE


def search(conn, bName):
    return execute(conn, "SELECT s.sid FROM Sailors AS s INNER JOIN Boats ON s.sid="+bName)

def views(bp):
    @bp.route("/who-sailed")
    def _voyages():
        with get_db() as conn:
            bName = request.args.get("boat-name")
            rows = search(conn, bName)
        return render_template("table.html", name="who-sailed", rows=rows)