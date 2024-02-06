# -*- coding: utf-8 -*-

import csv
import json


def alpha2countrydata(alpha, orig_data):
    for country in orig_data["countries"]:
        if "alpha3" in country and country["alpha3"] == alpha:
            return country
    return None


subregions_data = {}
with open('../src/CLASS.csv', encoding='utf-8') as file:
    reader = csv.reader(file, delimiter='\t')
    next(reader, None)
    for row in reader:
        subregions_data[row[1]] = row[2]


for lang in ('en', 'bg', 'es', 'cs', 'de', 'el', 'fr', 'it', 'lv', 'hu', 'nl', 'pl', 'pt', 'sv'):
    with open(f"../data/country_currency_{lang}.json", encoding='utf-8') as orig_file:
        orig_data = json.load(orig_file)

    result = {
        "regions": [
            {"name": "Europe & Central Asia", "countries": []},
            {"name": "North America", "countries": []},
            {"name": "Middle East & North Africa", "countries": []},
            {"name": "Latin America & Caribbean", "countries": []},
            {"name": "South Asia", "countries": []},
            {"name": "Sub-Saharan Africa", "countries": []},
            {"name": "East Asia & Pacific", "countries": []},
        ]
    }

    for alpha3, region in subregions_data.items():
        for r in result["regions"]:
            if r["name"] == region:
                orig_country_data = alpha2countrydata(alpha3, orig_data)
                if orig_country_data:
                    r["countries"].append(orig_country_data)
                else:
                    print("Missed data for", alpha3)

    with open(f"../data/regions_WorldBank_{lang}.json", 'w', encoding='utf8') as json_file:
        json.dump(result, json_file, ensure_ascii=False, indent=2)
