# -*- coding: utf-8 -*-

import csv
import json
import xml.etree.ElementTree as ET
import lxml.html

def get_alternative_names(country):
    country = country.lower()
    for names in alternative_names.values():
        for name in names:
            if name.lower() == country:
                return names
    return [country,]

def country2iso4217(country, currencies_list):
    names = get_alternative_names(country)
    for key, value in currencies_list.items():
        key = key.replace(' (THE)', '').lower()
        for name in names:
            if name.lower() == key:
                return value
    return None


with open('../data/dependent_countries.json', encoding='utf-8') as file:
    dependend_data = json.load(file)

with open('../data/countries_alternative_names.json', encoding='utf-8') as file:
    alternative_names = json.load(file)

countries_list = []
with open('../src/UNSD — Methodology.csv', encoding='utf-8') as file:
    reader = csv.reader(file, delimiter=';')
    next(reader, None)
    for row in reader:
        countries_list.append(row)

currencies_list = {}
tree = ET.parse('../src/list-one.xml')
CcyTbl = tree.getroot()
for CcyNtry in CcyTbl[0]:
    Ccy = CcyNtry.find('Ccy')
    if Ccy is not None:
        CtryNm = CcyNtry.find('CtryNm')
        if not CtryNm.text.startswith('ZZ'):
            if CtryNm.text not in currencies_list:
                currencies_list[CtryNm.text] = Ccy.text

eu_countries_list = {}
page = lxml.html.parse('../src/en-5000500.html')
table = page.getroot().get_element_by_id("listOfCountriesTable")
for tr in table[1:]:
    tds = tr.getchildren()
    if len(tds) == 10:
        alpha2 = tds[3].text
        # https://publications.europa.eu/code/en/en-5000500.htm#an-1
        if alpha2 == 'EL':
            alpha2 = 'GR'
        if alpha2 == 'UK':
            alpha2 = 'GB'
        
        for text in tds[1].itertext():
            name = text.replace('(', '').strip()
            break

        major = tds[7].text
        if major == '—':
            major = None
        if major:
            major = major.split('(')[0]
            major = major.split()[-1]
            major = major.title()
        minor = tds[9].text
        if minor == '—':
            minor = None
        if minor:
            minor = minor.replace('[', '').replace(']', '') # TODO: When [] in unit - it's obsolete
            minor = minor.split('(')[0]
            minor = minor.title().strip()

        eu_countries_list[alpha2] = {"name": name, "iso4217": tds[8].text, "dependent": bool(tr.get('class')), "major": major, "minor": minor}
#    else:
#        print('Check lines:', tds[0].text)

with open('../src/currencies.json', encoding='utf-8') as orig_file:
    currencies_data = json.load(orig_file)

result = {"countries": []}
for country in countries_list:
    country_name = country[8]
    alpha2 = country[10]
    alpha3 = country[11]
    
    if alpha3 in alternative_names:
        country_name = alternative_names[alpha3][0]
    
    data = {
        "name": country_name,
        "alpha2": alpha2,
        "alpha3": alpha3,
        "units": [],
    }

    iso4217 = country2iso4217(country_name, currencies_list)
    if iso4217:
        data["iso4217"] = iso4217
        if iso4217 in currencies_data:
            data["units"].append(currencies_data[iso4217]["majorSingle"])
            data["units"].append(currencies_data[iso4217]["minorSingle"])
        else:
            print("Missed currency for", country_name)
    else:
        print("Missed iso4217 for", country_name)
    
    # Upgrade currencies from EU
    if alpha2 in eu_countries_list:
        data["units"] = []
        if eu_countries_list[alpha2]['major']:
            data["units"].append(eu_countries_list[alpha2]['major'])
        if eu_countries_list[alpha2]['minor']:
            data["units"].append(eu_countries_list[alpha2]['minor'])
    else:
        print("Missed EU currency for", country_name)

    if 'alpha3' in data and data['alpha3'] in dependend_data:
        data['dependent'] = True
#        if 'unrecognized' not in data:
#            data['dependent'] = True

    result["countries"].append(data)

with open('../data/unrecognized_countries.json', encoding='utf-8') as file:
    unrecognized_countries = json.load(file)

for data in unrecognized_countries:
    data['unrecognized'] = True
    result["countries"].append(data)

with open('../data/country_currency.json', 'w', encoding='utf8') as json_file:
    json.dump(result, json_file, ensure_ascii=False, indent=2)
