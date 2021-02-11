import requests
import urllib.request
import re
import csv
from bs4 import BeautifulSoup

finn_string = requests.get('https://www.finn.no/car/used/search.html?condition=1&mileage_to=280000&model=1.813.1397&price_to=280000&sort=PUBLISHED_DESC&year_from=2007').content.decode('utf8')

# Regex expressions
regex_get_ad_ids = r'(?:<div aria-owns="ads__unit__content__title)([\d]{9})'
regex_price = r'(?:Totalpris[\s\S]*class=\"u-t3\">)([\d]{3}[\s][\d]{3})(?:[\s]kr</span>)'
regex_kilometers = r'(?:<div>Kilometer</div>[\s\S]*<div class=\"u-strong\">)([\d]{3}[\s][\d]{3})(?:[\s]km</div>)'
regex_gearbox = r'(?:<div>Girkasse</div>[\s\S]*<div class=\"u-strong\">)(Automat|Manuell)(?:</div>)'
regex_service = r'Bilens serviceprogram er fulgt. Det er tatt servicer på bilen i henhold til fabrikkens retningslinjer.'
regex_description = r'(?:Beskrivelse</h2>[\n][\s]*)([\s\S]*)(?:Spesifikasjoner)'
regex_salestype = r'(?:Salgsform</dt>[\s]*<dd>)([ \S]*)(?:</dd>[\n])'
regex_year = r'(?:<dt>1. gang registrert</dt>[\s]*<dd>[\d]{2}.[\d]{2}.)([\d]{4})(?:</dd>[\n])'
regex_color = r'(?:<dt>Farge</dt>[\s]*<dd>)([\S]*)(?:</dd>[\n])'

# Getting ad IDs for each match
list_of_ids = re.findall(regex_get_ad_ids, finn_string)

# Iterating over the pages, gathering information of interest
for finn_id in list_of_ids:
    print(finn_id)
    ad_html = requests.get(f'https://www.finn.no/car/used/ad.html?finnkode={finn_id}').content.decode('utf8')

    # Retrieving values from web page
    try:
        price = re.findall(regex_price, ad_html)[0]
    except IndexError:
        price = 'price not found'
    try:
        kilometers = re.findall(regex_kilometers, ad_html)[0]
    except IndexError:
        kilometers = 'kilometers not found'
    try:
        gearbox = re.findall(regex_gearbox, ad_html)[0]
    except IndexError:
        gearbox = 'gearbox not found'
    if re.search(regex_service, ad_html):
        service = True
    else:
        service = False
    try:
        description = BeautifulSoup(re.findall(regex_description, ad_html, )[0], "html5").text
    except IndexError:
        description = 'could not retrieve description'
    try:
        salestype = re.findall(regex_salestype, ad_html)[0]
    except IndexError:
        salestype = 'sales type could not be retrieved'
    try:
        year = re.findall(regex_year, ad_html)[0]
    except IndexError:
        year = 'could not retrieve year'
    try:
        color = re.findall(regex_color, ad_html)[0]
    except IndexError:
        color = 'could not retrieve color'
    