import concurrent.futures
import requests
import time
from bs4 import BeautifulSoup

MAX_THREADS = 30


def get_urls(start):
    data = {"measure": "2", "step": "all", "go": "Go"}

    response = requests.post(
        start,
        # headers=headers,
        data=data,
    )

    soup = BeautifulSoup(response.text)
    urls = [a.get("href").replace("?measure=2", "") for a in soup.select("#ship_results td a")]
    urls = list(set(urls))
    return urls


def download_url(url):
    local_name = (
        "horizon_html/"
        + url.replace("https://horizonship.com/", "")
        .replace("/", "_")
        .replace("?measure=2", "")
        + ".html"
    )
    print(local_name)

    resp = requests.get(url)
    with open(local_name, "wb") as fh:
        fh.write(resp.content)

    time.sleep(0.25)


def download_listings(story_urls):
    threads = min(MAX_THREADS, len(story_urls))

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(download_url, story_urls)


def main():
    # start = "https://horizonship.com/ship-category/offshore-supply-vessels-for-sale/"
    start = "https://horizonship.com/ship-category/tankers-for-sale/crude-oil-tankers-for-sale/"
    urls = get_urls(start)
    download_listings(urls)


if __name__ == "__main__":
    main()
