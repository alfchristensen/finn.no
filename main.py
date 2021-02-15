import requests
import urllib.request
import re
import csv
from bs4 import BeautifulSoup
import time

finn_string = requests.get('https://www.finn.no/car/used/search.html?mileage_to=300000&model=1.813.1397&price_to=280000&registration_class=1&sort=PRICE_ASC&stored-id=46543826&year_from=2003').content.decode('utf8')

# Regex expressions
regex_get_ad_ids = r'(?:<div aria-owns="ads__unit__content__title)([\d]{9})'
regex_price = r'(?:Totalpris[\s\S]*class=\"u-t3\">)([\d]{3}[\s][\d]{3})(?:[\s]kr</span>)'
regex_kilometers = r'(?:<div>Kilometer<\/div>[\s]*<div class=\"u-strong\">)([\d]{3})(?:[\s])([\d]{3})(?:[\s]km<\/div>)'
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
regex_listprice = r'(?:valuation-price dealer-price\">)([\d]{3})(?:[\s])([\d]{3})(?:[\s]kr<\/div>)'

# Getting ad IDs for each match
list_of_ids = re.findall(regex_get_ad_ids, finn_string)

# Function for retrieving regex results
def retrieve_value(regex, html_ad):
    try:
        value = re.findall(regex, html_ad)[0]
    except IndexError:
        value = False
    return value

# CSV file
with open('cars.csv', "wb") as csv_file:
    writer = csv.writer(csv_file, delimiter=';')
    #for line in data:
        #writer.writerow(line)

    # Iterating over the pages, gathering information of interest
    for finn_id in list_of_ids:

        time.sleep(5)

        html_ad = requests.get(f'https://www.finn.no/car/used/ad.html?finnkode={finn_id}').content.decode('utf8')

        # Retrieving values from web page
        price = retrieve_value(regex_price, html_ad)
        kilometers = str(retrieve_value(regex_kilometers, html_ad)[0]) + str(retrieve_value(regex_kilometers, html_ad)[1])
        gearbox = retrieve_value(regex_gearbox, html_ad)
        salestype = retrieve_value(regex_salestype, html_ad)
        year = retrieve_value(regex_year, html_ad)
        color = retrieve_value(regex_color, html_ad)
        horsepower = retrieve_value(regex_horsepower, html_ad)
        seats = retrieve_value(regex_seats, html_ad)
        taxclass = retrieve_value(regex_taxclass, html_ad)
        registration = retrieve_value(regex_registration, html_ad)
        chassisnumber = retrieve_value(regex_chassisnumber, html_ad)

        # Special cases
        service = bool(re.search(regex_service, html_ad))
        try:
            description = BeautifulSoup(re.findall(regex_description, html_ad)[0], "html5").text
        except:
            description = ''
        link_listprice = f'https://www.kvdnorge.no/bilvardering?regnr={registration}&distance={kilometers}' if registration else ''

        # Print for verification during execution
        print(registration, chassisnumber, service, kilometers, year, price, horsepower, seats, color, taxclass, gearbox, salestype, link_listprice)#, description)

        # Add row to CSV file
        line = [registration, chassisnumber, service, kilometers, year, price, horsepower, seats, color, taxclass, gearbox, salestype, link_listprice, description]
        writer.write(line)
        
        