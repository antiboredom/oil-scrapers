from bs4 import BeautifulSoup
from html import unescape
from pprint import pprint
import json
from glob import glob


def parse_page(html):
    soup = BeautifulSoup(html, features="lxml")

    meta = soup.select_one(".yoast-schema-graph--main")
    meta_data = json.loads(meta.text)["@graph"][1]

    date = meta_data.get("datePublished")
    description = meta_data.get("description")
    name = meta_data.get("name")
    name = name.replace(" - Horizon Ship Brokers, Inc.", "").strip()
    name = unescape(name)
    url = meta_data.get("url")
    img = soup.select_one(".fancybox")
    if img:
        img = img.get("href")

    table = soup.select_one(".ship_table")

    return {"name": name, "date": date, "img": img}


out = []
for f in glob("./horizon_html/*.html"):
    with open(f, "r") as infile:
        html = infile.read()
    item = parse_page(html)
    out.append(item)

with open("ships_for_sale.json", "w") as outfile:
    json.dump(out, outfile)
