# -*- coding: utf-8 -*-

import csv
import json
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

with open('../data/countries_alternative_names.json', encoding='utf-8') as file:
    alternative_names = json.load(file)

with open('../data/contemporary_currency.json', encoding='utf-8') as file:
    contemporary_currencies = json.load(file)

countries_list = []
with open('../src/UNSD — Methodology.csv', encoding='utf-8') as file:
    reader = csv.reader(file, delimiter=';')
    next(reader, None)
    for row in reader:
        countries_list.append(row)


def read_eu_countries(lang):
    eu_countries_list = {}
    page = lxml.html.parse(f"../src/{lang}-5000500.htm")
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
            if lang == 'fr':
                major = major.replace('le ', '').replace('la ', '').replace('l’', '')
            major = major.strip()
        if major == '—':
            major = None
        if major:
            if major[0] == '(':
                major = major.split(')')[-1]
            else:
                major = major.split('(')[0]
            if lang in ('fr', 'it', 'es', 'el', 'pl', 'pt'):
                major = major.split()[0]
            else:
                major = major.split()[-1]
                if lang in ('de', 'hu', 'nl', 'sv'):
                    major = major.split('-')[-1]
                    major = major.split('/')[-1]
            major = major.title()
        if alpha2 == 'GB' and lang == 'en':
            major = "Pound"
        elif alpha2 == 'CN' and lang == 'en':
            major = "Yuan"
        elif alpha2 == 'VE' and lang == 'en':
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


def process_countries(lang):
    eu_countries_list = read_eu_countries(lang)
    result = {"countries": {}}
    for country in countries_list:
        alpha2 = country[10]
        alpha3 = country[11]

        country_name = get_alternative_names(country[8])[0]
        result["countries"][country_name] = country_name

        if lang != 'en':
            if alpha2 in eu_countries_list:
                country_name_lang = eu_countries_list[alpha2]["name"]
                result["countries"][country_name] = country_name_lang

    for data in unrecognized_countries:
        country_name = data["name"]
        result["countries"][country_name] = country_name

    for data in disappeared_countries:
        country_name = data["name"]
        result["countries"][country_name] = country_name

    with open(f"../i18n/countries_{lang}.json", 'w', encoding='utf8') as json_file:
        json.dump(result, json_file, ensure_ascii=False, indent=2)


for lang in ('en', 'bg', 'es', 'cs', 'de', 'el', 'et', 'fr', 'it', 'lv', 'hu', 'nl', 'pl', 'pt', 'sk', 'sl', 'sv'):
    process_countries(lang)
