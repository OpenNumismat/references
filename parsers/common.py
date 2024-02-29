import json
import os


def lang_list():
    return ('en', 'bg', 'es', 'cs', 'de', 'el', 'fr', 'it', 'lv', 'hu', 'nl', 'pl', 'pt', 'sv')

regions = {}
def get_regions(name, lang):
    result = {"regions": []}

    path = f'../i18n/regions_{lang}.json'
    if not os.path.isfile(path):
        path = f'../i18n/regions_en.json'

    with open(path, encoding='utf-8') as file:
        data = json.load(file)
        
        global regions
        regions = data[name]
        
        for region, region_name in regions.items():
            result["regions"].append({"name": region_name, "countries": []})
        
    return result

def region2region_name(region):
    if region in regions:
        return regions[region]
    else:
        return None

with open('../data/countries_alternative_names.json', encoding='utf-8') as file:
    alternative_names = json.load(file)

def get_alternative_names(country):
    for names in alternative_names.values():
        for name in names:
            if name.lower() == country.lower():
                return names
    return [country,]