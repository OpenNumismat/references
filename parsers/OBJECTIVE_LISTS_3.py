# -*- coding: utf-8 -*-

import json


def str2latin(string):
    return string.replace('ô', 'o').replace('ó', 'o').replace('ç', 'c').replace('é', 'e').replace('ë', 'e').replace('ā', 'a').replace('ã', 'a').replace('í', 'i').replace('ê', 'e').replace('ş', 's').replace('Đ', 'D').replace('ồ', 'o').replace('à', 'a')

def get_alternative_names(country):
    country = country.lower()
    for names in alternative_names.values():
        for name in names:
            if name.lower() == country:
                return names
    return [country,]

def country2countrydata(country, orig_data):
    names = get_alternative_names(country)
    for orig_country in orig_data["countries"]:
        key = orig_country["name"].lower()
        for name in names:
            if name.lower() == key:
                return orig_country
    return None


with open('../src/OBJECTIVE_LISTS_3.json', encoding='utf-8') as subregions_file:
    subregions_data = json.load(subregions_file)

with open('../data/countries_alternative_names.json', encoding='utf-8') as file:
    alternative_names = json.load(file)

with open('../data/country_currency.json', encoding='utf-8') as orig_file:
    orig_data = json.load(orig_file)



result = {
    "regions": []
}

for region in subregions_data:
    result["regions"].append({
        "name": region["region"],
        "countries": [],
    })

for region in subregions_data:
    region_name = region['region']
    for country in region['countries']:
        for r in result["regions"]:
            if r["name"] == region_name:
                orig_country_data = country2countrydata(country, orig_data)
                if orig_country_data:
                    r["countries"].append(orig_country_data)
                else:
                    print("Missed data for", country)

with open('../data/Macroregions (OBJECTIVE LISTS).json', 'w', encoding='utf8') as json_file:
    json.dump(result, json_file, ensure_ascii=False, indent=2)
