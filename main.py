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
regex_horsepower = r'(?:<dt>Effekt</dt>[\s]*<dd>)([\d]*)(?: Hk</dd>[\n])'
regex_seats = r'(?:<dt>Antall seter</dt>[\s]*<dd>)([\d])(?:</dd>[\n])'
regex_taxclass = r'(?:<dt>Avgiftsklasse</dt>[\s]*<dd>)([\S]*)(?:</dd>[\n])'
regex_registration = r'(?:<dt>Reg\.nr\.</dt>[\s]*<dd>)([\S]*)(?:</dd>[\n])'
regex_chassisnumber = r'(?:<dt>Chassis nr\. \(VIN\)</dt>[\s]*<dd>)([\S]*)(?:</dd>[\n])'

# Getting ad IDs for each match
list_of_ids = re.findall(regex_get_ad_ids, finn_string)

# Function for retrieving regex results
def retrieve_value(regex, ad_html):
    try:
        value = re.findall(regex, ad_html)[0]
    except IndexError:
        value = 'unable to retrieve value'
    return value

# Iterating over the pages, gathering information of interest
for finn_id in list_of_ids:
    print(finn_id)
    ad_html = requests.get(f'https://www.finn.no/car/used/ad.html?finnkode={finn_id}').content.decode('utf8')
    #vd_html = requests.get(f'')

    # Retrieving values from web page
    price = retrieve_value(regex_price, ad_html)
    kilometers = retrieve_value(regex_kilometers, ad_html)
    gearbox = retrieve_value(regex_gearbox, ad_html)
    salestype = retrieve_value(regex_salestype, ad_html)
    year = retrieve_value(regex_year, ad_html)
    color = retrieve_value(regex_color, ad_html)
    horsepower = retrieve_value(regex_horsepower, ad_html)
    seats = retrieve_value(regex_seats, ad_html)
    taxclass = retrieve_value(regex_taxclass, ad_html)
    registration = retrieve_value(regex_registration, ad_html)
    chassisnumber = retrieve_value(regex_chassisnumber, ad_html)
    service = bool(re.search(regex_service, ad_html))
    description = BeautifulSoup(re.findall(regex_description, ad_html)[0], "html5").text

    temp = kilometers.replace(' ', '')

    print(registration, temp)
    
    