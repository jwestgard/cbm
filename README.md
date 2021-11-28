# Census of Bede Manuscripts (CBM)

## Bootstrap

* Purpose: Loads data stored in CSV files into a SQLite database file
* Usage: python -m bootstrap <DB_FILE>
* Notes: Currently creates four tables: cities, countries, entries, works

## Viewer

* Purpose: Serves webpages listing the manuscripts containing each of Bede's works
* Usage: python -m viewer <DB_FILE> 
* Notes: 
    - Creates a master index listing works in the works table
    - Creates a page for each work listing manuscripts in the entries table and joining data in the cities and countries tables
    - Serves the site at http://127.0.0.1:5000/
