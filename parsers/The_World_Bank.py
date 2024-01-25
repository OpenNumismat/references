# -*- coding: utf-8 -*-

import csv
import json


def alpha2countrydata(alpha, orig_data):
    for region in orig_data["regions"]:
        for country in region["countries"]:
            if "alpha3" in country and country["alpha3"] == alpha:
                return country
    return None


subregions_order = [
'Europe & Central Asia',
'Middle East & North Africa',
'North America',
'Latin America & Caribbean',
'South Asia',
'Sub-Saharan Africa',
'East Asia & Pacific',
]

subregions_data = {}
with open('../src/World_Bank.csv', encoding='utf-8') as subregions_file:
    spamreader = csv.reader(subregions_file, delimiter='\t')
    next(spamreader, None)
    for row in spamreader:
        subregions_data[row[1]] = row[2]


with open('../data/countries.json', encoding='utf-8') as orig_file:
    orig_data = json.load(orig_file)

result = {
    "regions": []
}

for region in subregions_order:
    result["regions"].append({
        "name": region,
        "countries": [],
    })

for alpha3, region in subregions_data.items():
    for r in result["regions"]:
        if r["name"] == region:
            orig_country_data = alpha2countrydata(alpha3, orig_data)
            if orig_country_data:
                r["countries"].append(orig_country_data)
            else:
                print("Missed data for", alpha3)

with open('../data/Regions (World Bank).json', 'w', encoding='utf8') as json_file:
    json.dump(result, json_file, ensure_ascii=False, indent=2)
