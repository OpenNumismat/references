import json

with open('../src/world.json', encoding='utf-8') as subregions_file:
    world_data = json.load(subregions_file)
    alpha_data = {}
    for country in world_data:
        alpha_data[country['alpha2'].upper()] = country['alpha3'].upper()

with open('../data/countries_old.json', encoding='utf-8') as file:
    orig_data = json.load(file)

with open('../data/unrecognized_countries.json', encoding='utf-8') as file:
    unrecognized_data = json.load(file)

with open('../data/dependend_countries.json', encoding='utf-8') as file:
    dependend_data = json.load(file)

for region in orig_data['regions']:
    for country in region['countries']:
        alpha2 = country['code']
        del country['code']
        country['alpha2'] = alpha2
        if alpha2 in alpha_data:
            alpha3 = alpha_data[alpha2]
            country['alpha3'] = alpha3
        else:
            print("Missed data for", alpha2)

        for unrecognized_country in unrecognized_data:
            if alpha2 == unrecognized_country['alpha2']:
                country['unrecognized'] = True

        if 'alpha3' in country and country['alpha3'] in dependend_data:
            if 'unrecognized' not in country:
                country['dependend'] = True


with open('../data/countries.json', 'w', encoding='utf8') as json_file:
    json.dump(orig_data, json_file, ensure_ascii=False, indent=2)
