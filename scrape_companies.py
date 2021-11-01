import concurrent.futures
import json
import glob
import requests
import time
import re
from bs4 import BeautifulSoup

MAX_THREADS = 30


def get_urls(start):

    response = requests.get(start)

    soup = BeautifulSoup(response.text)
    urls = [a.get("href") for a in soup.select(".h-company-block a")]
    urls = list(set(urls))
    return urls


def download_url(url):

    local_name = "companies_html/" + re.sub(r"\W", "_", url) + ".html"
    print(local_name)

    resp = requests.get(url)
    with open(local_name, "wb") as fh:
        fh.write(resp.content)

    time.sleep(0.25)


def download_listings(story_urls):
    threads = min(MAX_THREADS, len(story_urls))

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(download_url, story_urls)


def scrape():
    start = "https://www.offshore-technology.com/company-a-z/"
    urls = get_urls(start)
    download_listings(urls)


def parse():
    out = []
    for f in glob.glob("companies_html/*.html"):
        with open(f, "r") as infile:
            text = infile.read()
        soup = BeautifulSoup(text, features="lxml")

        name = soup.select_one(".c-company-header__title").text.strip()

        try:
            subheads = soup.select(".c-company-header__standfirst")
            subhead1 = subheads[0].text.strip()
            full_subhead = "\n".join([s.text.strip() for s in subheads])
        except Exception as e:
            subhead1 = ""
            full_subhead = ""

        intro = soup.select_one(".c-post-typography").text.strip()

        images = soup.select(".c-post-figure__image-container a")
        images = [i.get("href") for i in images]

        links = soup.select(".c-links-list__link")
        links = [l.get("href") for l in links]

        for el in soup.select("aside"):
            el.decompose()

        fulltext = soup.select(".c-post-typography")
        fulltext = "\n\n".join([s.text.strip() for s in fulltext])

        item = {
            "name": name,
            "subhead1": subhead1,
            "fullsubhead": full_subhead,
            "intro": intro,
            "images": images,
            "links": links,
            "fulltext": fulltext,
        }

        out.append(item)

    with open("contractors.json", "w") as outfile:
        json.dump(out, outfile, indent=2)


if __name__ == "__main__":
    parse()
