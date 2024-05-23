Sources:
- data/icons/flags/famfamfam - https://github.com/legacy-icons/famfamfam-flags/tree/1.0.0
- data/icons/flags/GoSquared - https://github.com/gosquared/flags
- data/icons/flags/StefanGabos - https://github.com/stefangabos/world_countries/tree/v2.8.2
- data/icons/flags/Wikipedia - https://github.com/rinvex/countries/tree/v9.0.1

- src/UNSD — Methodology.csv - https://unstats.un.org/unsd/methodology/m49/overview/
- src/list-one.xml - https://www.six-group.com/en/products-services/financial-information/data-standards.html
- src/en-5000500.html - https://publications.europa.eu/code/en/en-5000500.htm
- src/CLASS.xlsx - https://datatopics.worldbank.org/world-development-indicators/the-world-by-income-and-region.html
- src/Area.csv - https://www.cia.gov/the-world-factbook/field/area/country-comparison/
- src/OBJECTIVE_LISTS.html - https://objectivelists.com/2022/12/30/regions-of-the-world/
- src/mints.csv - https://onlinecoin.club/Info/Mints/

- src/countries.json - https://github.com/stefangabos/world_countries/tree/v2.8.2/data/countries/_combined
- src/world.json - https://github.com/stefangabos/world_countries/tree/v2.8.2/data/countries/_combined
- src/currencies.json - https://github.com/ourworldincode/currency/tree/main

Parsers and datas:
- data/<region_source>_<lang>.json - result files used by references.js
- parsers/<region_source>_lang.py - generate data/<region_source>_<lang>.json from src/<src>, data/country_currency.json, i18n/regions_{lang}.json, i18n/countries_{lang}.json, i18n/currencies_{lang}.json
- parsers/country_currency.py - generate data/country_currency.json
