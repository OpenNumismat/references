# -*- coding: utf-8 -*-

import csv
import json

def str2latin(string):
    return string.replace('ô', 'o').replace('ó', 'o').replace('ç', 'c').replace('é', 'e').replace('ë', 'e').replace('ā', 'a').replace('ã', 'a').replace('í', 'i').replace('ê', 'e').replace('ş', 's').replace('Đ', 'D').replace('ồ', 'o').replace('à', 'a')

def country2countrydata(country, orig_data):
    for orig_country in orig_data["countries"]:
        if str2latin(orig_country["name"]) == country:
            return orig_country
    return None


subregions_order = [
'Central Asia',
#'Antarctica',
'North America',
'East and Southeast Asia',
'South America',
'Australia and Oceania',
'South Asia',
'Africa',
'Middle East',
'Europe',
'Central America and the Caribbean',
]

subregions_data = {}
with open('../src/The_World_Factbook.csv', encoding='utf-8') as subregions_file:
    spamreader = csv.reader(subregions_file)
    next(spamreader, None)
    for row in spamreader:
        subregions_data[row[0]] = row[5]

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

for country, region in subregions_data.items():
    for r in result["regions"]:
        if r["name"] == region:
            orig_country_data = country2countrydata(country, orig_data)
            if orig_country_data:
                r["countries"].append(orig_country_data)
            else:
                print("Missed data for", country)

with open('../data/Regions (World Factbook).json', 'w', encoding='utf8') as json_file:
    json.dump(result, json_file, ensure_ascii=False, indent=2)
