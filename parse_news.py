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


def unique(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


def print_news():
    everything = get()
    for e in everything:
        date = datetime.fromisoformat(e["date"]).strftime("%Y-%m-%d")
        if not date or not e["teaser"]:
            continue
        print(date + ": " + e["teaser"])


def print_titles():
    everything = get()
    titles = [e["name"] for e in everything]
    titles = unique(titles)
    for t in titles:
        print(t)


def print_teasers():
    everything = get()
    teasers = [e["teaser"] for e in everything if "teaser" in e]
    teasers = unique(teasers)
    for t in teasers:
        print(t)


def images():
    everything = get()
    everything = [e for e in everything if e["img"]]
    for e in everything:
        print('<img src="{}">'.format(e["img"]["src"]))


# print_titles()
print_teasers()
