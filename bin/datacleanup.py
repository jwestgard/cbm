#!/usr/bin/env python3

import csv
import os
import sys

INPUT = sys.argv[1]
OUTPUT = sys.argv[2]

with open(INPUT) as handle:
    data = [{'id': row[0],
             'name': row[1],
             'native': row[2],
             'country_id': row[4]
             } for row in csv.reader(handle)]

with open(OUTPUT, 'w') as handle:
    writer = csv.DictWriter(handle, fieldnames=['id','name','native','country_id'])
    writer.writeheader()
    for row in data:
        print(row)
        writer.writerow(row)
