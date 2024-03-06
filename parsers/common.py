import json
import os


def lang_list():
    return ('en', 'bg', 'ca', 'es', 'cs', 'de', 'el', 'et', 'fa', 'fr', 'it', 'lv', 'hu', 'nl', 'pl', 'pt', 'ru', 'sk', 'sl', 'sv', 'tk', 'uk')

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

def get_translated_country_names(lang):
    path = f'../i18n/countries_{lang}.json'
    if not os.path.isfile(path):
        path = f'../i18n/countries_en.json'

    with open(path, encoding='utf-8') as file:
        data = json.load(file)
        return data["countries"]

def get_translated_currency_names(lang):
    path = f'../i18n/currencies_{lang}.json'
    if not os.path.isfile(path):
        path = f'../i18n/currencies_en.json'

    with open(path, encoding='utf-8') as file:
        data = json.load(file)
        return data["currencies"]
