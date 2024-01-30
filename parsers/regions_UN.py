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
        countries_list[row[8]] = row[3]

with open('../data/country_currency.json', encoding='utf-8') as orig_file:
    orig_data = json.load(orig_file)

result = {
    "regions": [
        {"name": "Europe", "countries": []},
        {"name": "Americas", "countries": []},
        {"name": "Asia", "countries": []},
        {"name": "Africa", "countries": []},
        {"name": "Oceania", "countries": []},
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

with open('../data/regions_UN.json', 'w', encoding='utf8') as json_file:
    json.dump(result, json_file, ensure_ascii=False, indent=2)
