import json
import glob
from datetime import datetime
from bs4 import BeautifulSoup
import csv

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


def create_csv():
    """fields are name, teaser, date"""
    out = []

    # scraped news
    for f in glob.glob("news/*.json"):
        with open(f, "r") as infile:
            news = json.load(infile)
        for n in news:
            item = (
                datetime.fromisoformat(n["date"]),
                n["name"],
                n["teaser"],
            )
            # if item["snippet"] and "After 6 years of drilling in the Sleipner West natural gas field in the Norwegian North Sea" in item["snippet"]:
            # print(item)
            # if item not in out:
            out.append(item)

    # archived news
    for f in glob.glob("./oil_news_old/*.html"):
        with open(f, "r") as infile:
            html = infile.read()
        soup = BeautifulSoup(html, "html.parser")
        date_info = soup.select(".search_term")[1].text.strip()
        date_info = date_info.replace("Publication Date: ", "").replace("-", "").strip()
        date = datetime.strptime(date_info, "%b %d, %Y")
        items = soup.select("li.result")
        for i in items:
            title = i.select_one("a.title").text.strip()
            snippet = i.select_one("p.snippet").text.replace(title, "").strip()
            item = (date, title, snippet)
            # if item not in out:
            out.append(item)

    out = list(set(out))
    out = sorted(out, key=lambda k: k[0])

    with open("news.csv", "w") as outfile:
        fieldnames = ["date", "title", "snippet"]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)

        writer.writeheader()
        for date, title, snippet in out:
            item = {
                "date": date.strftime("%Y-%m-%d"),
                "title": title,
                "snippet": snippet,
            }
            writer.writerow(item)


create_csv()

# print_titles()
# print_teasers()
