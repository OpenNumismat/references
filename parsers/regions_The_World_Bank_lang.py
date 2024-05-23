import csv
import json

from common import *


def alpha2countrydata(alpha, orig_data):
    for country in orig_data["countries"]:
        if "alpha3" in country and country["alpha3"] == alpha:
            return country
    return None


TITLE = "regions_WorldBank"

subregions_data = {}
with open('../src/CLASS.csv', encoding='utf-8') as file:
    reader = csv.reader(file, delimiter='\t')
    next(reader, None)
    for row in reader:
        subregions_data[row[1]] = row[2]


with open(f"../data/country_currency.json", encoding='utf-8') as orig_file:
    orig_data = json.load(orig_file)

for lang in lang_list():
    result = get_regions(TITLE, lang)
    translated_country_names = get_translated_country_names(lang)
    translated_currency_names = get_translated_currency_names(lang)

    for alpha3, region in subregions_data.items():
        for r in result["regions"]:
            if r["name"] == region2region_name(region):
                orig_country = alpha2countrydata(alpha3, orig_data)
                if orig_country:
                    translated_country = orig_country.copy()
                    translated_country["name"] = translated_country_names[orig_country["name"]]

                    units = []
                    for unit in orig_country["units"]:
                        units.append(translated_currency_names[unit])
                    translated_country["units"] = units

                    if "contemporary_units" in orig_country:
                        units = []
                        for unit in orig_country["contemporary_units"]:
                            units.append(translated_currency_names[unit])
                        translated_country["contemporary_units"] = units

                    r["countries"].append(translated_country)
                else:
                    print(f"Missed {lang} data for {alpha3}")

    with open(f"../data/{TITLE}_{lang}.json", 'w', encoding='utf8') as json_file:
        json.dump(result, json_file, ensure_ascii=False, indent=2)
