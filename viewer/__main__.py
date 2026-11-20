import csv
import sys

from flask import Flask
from flask import render_template
from flask_bootstrap import Bootstrap

from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import select
from sqlalchemy import Table
from sqlalchemy.orm import DeclarativeBase


DBFILE = sys.argv[1]

app = Flask(__name__)
bootstrap = Bootstrap(app)
engine = create_engine(f"sqlite+pysqlite:///{DBFILE}", echo=True, future=True)

class Base(DeclarativeBase):
    pass

metadata = Base.metadata
registry = Base.registry

works = Table('works', metadata, autoload_with=engine)
manuscripts = Table('manuscripts', metadata, autoload_with=engine)
repositories = Table('repositories', metadata, autoload_with=engine)
countries = Table('countries', metadata, autoload_with=engine)
cities = Table('cities', metadata, autoload_with=engine)
entries = Table('entries', metadata, autoload_with=engine)

'''
registry.map_imperatively(
    Repository,
    repositories,
    properties={"city": relationship("City", back_populates="repositories")},
)

registry.map_imperatively(
    City,
    cities,
    properties={"country": relationship("Country", back_populates="cities")},
)
'''

@app.route("/")
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


@app.route("/manuscripts")
def mss_list():
    with engine.connect() as conn:
        results = conn.execute(
            select(manuscripts)
            ).fetchall()
    return render_template("manuscripts.html", manuscripts=results)


@app.route("/countries")
def country_list():
    with engine.connect() as conn:
        results = conn.execute(
            select(countries)
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
