from __future__ import print_function

import os
import sys
import time
import pilosa

from pilosa import Client, Index, TimeQuantum
from pilosa.imports import csv_column_reader, csv_row_id_column_id

try:
    # Python 2.7 and 3 are used here
    from io import StringIO
except ImportError:
    #Python 2.6 and 2.7 are used here
    from StringIO import StringIO

# Creating the Schema
client = pilosa.Client()
schema = client.schema()
# This is where the index will go later
# This is where the fields will go later
repository = schema.index("repository")
stargazer = repository.field("stargazer", time_quantum=pilosa.TimeQuantum.YEAR_MONTH_DAY)
language = repository.field("language")
client.sync_schema(schema)

# Now we are loading our data into the stargazer field
time_func = lambda s: int(time.mktime(time.strptime(s, "%Y-%m-%dT%H:%M")))
with open("stargazer.csv") as f:
    stargazer_reader = csv_column_reader(f, timefunc=time_func)
    client.import_field(stargazer, stargazer_reader)

# Now we are loading our data into the langauge field
with open("language.csv") as f:
    language_reader = csv_column_reader(f, csv_row_id_column_id)
    client.import_field(language, language_reader)

# Now lets make some queries on csv files to measure the peformance of pilosa bitmapping technique :-

# Query 1: Let's find out which repositories did user 14 starred.
response = client.query(stargazer.row(14))
print("User 14 starredd: ", response.result.row.columns)

# Query2 : What are the top 5 programming language in sample data.
def load_language_names():
    with open("languages.txt") as f:
        return [line.strip() for line in f]

def print_topn(items):
    lines = ["\t{i}. {s[0]}: {s[1]} stars".format(s=s, i = i + 1) for i, s in enumerate(items)]
    print("\n".join(lines))

language_names = load_language_names()
top_languages = client.query(language.topn(5)).result.count_items
language_items = [(language_names[item.id], item.count) for item in top_languages]

print("Top languages: ")
print_topn(language_items)

#Query 3 : which repositories were starred by user 14 or 19.

repsonse = client.query(repository.intersect(stargazer.row(14), stargazer.row(19)))
print("Both user 14 and 19 starred: ", response.result.row.columns)

#Query 4 : which repositories were starred by user 14 or 19 and were also written in langauge 1.

response = client.query(repository.intersect(stargazer.row(14), stargazer.row(19), language.row(1)))
print("Both user 14 and 19 starred and were written in language 1: ", response.result.row.columns)