import csv
import json

def country2countrydata(country, orig_data):
    for orig_country in orig_data["countries"]:
        if orig_country["name"] == country:
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

for country, region in countries_list.items():
    for r in result["regions"]:
        if r["name"] == region:
            orig_country_data = country2countrydata(country, orig_data)
            if orig_country_data:
                r["countries"].append(orig_country_data)
            else:
                print("Missed data for", country)

with open('../data/subregions_UN.json', 'w', encoding='utf8') as json_file:
    json.dump(result, json_file, ensure_ascii=False, indent=2)
