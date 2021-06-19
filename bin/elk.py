#!/usr/bin/env python3

import csv
import os
import sys

datadir =  "/Users/westgard/Dev/census/filemaker/export"
tables = ["cities", "countries", "lk_entries", "manuscripts"]
data = dict()

column_lists = {
    "lk_entries":      ["id", "manuscripts_id", "orig_id", "page", "settlement", 
                    "repository", "idno", "locus", "opus", "author", "provenance", 
                    "dating", "refs", "raw_text"
                    ],
    "manuscripts":  ["id", "opus", "texttype", "bool", "repository", "shelfmark", 
                    "notes", "entry", "support", "extent", "units", "unknown_L", 
                    "unknown_M", "unknown_N", "unknown_O", "unknown_P", "unknown_Q", 
                    "unknown_R", "dating", "c_early", "c_late", "y_early", "y_late", 
                    "prov_country", "prov_institution", "prov_later", "initials",
                    "update_timestamp", "unknown_AC", "unknown_AD", "list_xml", 
                    "original_entry", "sm_pref", "sm_base", "sm_suff", "sm_full", 
                    "unknown_AK", "lit_refs", "provenances"
                    ],
    "repositories": ["id", "city_id", "name", "address", "website", "blank", 
                    "name_former", "name_short"
                    ],
    "cities":       ["id", "name_english", "name_native", "blank", "country_id"
                    ],
    "countries":    ["id", "name_english", "name_native"
                    ]
    }

def create_datalist(table, cols):
    num_cols = len(cols)
    results = []
    with open(table) as handle:
        for row in csv.reader(handle):
            print(row)
            if len(row) == num_cols:
                rowdict = dict(zip(row, cols))
                results.append(rowdict)
            else:
                print('error')
        return results

for table in tables:
    print(f"Working on {table}")
    filepath = os.path.join(datadir, table + '.csv')
    cols = column_lists.get(table)
    data[table] = create_datalist(filepath, cols)

for table, rows in data.items():
    print(table, len(rows))