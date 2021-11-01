import re
import requests
from bs4 import BeautifulSoup


def string_escape(s, encoding="utf-8"):
    return s.encode("latin1").decode("unicode-escape").encode("latin1").decode(encoding)


cookies = {
    "BID": "164635ef6a5ec8960683d0c2d769150a",
    "activity": "%7B%22last_hit_at%22%3A1635277481%2C%22last_visit_at%22%3A1633319369%7D",
    "last_search_rails": "%7B%22keywords%22%3A%22%22%2C%22location%22%3A%22Iraq%22%2C%22pay%22%3A%22%22%2C%22emp%22%3A%22%22%2C%22languages%22%3A%22%22%7D",
    "visited_before": "true",
    "session_rails": "8bcde6e908c6b1920d978081f486cd05",
    "chatbot_default_display": "displayed",
}

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:93.0) Gecko/20100101 Firefox/93.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "https://www.oilandgasjobsearch.com/jobs?keywords=&location=Iraq&page_number=3",
    "X-CSRF-Token": "zhL9C4mbtNeqA7Dit4Js6DSfVvjQfDVZE0CtIKekpPNlOnSQrg6/n825I1Aki5OBTRUNfinzdVd9Bjk92NTOfQ==",
    "X-Requested-With": "XMLHttpRequest",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "TE": "trailers",
}


def get_page(p, country):
    params = (
        ("keywords", ""),
        ("location", country),
        ("page_number", p),
    )

    response = requests.get(
        "https://www.oilandgasjobsearch.com/jobs.js",
        headers=headers,
        params=params,
        cookies=cookies,
    )

    content = response.text
    html = re.search(r"\.append\(\"(.*)\"\)", content).group(1)
    html = string_escape(html).replace("\\/", "/")
    soup = BeautifulSoup(html, features='lxml')
    jobs = soup.select(".data-results-content-parent")
    for job in jobs:
        title = job.select_one(".data-results-title").text.strip()
        details = job.select(".data-details span")
        company = details[0].text.strip()
        location = details[1].text.strip() + ", " + country
        # url = job.select_one("a").get("href")
        date = job.select_one(".data-results-publish-time").text

        item = {
            "title": title,
            "company": company,
            "location": location,
            "date": date,
        }

        print(item)
    # print(soup)


get_page(600, "USA")


# NB. Original query string below. It seems impossible to parse and
# reproduce query strings 100% accurately so the one below is given
# in case the reproduced version is not "correct".
# response = requests.get('https://www.oilandgasjobsearch.com/jobs.js?keywords=&location=Iraq&page_number=4', headers=headers, cookies=cookies)
