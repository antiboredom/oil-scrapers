import json
from requests_html import HTMLSession

BASE = "https://www.rigzone.com/oil/jobs/search/"

session = HTMLSession()


def get_page(p=1):
    out = []
    r = session.get(BASE, params={"page": p})
    jobs = r.html.find("article.update-block")
    for j in jobs:
        title = j.find("h3 a", first=True)
        url = title.attrs.get("href")
        title = title.text
        employer_block = j.find("address", first=True).text.split("\n")
        employer = employer_block[0]
        location = employer_block[1]

        try:
            description = j.find(".description", first=True).text
        except Exception as e:
            description = ""

        try:
            responsibility = j.find(".responsibility", first=True).text
        except Exception as e:
            responsibility = ""

        try:
            experience = j.find(".experience", first=True).text
        except Exception as e:
            experience = ""

        try:
            time = j.find("time", first=True).text
        except Exception as e:
            time = ""

        item = {
            "title": title,
            "url": url,
            "employer": employer,
            "location": location,
            "responsibility": responsibility,
            "experience": experience,
            "time": time,
            "description": description,
        }
        out.append(item)
    return out


def get_all():
    jobs = []
    for p in range(1, 1000000):
        print(p)
        results = get_page(p)
        if len(results) == 0:
            break
        else:
            jobs += results

    with open("rigzone.json", "w") as outfile:
        json.dump(jobs, outfile)


get_all()
