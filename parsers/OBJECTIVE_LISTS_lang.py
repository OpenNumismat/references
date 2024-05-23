# -*- coding: utf-8 -*-

import json

from common import *


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


TITLE = "Regions (OBJECTIVE LISTS)"

with open('../src/OBJECTIVE_LISTS.json', encoding='utf-8') as subregions_file:
    subregions_data = json.load(subregions_file)

with open('../data/countries_alternative_names.json', encoding='utf-8') as file:
    alternative_names = json.load(file)


with open("../data/country_currency.json", encoding='utf-8') as file:
    orig_data = json.load(file)
countries_list = {}
for region_data in subregions_data:
    region = region_data['region']
    for name in region_data['countries']:
        for orig_country in orig_data["countries"]:
            if compare_county_names(name, orig_country["name"]):
                countries_list[orig_country["alpha3"]] = region
                break


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
