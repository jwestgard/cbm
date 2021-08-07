from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy import insert

import csv
import sys

DBFILE = sys.argv[1]

if __name__ == "__main__":

    engine = create_engine(f"sqlite+pysqlite:///{DBFILE}", echo=True, future=True)

    metadata = MetaData()

    countries_table = Table(
        "countries",
        metadata,
        Column('id', Integer, primary_key=True),
        Column('old_id', Integer),
        Column('name', String(30)),
        Column('native', String)
    )

    cities_table = Table(
        "cities",
        metadata,
        Column('id', Integer, primary_key=True),
        Column('old_id', Integer),
        Column('name', String(50)),
        Column('native', String),
        Column('country_id', ForeignKey('countries.id'), nullable=False)
    )

    metadata.create_all(engine)

    countries_data = [row for row in csv.DictReader(open('csv/countries.csv'))]
    cities_data = [row for row in csv.DictReader(open('csv/cities.csv'))]

    with engine.connect() as conn:
        result = conn.execute(insert(countries_table), countries_data)
        conn.commit()

    with engine.connect() as conn:
        result = conn.execute(insert(cities_table), cities_data)
        conn.commit()

