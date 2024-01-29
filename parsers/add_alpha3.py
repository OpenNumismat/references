import json

with open('../src/ISO-3166-Countries-with-Regional-Codes.json', encoding='utf-8') as subregions_file:
    subregions_data = json.load(subregions_file)
    alpha_data = {}
    for country in subregions_data:
        alpha_data[country['alpha-2']] = country['alpha-3']

with open('../data/countries_old.json', encoding='utf-8') as orig_file:
    orig_data = json.load(orig_file)

with open('../data/unrecognized_countries.json', encoding='utf-8') as orig_file:
    unrecognized_data = json.load(orig_file)

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
            if alpha2 == unrecognized_country['alpha-2']:
                country['unrecognized'] = True

with open('../data/countries.json', 'w', encoding='utf8') as json_file:
    json.dump(orig_data, json_file, ensure_ascii=False, indent=2)
