import csv
import json


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
            if name.lower() == key:
                return orig_country
    return None
    

countries_list = {}
with open('../src/UNSD — Methodology.csv', encoding='utf-8') as file:
    reader = csv.reader(file, delimiter=';')
    next(reader, None)
    for row in reader:
        region = row[7]
        if not region:
            region = row[5]
        countries_list[row[8]] = region

with open('../data/countries_alternative_names.json', encoding='utf-8') as file:
    alternative_names = json.load(file)

with open('../data/country_currency.json', encoding='utf-8') as orig_file:
    orig_data = json.load(orig_file)

result = {
    "regions": [
        {"name": "Western Europe", "countries": []},
        {"name": "Northern Europe", "countries": []},
        {"name": "Southern Europe", "countries": []},
        {"name": "Eastern Europe", "countries": []},

        {"name": "Northern America", "countries": []},
        {"name": "Central America", "countries": []},
        {"name": "Caribbean", "countries": []},
        {"name": "South America", "countries": []},

        {"name": "Western Asia", "countries": []},
        {"name": "Central Asia", "countries": []},
        {"name": "Southern Asia", "countries": []},
        {"name": "Eastern Asia", "countries": []},
        {"name": "South-eastern Asia", "countries": []},

        {"name": "Northern Africa", "countries": []},
        {"name": "Western Africa", "countries": []},
        {"name": "Middle Africa", "countries": []},
        {"name": "Eastern Africa", "countries": []},
        {"name": "Southern Africa", "countries": []},

        {"name": "Australia and New Zealand", "countries": []},
        {"name": "Melanesia", "countries": []},
        {"name": "Micronesia", "countries": []},
        {"name": "Polynesia", "countries": []},
    ]
}

for orig_country in orig_data["countries"]:
    finded = False
    for country, region in countries_list.items():
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
'''
for country, region in countries_list.items():
    for r in result["regions"]:
        if r["name"] == region:
            orig_country_data = country2countrydata(country, orig_data)
            if orig_country_data:
                r["countries"].append(orig_country_data)
            else:
                print("Missed data for", country)
'''
with open('../data/subregions_UN.json', 'w', encoding='utf8') as json_file:
    json.dump(result, json_file, ensure_ascii=False, indent=2)
