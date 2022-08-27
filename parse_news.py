import json
import glob
import re
from datetime import datetime
from bs4 import BeautifulSoup
import html
from nltk.tokenize import sent_tokenize
import csv

files = glob.glob("news/*.json")

replacements = [
    ["&#128;", "€"],
    ["&#130;", "‚"],
    ["&#131;", "ƒ"],
    ["&#132;", "„"],
    ["&#133;", "…"],
    ["&#134;", "†"],
    ["&#135;", "‡"],
    ["&#136;", "ˆ"],
    ["&#137;", "‰"],
    ["&#138;", "Š"],
    ["&#139;", "‹"],
    ["&#140;", "Œ"],
    ["&#142;", "Ž"],
    ["&#145;", "‘"],
    ["&#146;", "’"],
    ["&#147;", "“"],
    ["&#148;", "”"],
    ["&#149;", "•"],
    ["&#150;", "–"],
    ["&#151;", "—"],
    ["&#152;", "˜"],
    ["&#153;", "™"],
    ["&#154;", "š"],
    ["&#155;", "›"],
    ["&#156;", "œ"],
    ["&#158;", "ž"],
    ["&#159;", "Ÿ"],
    ["&#160;", " "],
    ["&#161;", "¡"],
    ["&#162;", "¢"],
    ["&#163;", "£"],
    ["&#164;", "¤"],
    ["&#165;", "¥"],
    ["&#166;", "¦"],
    ["&#167;", "§"],
    ["&#168;", "¨"],
    ["&#169;", "©"],
    ["&#170;", "ª"],
    ["&#171;", "«"],
    ["&#172;", "¬"],
    ["&#174;", "®"],
    ["&#175;", "¯"],
    ["&#176;", "°"],
    ["&#177;", "±"],
    ["&#178;", "²"],
    ["&#179;", "³"],
    ["&#180;", "´"],
    ["&#181;", "µ"],
    ["&#182;", "¶"],
    ["&#183;", "·"],
    ["&#184;", "¸"],
    ["&#185;", "¹"],
    ["&#186;", "º"],
    ["&#187;", "»"],
    ["&#188;", "¼"],
    ["&#189;", "½"],
    ["&#190;", "¾"],
    ["&#191;", "¿"],
    ["&#192;", "À"],
    ["&#193;", "Á"],
    ["&#194;", "Â"],
    ["&#195;", "Ã"],
    ["&#196;", "Ä"],
    ["&#197;", "Å"],
    ["&#198;", "Æ"],
    ["&#199;", "Ç"],
    ["&#200;", "È"],
    ["&#201;", "É"],
    ["&#202;", "Ê"],
    ["&#203;", "Ë"],
    ["&#204;", "Ì"],
    ["&#205;", "Í"],
    ["&#206;", "Î"],
    ["&#207;", "Ï"],
    ["&#208;", "Ð"],
    ["&#209;", "Ñ"],
    ["&#210;", "Ò"],
    ["&#211;", "Ó"],
    ["&#212;", "Ô"],
    ["&#213;", "Õ"],
    ["&#214;", "Ö"],
    ["&#215;", "×"],
    ["&#216;", "Ø"],
    ["&#217;", "Ù"],
    ["&#218;", "Ú"],
    ["&#219;", "Û"],
    ["&#220;", "Ü"],
    ["&#221;", "Ý"],
    ["&#222;", "Þ"],
    ["&#223;", "ß"],
    ["&#224;", "à"],
    ["&#225;", "á"],
    ["&#226;", "â"],
    ["&#227;", "ã"],
    ["&#228;", "ä"],
    ["&#229;", "å"],
    ["&#230;", "æ"],
    ["&#231;", "ç"],
    ["&#232;", "è"],
    ["&#233;", "é"],
    ["&#234;", "ê"],
    ["&#235;", "ë"],
    ["&#236;", "ì"],
    ["&#237;", "í"],
    ["&#238;", "î"],
    ["&#239;", "ï"],
    ["&#240;", "ð"],
    ["&#241;", "ñ"],
    ["&#242;", "ò"],
    ["&#243;", "ó"],
    ["&#244;", "ô"],
    ["&#245;", "õ"],
    ["&#246;", "ö"],
    ["&#247;", "÷"],
    ["&#248;", "ø"],
    ["&#249;", "ù"],
    ["&#250;", "ú"],
    ["&#251;", "û"],
    ["&#252;", "ü"],
    ["&#253;", "ý"],
    ["&#39;", "'"],
    ["&#34", '"'],
]


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

    seen = set()

    # scraped news
    for f in glob.glob("news/*.json"):
        with open(f, "r", encoding="utf-8") as infile:
            news = json.load(infile)
        for n in news:
            if n["teaser"] is None:
                continue
            if (n["name"], n["teaser"]) in seen:
                continue
            seen.add((n["name"], n["teaser"]))

            teaser = n["teaser"]

            for s, r in replacements:
                teaser = teaser.replace(s, r)
                teaser = teaser.replace(s.replace(";", ""), r)
            # teaser = teaser.replace("&#39;", "'").replace("&34;", '"').replace("&#151;", "-")

            teaser = teaser.replace("‘", "'").replace("’", "'")

            if "�" in teaser:
                teaser = re.sub("\.$", " [sic].", teaser)

            item = (
                datetime.fromisoformat(n["date"]),
                n["name"].replace("&#39;", "'").replace("‘", "'").replace("’", "'"),
                teaser
            )
            # if item["snippet"] and "After 6 years of drilling in the Sleipner West natural gas field in the Norwegian North Sea" in item["snippet"]:
            # print(item)
            # if item not in out:
            out.append(item)

    # archived news
    for f in glob.glob("./oil_news_old/*.html"):
        with open(f, "r", encoding="utf-8") as infile:
            html_content = infile.read()
        soup = BeautifulSoup(html_content, "html.parser")
        date_info = soup.select(".search_term")[1].text.strip()
        date_info = date_info.replace("Publication Date: ", "").replace("-", "").strip()
        date = datetime.strptime(date_info, "%b %d, %Y")
        items = soup.select("li.result")
        for i in items:
            title = i.select_one("a.title").text.strip()
            title = title.replace("&#39;", "'").replace("‘", "'").replace("’", "'")
            snippet = i.select_one("p.snippet").text.replace(title, "").strip()
            if snippet == "":
                continue
            snippet = snippet.replace("&#39;", "'").replace("‘", "'").replace("’", "'")
            # snippet = snippet.replace("...", ".")
            snippet_sentences = sent_tokenize(snippet)
            if len(snippet_sentences) > 1:
                snippet = snippet_sentences[0]
            else:
                # snippet += "FIXME_FIXME"
                snippet = snippet.replace("...", "[...]")

            if (title, snippet) in seen:
                continue

            seen.add((title, snippet))

            item = (date, title, snippet)
            # if item not in out:
            out.append(item)

    out = list(set(out))
    out = sorted(out, key=lambda k: k[0])
    min_date = datetime(1989, 3, 24)
    max_date = datetime(2020, 3, 24)

    with open("news.csv", "w", encoding="utf8") as outfile:
        fieldnames = ["date", "snippet"]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)

        writer.writeheader()
        for date, _title, snippet in out:
            if date < min_date or date > max_date:
                continue
            item = {
                "date": date.strftime("%Y-%m-%d"),
                # "title": title,
                "snippet": snippet,
            }
            writer.writerow(item)
            # print(f"{date}\t{snippet}")


create_csv()

# print_titles()
# print_teasers()
