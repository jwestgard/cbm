import csv
import sys

from flask import Flask
from flask import render_template
from flask_bootstrap import Bootstrap

from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import select
from sqlalchemy import Table


DBFILE = sys.argv[1]

app = Flask(__name__)
bootstrap = Bootstrap(app)
engine = create_engine(f"sqlite+pysqlite:///{DBFILE}", echo=True, future=True)
metadata = MetaData()

works = Table('works', metadata, autoload_with=engine)
countries = Table('countries', metadata, autoload_with=engine)
cities = Table('cities', metadata, autoload_with=engine)
entries = Table('entries', metadata, autoload_with=engine)


class Work():
    def __init__(self, **kwargs):
        super().__init__()
        for k, v in kwargs.items():
            setattr(self, k, v)


@app.route("/")
def index():
    with open("csv/opera.csv") as handle:
        works = [Work(**row) for row in csv.DictReader(handle)]
    return render_template("home.html", works=works)


@app.route("/works")
def works_list():
    with engine.connect() as conn:
        results = conn.execute(
            select(works)
            ).fetchall()
    return render_template("home.html", works=results)


@app.route("/works/<abbreviation>")
def single_work(abbreviation):
    with engine.connect() as conn:
        work = conn.execute(
            select(works).where(works.c.abbreviation == abbreviation)
            ).fetchone()
        mss = conn.execute(
            select(entries).where(entries.c.work_id == work.id)
            ).fetchall()
    return render_template("work.html", work=work, mss=mss)


@app.route("/countries")
def country_list():
    with engine.connect() as conn:
        results = conn.execute(
            select(text('* from countries'))
            ).fetchall()
    return render_template("countries.html", countries=results)


@app.route("/countries/<country_id>")
def city_list(country_id):
    with engine.connect() as conn:
        results = conn.execute(
            select(cities).where(cities.c.country_id == country_id)
            ).fetchall()
    return render_template("cities.html", cities=results)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
