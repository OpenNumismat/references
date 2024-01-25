import json

def alpha2countrydata(alpha, orig_data):
    for region in orig_data["regions"]:
        for country in region["countries"]:
            if country["alpha2"] == alpha:
                return country
    return None
    

with open('../src/ISO-3166-Countries-with-Regional-Codes.json', encoding='utf-8') as subregions_file:
    subregions_data = json.load(subregions_file)

with open('../data/countries.json', encoding='utf-8') as orig_file:
    orig_data = json.load(orig_file)

subregions_order = [
"Western Europe",
"Northern Europe",
"Southern Europe",
"Eastern Europe",

"Western Asia",
"Central Asia",
"Southern Asia",
"Eastern Asia",
"South-eastern Asia",

"Northern Africa",
"Western Africa",
"Middle Africa",
"Eastern Africa",
"Southern Africa",

"Northern America",
"Central America",
"Caribbean",
"South America",

"Australia and New Zealand",
"Melanesia",
"Micronesia",
"Polynesia",
]

result = {
    "regions": []
}

for region in subregions_order:
    result["regions"].append({
        "name": region,
        "countries": [],
    })

for country in subregions_data:
    if country['intermediate-region'] in subregions_order:
        region = country['intermediate-region']
    else:
        region = country['sub-region']
    for r in result["regions"]:
        if r["name"] == region:
            orig_country_data = alpha2countrydata(country['alpha-2'], orig_data)
            if orig_country_data:
                r["countries"].append(orig_country_data)
            else:
                print("Missed data for", country['alpha-2'])

with open('../data/Subregions (UN).json', 'w', encoding='utf8') as json_file:
    json.dump(result, json_file, ensure_ascii=False, indent=2)
