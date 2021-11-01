import requests
import json
from datetime import datetime

with open("oil_journal.gql", "r") as infile:
    gql = infile.read()


sections = [
    (32509, "pipelines"),
    (32498, "refining"),
    (32492, "drilling"),
    (32488, "exploration"),
]

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:93.0) Gecko/20100101 Firefox/93.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "https://www.ogj.com/",
    "content-type": "application/json",
    "x-tenant-key": "ebm_ogj",
    "x-cdn-image-hostname": "base.imgix.net",
    "x-cdn-asset-hostname": "media.cygnus.com",
    "Origin": "https://www.ogj.com",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "TE": "trailers",
}


def get_page(section_id, limit=50, skip=0):
    out = []

    data = {
        "operationName": "getContentStream",
        "variables": {
            "limit": 1,
            "excludeContentIds": [],
            "sectionBubbling": True,
            "requirePrimaryImage": False,
            "scheduleOption": 2,
            "limit": limit,
            "skip": skip,
            "sectionId": section_id,
        },
        "query": gql,
    }

    data = json.dumps(data)

    response = requests.post(
        "https://aerilon.graphql.aspire-ebm.com/", headers=headers, data=data
    )

    results = response.json()["data"]["getContentStream"]["edges"]

    for result in results:
        r = result["node"]
        item = {
            "id": r["id"],
            "name": r["name"],
            "teaser": r["teaser"],
            "date": datetime.fromtimestamp(r["published"] / 1000).isoformat(),
            "url": r["siteContext"]["path"],
            "company": r["company"],
            "img": r.get("primaryImage"),
        }
        out.append(item)

    return out


def get_section(section_id, limit=10, max_results=2000):
    out = []
    for skip in range(0, max_results, limit):
        print(skip)
        try:
            results = get_page(section_id, limit=limit, skip=skip)
            out += results
        except Exception as e:
            print(e)
    return out


if __name__ == "__main__":
    # print(get_page(sections[0][0], 50, 20810))
    for section_id, section_name in sections:
        print(section_name)
        results = get_section(section_id, max_results=2000)
        with open("news/" + section_name + ".json", "w") as outfile:
            json.dump(results, outfile)
