from bs4 import BeautifulSoup
from datetime import datetime
from glob import glob


def parse_old_stuff():
    out = []
    files = glob("./oil_news_old/*.html")
    for f in files:
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
            out.append({"name": title, "teaser": snippet, "date": date})
            # print(title)
            # print(snippet)
    out = sorted(out, key=lambda k: k["date"])
    return out

if __name__ == "__main__":
    results = parse_old_stuff()
    for r in results:
        date = r["date"].strftime("%Y-%m-%d")
        print(date, r['name'])
