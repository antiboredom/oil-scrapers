import json
import glob
from datetime import datetime

files = glob.glob("news/*.json")

def get():
    everything = []
    for f in files:
        with open(f, "r") as infile:
            everything += json.load(infile)

    everything = sorted(everything, key=lambda k: datetime.fromisoformat(k["date"]))
    return everything

def print_news():
    everything = get()
    for e in everything:
        date = datetime.fromisoformat(e["date"]).strftime("%Y-%m-%d")
        if not date or not e["teaser"]:
            continue
        print(date + ": " + e["teaser"])

def images():
    everything = get()
    everything = [e for e in everything if e["img"]]
    for e in everything:
        print('<img src="{}">'.format(e['img']['src']))

images()

