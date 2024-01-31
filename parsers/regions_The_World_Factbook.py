# -*- coding: utf-8 -*-

import csv
import json

def str2latin(string):
    return string.replace('ô', 'o').replace('ó', 'o').replace('ç', 'c').replace('é', 'e').replace('ë', 'e').replace('ā', 'a').replace('ã', 'a').replace('í', 'i').replace('ê', 'e').replace('ş', 's').replace('Đ', 'D').replace('ồ', 'o').replace('à', 'a')

def get_alternative_names(country):
    country = country.lower()
    for names in alternative_names.values():
        names = [name.lower() for name in names]
        for name in names:
            if name == country:
                return names
    return [country,]

def compare_county_names(country1, country2):
    return bool(country2.lower() in get_alternative_names(country1))

def country2countrydata(country, orig_data):
    names = get_alternative_names(country)
    for orig_country in orig_data["countries"]:
        key = orig_country["name"].lower()
        for name in names:
            if name == key:
                return orig_country
    return None


subregions_data = {}
with open('../src/Area.csv', encoding='utf-8') as subregions_file:
    spamreader = csv.reader(subregions_file)
    next(spamreader, None)
    for row in spamreader:
        subregions_data[row[0]] = row[5]

with open('../data/countries_alternative_names.json', encoding='utf-8') as file:
    alternative_names = json.load(file)

with open('../data/country_currency.json', encoding='utf-8') as orig_file:
    orig_data = json.load(orig_file)

result = {
    "regions": [
        {"name": "Europe", "countries": []},
        {"name": "North America", "countries": []},
        {"name": "Middle East", "countries": []},
        {"name": "Central Asia", "countries": []},
        {"name": "East and Southeast Asia", "countries": []},
        {"name": "South America", "countries": []},
        {"name": "Australia and Oceania", "countries": []},
        {"name": "South Asia", "countries": []},
        {"name": "Africa", "countries": []},
        {"name": "Central America and the Caribbean", "countries": []},
#        {"name": "Antarctica", "countries": []},
    ]
}

for orig_country in orig_data["countries"]:
    finded = False
    for country, region in subregions_data.items():
        if compare_county_names(country, orig_country["name"]):
            for r in result["regions"]:
                if r["name"] == region:
                    r["countries"].append(orig_country)
                    finded = True
                    break
            break

    if not finded and "unrecognized" in orig_country:
        for r in result["regions"]:
            for c in r["countries"]:
                if c["alpha3"] == orig_country["part_of"]:
                    r["countries"].append(orig_country)
                    finded = True
                    break

    if not finded:
        print("Missed data for", orig_country["name"])

with open('../data/regions_World_Factbook.json', 'w', encoding='utf8') as json_file:
    json.dump(result, json_file, ensure_ascii=False, indent=2)
