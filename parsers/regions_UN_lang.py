import csv
import json

from common import *


def country2countrydata(country, orig_data):
    names = get_alternative_names(country)
    for orig_country in orig_data["countries"]:
        key = orig_country["name"].lower()
        for name in names:
            if name.lower() == key:
                return orig_country
    return None



TITLE = "regions_UN"

countries_list = {}
with open('../src/UNSD — Methodology.csv', encoding='utf-8') as file:
    reader = csv.reader(file, delimiter=';')
    next(reader, None)
    for row in reader:
        countries_list[row[11]] = row[3]

with open(f"../data/country_currency.json", encoding='utf-8') as orig_file:
    orig_data = json.load(orig_file)

for lang in lang_list():
    result = get_regions(TITLE, lang)
    translated_country_names = get_translated_country_names(lang)
    translated_currency_names = get_translated_currency_names(lang)

    for orig_country in orig_data["countries"]:
        finded = False
        for alpha3, region in countries_list.items():
            if alpha3 == orig_country["alpha3"]:
                for r in result["regions"]:
                    if r["name"] == region2region_name(region):
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
                        finded = True
                        break
                break

        if not finded and ("unrecognized" in orig_country or "disappeared" in orig_country):
            for r in result["regions"]:
                for c in r["countries"]:
                    if c["alpha3"] == orig_country["part_of"]:
                        translated_country = orig_country.copy()
                        translated_country["name"] = translated_country_names[orig_country["name"]]

                        units = []
                        for unit in orig_country["units"]:
                            units.append(translated_currency_names[unit])
                        translated_country["units"] = units

                        r["countries"].append(translated_country)
                        finded = True
                        break

        if not finded:
            print(f"Missed {lang} data for {orig_country['name']}")

    with open(f"../data/{TITLE}_{lang}.json", 'w', encoding='utf8') as json_file:
        json.dump(result, json_file, ensure_ascii=False, indent=2)
