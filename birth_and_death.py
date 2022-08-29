from dateutil import parser
import pandas as pd
import numpy as np

# date_template = "%A %B %-d %Y"
date_template = "%A %B {S} %Y"


def suffix(d):
    return "th" if 11 <= d <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(d % 10, "th")

def custom_strftime(format, t):
    return t.strftime(format).replace('{S}', str(t.day) + suffix(t.day))


def parse_wells():
    df = pd.read_csv("deadwells.csv")
    df.sort_values(by=["CompletionDate"], inplace=True, ascending=True)
    for _, row in df.iterrows():
        # try:
        #     first_prod = parser.parse(row["FirstProdDate"])
        # except Exception as e:
        #     continue

        try:
            completion = parser.parse(row["CompletionDate"])
        except Exception as e:
            continue

        try:
            plug = parser.parse(row["PlugDate"])
        except Exception as e:
            continue

        # valid = completion < first_prod and first_prod < plug
        valid = completion < plug

        if not valid:
            continue

        # first_prod = first_prod.strftime(date_template)
        # plug = plug.strftime(date_template)
        # completion = completion.strftime(date_template)
        plug = custom_strftime(date_template, plug)
        completion = custom_strftime(date_template, completion)

        name = row["Name"]
        county = row["County"]
        state = row["State"]
        operator = row["OperatorReported"]
        location = county + ", " + state
        total_oil = row["CumulativeOilProduction"]
        total_gas = row["CumulativeGasProduction"]

        if np.isnan(total_oil):
            total_oil = 0

        if np.isnan(total_gas):
            total_gas = 0

        birth = f"{name} was completed by {operator} in {location} on {completion}, "

        # if first_prod:
        #     drilling = f"began drilling on {first_prod}, "
        # else:
        #     drilling = ""
        drilling = ""

        death = f"and was plugged and abandoned on {plug}."
        totals = f" It produced {total_oil:,.0f} barrels of oil."

        print(birth + drilling + death + totals)

    # items = []
    # with open("./deadwells.csv", "r") as infile:
    #     reader = csv.DictReader(infile)
    #
    #     for row in reader:
    #         if "FirstProdDate" not in row or row["FirstProdDate"] == "":
    #             first_prod = None
    #         else:
    #             first_prod = parser.parse(row["FirstProdDate"])
    #
    #         if "CompletionDate" not in row or row["CompletionDate"] == "":
    #             completion = None
    #         else:
    #             completion = parser.parse(row["CompletionDate"])
    #
    #         if "PlugDate" not in row or row["PlugDate"] == "":
    #             plug = None
    #         else:
    #             plug = parser.parse(row["PlugDate"])
    #
    #         name = row["Name"]
    #         county = row["County"]
    #         state = row["State"]
    #         operator = row["OperatorReported"]
    #         location = county + ", " + state
    #
    #         items.append((name, location, operator, completion, first_prod, plug))
    #
    #
    # items = sorted(items, key=lambda k: k[3])
    # for name, location, operator, completion, first_prod, plug in items:
    #     print(
    #         f"{name} was created by {operator} in {location} on {completion}, began drilling on {first_prod}, and was plugged and abandoned on {plug}"
    #     )


parse_wells()
