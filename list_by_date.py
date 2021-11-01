import glob
import csv
import json
import re
from datetime import datetime
from dateutil import parser


YEAR = 2021

items = []


def parse_wells():
    out = []
    with open("./bigwells.csv", "r") as infile:
        reader = csv.DictReader(infile)

        for row in reader:
            if "FirstProdDate" not in row or row["FirstProdDate"] == "":
                continue
            date = parser.parse(row["FirstProdDate"])
            if date.year != YEAR:
                continue
            name = row["Name"]
            county = row["County"]
            state = row["State"]
            operator = row["OperatorReported"]
            out.append(
                {
                    "type": "well",
                    "name": name,
                    "operator": operator,
                    "location": county + ", " + state,
                    "date": date,
                }
            )
    return out


def parse_ships_for_sale():
    out = []
    with open("./ships_for_sale.json", "r") as infile:
        data = json.load(infile)

    for s in data:
        date = parser.parse(re.sub("T.*", "", s["date"]))
        if date.year != YEAR:
            continue

        out.append({"type": "sale", "date": date, "name": s["name"]})
    return out


def parse_rigzone():
    out = []

    with open("rigzone.json") as infile:
        data = json.load(infile)

    for job in data:
        date = parser.parse(job["time"].replace("Posted: ", ""))

        if date.year != YEAR:
            continue

        out.append(
            {
                "type": "job",
                "date": date,
                "title": job["title"],
                "employer": job["employer"],
                "location": job["location"],
            }
        )
    return out


def parse_news():
    out = []

    files = glob.glob("news/*.json")

    everything = []
    for f in files:
        with open(f, "r") as infile:
            everything += json.load(infile)

    for e in everything:
        date = parser.parse(e["date"])
        if date.year != YEAR:
            continue
        out.append({"type": "news", "date": date, "line": e["teaser"]})
    return out


# def make_json():
items = parse_news() + parse_rigzone() + parse_wells() + parse_ships_for_sale()
items = sorted(items, key=lambda k: k["date"])
for item in items:
    cat = item["type"]
    item["date"] = item["date"].strftime("%Y-%m-%d")
    if cat == "news":
        print("{date}: {line}".format(**item))
    elif cat == "job":
        print(
            "{date}: {employer} is looking for a {title} in {location}".format(**item)
        )
    elif cat == "well":
        print(
            "{date}: {operator} began drilling at {name} in {location}".format(**item)
        )
    elif cat == "sale":
        print(
            "{date}: {name} is offered for sale".format(**item)
        )


    # with open(str(YEAR) + '.json', "w") as outfile:
    #     json.dump(items, outfile)
