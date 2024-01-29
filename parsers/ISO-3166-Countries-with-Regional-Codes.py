import json

def alpha2countrydata(alpha, orig_data):
    for country in orig_data["countries"]:
        if country["alpha2"] == alpha:
            return country
    return None
    

with open('../src/ISO-3166-Countries-with-Regional-Codes.json', encoding='utf-8') as subregions_file:
    subregions_data = json.load(subregions_file)

with open('../data/countries.json', encoding='utf-8') as orig_file:
    orig_data = json.load(orig_file)

regions_order = [
"Europe",
"Americas",
"Asia",
"Africa",
"Oceania",
]

result = {
    "regions": []
}

for region in regions_order:
    result["regions"].append({
        "name": region,
        "countries": [],
    })

for country in subregions_data:
#    if country['region'] in regions_order:
#        region = country['region']

    for r in result["regions"]:
        if r["name"] == country['region']:
            orig_country_data = alpha2countrydata(country['alpha-2'], orig_data)
            if orig_country_data:
                r["countries"].append(orig_country_data)
            else:
                print("Missed data for", country['alpha-2'])

with open('../data/Regions (UN).json', 'w', encoding='utf8') as json_file:
    json.dump(result, json_file, ensure_ascii=False, indent=2)
