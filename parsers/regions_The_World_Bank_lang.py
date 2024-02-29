import csv
import json

from common import *


def alpha2countrydata(alpha, orig_data):
    for country in orig_data["countries"]:
        if "alpha3" in country and country["alpha3"] == alpha:
            return country
    return None


TITLE = "regions_The_World_Bank"

subregions_data = {}
with open('../src/CLASS.csv', encoding='utf-8') as file:
    reader = csv.reader(file, delimiter='\t')
    next(reader, None)
    for row in reader:
        subregions_data[row[1]] = row[2]


for lang in lang_list():
    with open(f"../data/country_currency_{lang}.json", encoding='utf-8') as orig_file:
        orig_data = json.load(orig_file)

    result = get_regions(TITLE, lang)

    for alpha3, region in subregions_data.items():
        for r in result["regions"]:
            if r["name"] == region2region_name(region):
                orig_country_data = alpha2countrydata(alpha3, orig_data)
                if orig_country_data:
                    r["countries"].append(orig_country_data)
                else:
                    print(f"Missed {lang} data for {alpha3}")

    with open(f"../data/{TITLE}_{lang}.json", 'w', encoding='utf8') as json_file:
        json.dump(result, json_file, ensure_ascii=False, indent=2)
