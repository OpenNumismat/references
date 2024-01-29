import json

independend_alpha3 = []
with open('../src/countries.json', encoding='utf-8') as orig_file:
    countries_data = json.load(orig_file)
    for country in countries_data:
        independend_alpha3.append(country['alpha3'])

with open('../src/world.json', encoding='utf-8') as orig_file:
    world_data = json.load(orig_file)

result = []
for world_country in world_data:
    alpha3 = world_country['alpha3']
    if alpha3 in independend_alpha3:
        continue

    result.append(alpha3.upper())

with open('../data/dependend_countries.json', 'w', encoding='utf8') as json_file:
    json.dump(result, json_file, ensure_ascii=False, indent=2)
