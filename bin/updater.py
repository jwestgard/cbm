#!/usr/bin/env python3

import csv
import sys

with open(sys.argv[1]) as repofile:
    repos = [row for row in csv.DictReader(repofile)]

with open(sys.argv[2]) as cityfile:
    cities = {row['old_id']: row['id'] for row in csv.DictReader(cityfile)}

for repo in repos:
    repo['city_id'] = int(cities[repo['city_id']])

repos.sort(key=lambda x: x['city_id'])

for n, repo in enumerate(repos, 1):
    repo['old_id'] = repo['id']
    repo['id'] = n
    if repo['website'] and not repo['website'].startswith('http'):
        repo['website'] = 'http://' + repo['website']


with open('output.csv', 'w') as handle:
    fieldnames = ['id', 'old_id', 'city_id', 'name', 
                  'address', 'website', 'other_name', 'abbreviation']
    writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction='ignore')
    writer.writeheader()
    for repo in repos:
        writer.writerow(repo)
