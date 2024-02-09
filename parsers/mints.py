import csv
import json

def get_alternative_names(country):
    country = country.lower()
    for names in alternative_names.values():
        for name in names:
            if name.lower() == country:
                return names
    return [country,]

with open('../data/countries_alternative_names.json', encoding='utf-8') as file:
    alternative_names = json.load(file)

with open('../data/country_currency.json', encoding='utf-8') as orig_file:
    orig_data = json.load(orig_file)

mints_list = []
with open('../src/mints.csv', encoding='utf-8') as file:
    reader = csv.reader(file, delimiter='\t')
    next(reader, None)
    for row in reader:
        mints_list.append(row)

result = []
for mint in mints_list:
    if len(mint) >= 5:
        location = mint[2].split(', ')[0]
        country = get_alternative_names(mint[1])
        country_data = {}
        for orig_country_data in orig_data["countries"]:
            if orig_country_data["name"].lower() == country[0].lower():
                country_data = {orig_country_data["alpha3"]: orig_country_data["name"]}
                break
        if not country_data:
            print(f"Missed country {country[0]}")
        mint_data = {
            "name": mint[0],
            "country": country_data,
            "location": location,
            "from_year": int(mint[3]),
        }
        if mint[4]:
            mint_data["to_year"] = int(mint[4])
        result.append(mint_data)

with open('../data/mints.json', 'w', encoding='utf8') as json_file:
    json.dump(result, json_file, ensure_ascii=False, indent=2)
