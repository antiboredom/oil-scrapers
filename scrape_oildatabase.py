import requests
import csv
import time
import json

cookies = {
    "__apex_test__": "",
    "__stripe_mid": "a2bffe00-0664-46d7-8c6d-b0f684dfc44212f4eb",
    ".AspNetCore.Antiforgery.ZBV4UtDBfxE": "CfDJ8JZChd3PgR1OiY6uSEMH50oANli1c5WzSr_P7_KqIkY3BN7k7MFvITseYbnMi3Xi5d-YOI9I_DzIt1QVh9PB8HLmKK85uXgpeRD8TJ-NSWOl1IhgER24_ByXEi8KNcWAPWhtZmIRb-9zVe5WjPts0qk",
    "_upscope__region": "InVzLWVhc3Qi",
    "_upscope__shortId": "IlpDR1hBQUxBUzQwRVFIS1BIIg==",
    "wdb.App.v2": "CfDJ8JZChd3PgR1OiY6uSEMH50opzq40hfbvEfuN7T3DFZ-TGRdwkPRcIcU4if0cMYWW29g4gLaunEIOBORjlqHeAyR622zIpf2CNI0HgH4dL64rhuBrAn7YLbleMv4t1GM6IQtWyE1UqdD4Lw0gm-tlP1ukT6De3zENnBvp84Atu6Tx22eRblxYwNf_aW_bczi-WF1VXvvm31KBzDBgpGU47ssgivQi_y1QzxHZRs9w1BpmPS6C_qGBvPOSWzd51XTYZpjafiCAuL1IQOQqaBdejo88WSN9EL7H2vY5oLCMOMpHGekurZXG1sKZMPzbDPxumKTcpt93jV3AcSyqZbfeu_k",
    "_upscope__waitingForCallAt": "",
    "WDBUT.v2": "Q2ZESjhKWkNoZDNQZ1IxT2lZNnVTRU1INTBxQkRKenlhdUF4VkFVdVZ6OFRUNHFWSEd5dlViQ1diS01YVFdmWjZ5RTZDMU8xTWU3Q1ptMDNQY19wZU9GV3lvS1pheHVfWDhTOWNFUWF3dkhxM1ZTbU5CeHpxZEM1N2RHUmR0TzJmX1NpX0lJTjZDYXJNUTJTbkt1NGVDT2lYcnhUOUFVNHZZRzJLal9lQU1oR0lSaTRfVkZBeFFXT3VYVEE5TTBLVndFYllPUERSOUdoLVpMdEZuZW5janF4TldZakJkOTVvby1kZ1BDbXIzcmlNdUpSb08xQS16OW4zcEc4MG9USmlaNWpDOFpqcUxNdl8wdjJLOU1wQVBQd20xbw%3D%3D",
}

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:92.0) Gecko/20100101 Firefox/92.0",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "https://app.welldatabase.com/browse/Wells",
    "Content-Type": "application/json; charset=utf-8",
    "RequestVerificationToken": "CfDJ8JZChd3PgR1OiY6uSEMH50o4-OG2PFxElXsl7gavYOuMr7KO7VDIwr9aEKRr-hcZWEwPOj1lZCbOcF5uTaVu9Fb0BONV5VZyKGlwETOErr2W-4APhJ4zuwAMgikpe6itn9v92AckTl37meS-yoaPJSCA4Hp8qWE9miupAf7x3n4rbDqyjiu20EHc8lDsY595Jw",
    "X-Requested-With": "XMLHttpRequest",
    "traceparent": "00-12fa2e8199a6d7f006e55ba831023f0e-25b4f9fb21e0cb3c-01",
    "Origin": "https://app.welldatabase.com",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "TE": "trailers",
}


def get_dead_wells(page=1, per_page=100, min_oil=100000, last_produced=1):
    skip = (page - 1) * per_page

    params = {
        "wellFilters": {
            "aoi": "Map",
            "northeastLatitude": 80.4303299657727,
            "northeastLongitude": -29.443359250000007,
            "southwestLatitude": -17.392579663677353,
            "southwestLongitude": -231.94335925000001,
            "zoom": 3,
            "source": "00000000-0000-0000-0000-000000000000",
            "aliasedStatuses": {"included": [2942]},
        },
        "dataType": "Well",
        "take": per_page,
        "skip": skip,
        "page": page,
        "pageSize": per_page,
        "group": [],
    }

    response = requests.post(
        "https://app.welldatabase.com/browse/wells/list",
        headers=headers,
        cookies=cookies,
        data=json.dumps(params),
    )

    results = response.json()
    return results


def get_wells(page=1, per_page=100, min_oil=100000, last_produced=1):
    skip = (page - 1) * per_page

    params = {
        "wellFilters": {
            "aoi": "Map",
            "isStoredSearch": True,
            "northeastLatitude": 80.4303299657727,
            "northeastLongitude": -29.443359250000007,
            "southwestLatitude": -17.392579663677353,
            "southwestLongitude": -231.94335925000001,
            "zoom": 3,
            "cumOil": {"min": str(min_oil)},
            "source": "00000000-0000-0000-0000-000000000000",
            "lastXProduction": {"oil": {"range": {"min": str(last_produced)}}},
        },
        "dataType": "Well",
        "take": per_page,
        "skip": skip,
        "page": page,
        "pageSize": per_page,
        "group": [],
    }

    response = requests.post(
        "https://app.welldatabase.com/browse/wells/list",
        headers=headers,
        cookies=cookies,
        data=json.dumps(params),
    )

    results = response.json()
    return results


def clean_listing(data):
    out = dict(data)
    del out["child"]
    for k, v in data["child"].items():
        out[k] = v
    return out


def get_all():
    results = get_dead_wells()
    data = [clean_listing(i) for i in results["data"]]

    per_page = 100
    total = results["total"]
    total_pages = int(total / per_page)

    print(total_pages)
    data = []
    for p in range(6679, total_pages):
        print(p, total_pages)
        try:
            _data = get_dead_wells(page=p)
            data += [clean_listing(i) for i in _data["data"]]
            time.sleep(0.2)

            with open("deadwells6.json", "w") as outfile:
                json.dump(data, outfile)
        except Exception as e:
            print(e)


def merge():
    with open("big_active_wells.json", "r") as infile:
        data = json.load(infile)
    with open("big_active_wells2.json", "r") as infile:
        data2 = json.load(infile)

    data += data2

    data_file = open("bigwells.csv", "w")
    csv_writer = csv.writer(data_file)

    count = 0
    for d in data:
        if count == 0:
            header = d.keys()
            csv_writer.writerow(header)
            count += 1
        csv_writer.writerow(d.values())

    data_file.close()

    # with open("merged_wells.json", "w") as outfile:
    #     json.dump(data, outfile)


if __name__ == "__main__":
    get_all()
    # merge()
