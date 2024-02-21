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
        countries_list[row[11]] = row[3]

with open('../data/countries_alternative_names.json', encoding='utf-8') as file:
    alternative_names = json.load(file)

for lang in ('en', 'bg', 'es', 'cs', 'de', 'el', 'fr', 'it', 'lv', 'hu', 'nl', 'pl', 'pt', 'sv'):
    result = {
        "regions": [
            {"name": "Europe", "countries": []},
            {"name": "Americas", "countries": []},
            {"name": "Asia", "countries": []},
            {"name": "Africa", "countries": []},
            {"name": "Oceania", "countries": []},
        ]
    }

    with open(f"../data/country_currency_{lang}.json", encoding='utf-8') as orig_file:
        orig_data = json.load(orig_file)

    for orig_country in orig_data["countries"]:
        finded = False
        for alpha3, region in countries_list.items():
#            if compare_county_names(country, orig_country["name"]):
            if alpha3 == orig_country["alpha3"]:
                for r in result["regions"]:
                    if r["name"] == region:
                        r["countries"].append(orig_country)
                        finded = True
                        break
                break

        if not finded and ("unrecognized" in orig_country or "disappeared" in orig_country):
            for r in result["regions"]:
                for c in r["countries"]:
                    if c["alpha3"] == orig_country["part_of"]:
                        r["countries"].append(orig_country)
                        finded = True
                        break

        if not finded:
            print("Missed data for", orig_country["name"])

    with open(f"../data/regions_UN_{lang}.json", 'w', encoding='utf8') as json_file:
        json.dump(result, json_file, ensure_ascii=False, indent=2)
