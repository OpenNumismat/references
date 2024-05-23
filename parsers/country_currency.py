# -*- coding: utf-8 -*-

import csv
import json
import os
import xml.etree.ElementTree as ET
import lxml.html

from common import *


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

with open('../data/unrecognized_countries.json', encoding='utf-8') as file:
    unrecognized_countries = json.load(file)

with open('../data/disappeared_countries.json', encoding='utf-8') as file:
    disappeared_countries = json.load(file)

with open('../data/contemporary_currency.json', encoding='utf-8') as file:
    contemporary_currencies = json.load(file)

countries_list = []
with open('../src/UNSD — Methodology.csv', encoding='utf-8') as file:
    reader = csv.reader(file, delimiter=';')
    next(reader, None)
    for row in reader:
        countries_list.append(row)


def read_eu_countries():
    eu_countries_list = {}
    page = lxml.html.parse(f"../src/en-5000500.htm")
    table = page.getroot().get_element_by_id("listOfCountriesTable")
    for tr in table[1:]:
        tds = tr.getchildren()
        if len(tds) == 11:
            alpha2 = tds[4].text.strip()

            for text in tds[1].itertext():
                name = text.split('(')[0].strip()
                break
            major = tds[8].text

            minor = tds[10].text
            for text in tds[9].itertext():
                iso4217 = text
                break
        elif len(tds) == 9:
            alpha2 = tds[3].text.strip()

            for text in tds[1].itertext():
                name = text.replace('(', '').strip()
                break
            major = tds[6].text

            minor = tds[8].text
            iso4217 = tds[7].text
        elif len(tds) == 10:
            alpha2 = tds[3].text.strip()

            for text in tds[1].itertext():
                name = text.replace('(', '').strip()
                break
            major = tds[7].text

            minor = tds[9].text
            iso4217 = tds[8].text
        else:
#            print('Check lines:', tds[0].text)
            continue
            
        # https://publications.europa.eu/code/en/en-5000500.htm#an-1
        if alpha2 == 'EL':
            alpha2 = 'GR'
        if alpha2 == 'UK':
            alpha2 = 'GB'
        
        name = name.split('/')[0].strip()
        name = ' '.join(name.split())
        
        if major:
            major = major.strip()
        if major == '—':
            major = None
        if major:
            if major[0] == '(':
                major = major.split(')')[-1]
            else:
                major = major.split('(')[0]
            major = major.split()[-1]
            major = major.title()
        if alpha2 == 'GB':
            major = "Pound"
        elif alpha2 == 'CN':
            major = "Yuan"
        elif alpha2 == 'VE':
            major = "Bolívar"

        if minor == '—':
            minor = None
        if minor:
            minor = minor.replace('[', '').replace(']', '') # TODO: When [] in unit - it's obsolete
            minor = minor.split('(')[0]
            minor = minor.title().strip()

        if not iso4217:
            if tds[8].getchildren():
                iso4217 = tds[8].getchildren()[0].text
            else:
                iso4217 = ""
        iso4217 = iso4217.strip()
        eu_countries_list[alpha2] = {"name": name, "iso4217": iso4217, "dependent": bool(tr.get('class')), "major": major, "minor": minor}
    
    return eu_countries_list


def get_country_mints(alpha3):
    with open('../data/mints.json', encoding='utf-8') as file:
        mints_data = json.load(file)

    result = []
    for mint_data in mints_data:
        if alpha3 in mint_data["country"]:
            result.append(mint_data)

    return result


def process_countries():
    eu_countries_list = read_eu_countries()
    result = {"countries": []}
    for country in countries_list:
        country_name_en = get_alternative_names(country[8])[0]
        alpha2 = country[10]
        alpha3 = country[11]
        
        if alpha3 in ('ATA', 'ESH', 'PSE'):
            continue
    
        data = {
            "name": country_name_en,
            "alpha2": alpha2,
            "alpha3": alpha3,
            "units": [],
        }

        # Upgrade currencies from EU
        if alpha2 in eu_countries_list:
            country_name = eu_countries_list[alpha2]["name"]
            if alpha3 in alternative_names:
                country_name = alternative_names[alpha3][0]
        
            data["name"] = country_name
            data["units"] = []
            if eu_countries_list[alpha2]['major']:
                data["units"].append(eu_countries_list[alpha2]['major'])
            if eu_countries_list[alpha2]['minor']:
                data["units"].append(eu_countries_list[alpha2]['minor'])
            data["iso4217"] = eu_countries_list[alpha2]['iso4217']
            data["key"] = alpha2
        else:
            print(f"Missed currency for {country_name}")

        for contemporary in contemporary_currencies:
            if contemporary['alpha3'] == alpha3:
                data["contemporary_units"] = contemporary['units']
                break

        if 'alpha3' in data and alpha3 in dependend_data:
            data['dependent'] = True
    #        if 'unrecognized' not in data:
    #            data['dependent'] = True

        mints = get_country_mints(alpha3)
        if mints:
            data['mints'] = mints

        result["countries"].append(data)

    for data in unrecognized_countries:
        data['unrecognized'] = True

        alpha3 = data['alpha3']
        mints = get_country_mints(alpha3)
        if mints:
            data['mints'] = mints

        alpha2 = data['alpha2']
        if alpha2:
            data["key"] = alpha2
        else:
            data["key"] = "_" + data["name"].lower().replace(' ', '-')

        result["countries"].append(data)

    for data in disappeared_countries:
        data['disappeared'] = True

        alpha3 = data['alpha3']
        mints = get_country_mints(alpha3)
        if mints:
            data['mints'] = mints

        alpha2 = data['alpha2']
        if alpha2:
            data["key"] = alpha2
        else:
            data["key"] = "_" + data["name"].lower().replace(' ', '-')

        result["countries"].append(data)

    with open(f"../data/country_currency.json", 'w', encoding='utf8') as json_file:
        json.dump(result, json_file, ensure_ascii=False, indent=2)


process_countries()
