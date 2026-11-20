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
        "countries", metadata,
        Column('id', Integer, primary_key=True),
        Column('old_id', Integer),
        Column('name', String(30)),
        Column('native', String)
    )

    cities_table = Table(
        "cities", metadata,
        Column('id', Integer, primary_key=True),
        Column('old_id', Integer),
        Column('name', String(50)),
        Column('native', String),
        Column('country_id', ForeignKey('countries.id'), nullable=False)
    )

    repositories_table = Table(
        "repositories", metadata,
        Column('id', Integer, primary_key=True),
        Column('old_id', Integer),
        Column('city_id', ForeignKey('cities.id'), nullable=False),
        Column('name', String(50)),
        Column('address', String),
        Column('website', String(50)),
        Column('other_name', String(50)),
        Column('abbreviation', String(50)),
    )

    manuscripts_table = Table(
        "manuscripts", metadata,
        Column('id', Integer, primary_key=True),
        Column('excluded', String(50)),
        Column('repo_id', ForeignKey('repositories.id'), nullable=False),
        Column('notes', String),
        Column('support', String(50)),
        Column('extent', String(50)),
        Column('length', String(50)),
        Column('numbered_by', String(50)),
        Column('sm_alpha_part', String(50)),
        Column('sm_num_part', Integer),
        Column('sm_suffix', String(50))
    )

    works_table = Table(
        "works", metadata,
        Column('id', Integer, primary_key=True),
        Column('abbreviation', String(10)),
        Column('abbreviation_long', String(30)),
        Column('title_lat', String),
        Column('title_eng', String),
        Column('refs', String)
    )

    entries_table = Table(
        "entries", metadata,
        Column('id', Integer, primary_key=True),
        Column('manuscript_id', Integer),
        Column('work_id', ForeignKey('works.id'), nullable=False),
        Column('section', String(75)),
        Column('subsection', String(75)),
        Column('extract', String(75)),
        Column('page', Integer),
        Column('settlement', String(50)),
        Column('repository', String(75)),
        Column('shelfmark', String(50)),
        Column('locus', String(75)),
        Column('provenance', String(50)),
        Column('dating', String(10)),
        Column('refs', String),
        Column('rawtext', String),
        Column('notes', String),
    )

    metadata.create_all(engine)

    with engine.connect() as conn:
        countries_data = [row for row in csv.DictReader(open('csv/countries.csv'))]
        conn.execute(insert(countries_table), countries_data)
        conn.commit()

    with engine.connect() as conn:
        cities_data = [row for row in csv.DictReader(open('csv/cities.csv'))]
        conn.execute(insert(cities_table), cities_data)
        conn.commit()

    with engine.connect() as conn:
        repositories_data = [row for row in csv.DictReader(open('csv/repositories.csv'))]
        conn.execute(insert(repositories_table), repositories_data)
        conn.commit()

    with engine.connect() as conn:
        mss_data = [row for row in csv.DictReader(open('csv/mss.csv'))]
        conn.execute(insert(manuscripts_table), mss_data)
        conn.commit()

    with engine.connect() as conn:
        works_data = [row for row in csv.DictReader(open('csv/opera.csv'))]
        conn.execute(insert(works_table), works_data)
        conn.commit()

    with engine.connect() as conn:
        entries_data = [row for row in csv.DictReader(open('csv/entries.csv'))]
        conn.execute(insert(entries_table), entries_data)
        conn.commit()
