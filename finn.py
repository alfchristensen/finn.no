import requests
import urllib.request
import re
import csv
from bs4 import BeautifulSoup
import time
import listprice

# Regex expressions
regex_get_ad_ids = r'(?:<div aria-owns="ads__unit__content__title)([\d]{9})'
regex_price = r'(?:Totalpris<\/span>[\s]*<span class="u-t3">)([\d]{3})(?:[\s])([\d]{3})(?:[\s]kr<\/span>)'
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

# Function for retrieving regex results
def retrieve_value(regex, html_ad):
    try:
        value = re.findall(regex, html_ad)[0]
    except IndexError:
        value = False
    return value

# Function for obtaining two dimentional list containing detailed results for all cars
def get_car_details(finn_search):

    # Defining list to hold results
    car_list = []
    
    # Getting list of ad IDs for each match
    finn_string = requests.get(finn_search).content.decode('utf8')
    list_of_ids = re.findall(regex_get_ad_ids, finn_string)

    # Iterating over the pages, gathering information of interest
    for finn_id in list_of_ids:

        # Sleeping thread to avoid finn rejecting requests
        time.sleep(1)

        # Loading web page
        html_ad = requests.get(f'https://www.finn.no/car/used/ad.html?finnkode={finn_id}').content.decode('utf8')

        # Retrieving values from web page
        price = int(str(retrieve_value(regex_price, html_ad)[0]) + str(retrieve_value(regex_price, html_ad)[1]))
        kilometers = int(str(retrieve_value(regex_kilometers, html_ad)[0]) + str(retrieve_value(regex_kilometers, html_ad)[1]))
        gearbox = retrieve_value(regex_gearbox, html_ad)
        salestype = retrieve_value(regex_salestype, html_ad)
        year = int(retrieve_value(regex_year, html_ad))
        color = retrieve_value(regex_color, html_ad)
        horsepower = int(retrieve_value(regex_horsepower, html_ad))
        seats = int(retrieve_value(regex_seats, html_ad))
        taxclass = retrieve_value(regex_taxclass, html_ad)
        registration = retrieve_value(regex_registration, html_ad)
        chassisnumber = retrieve_value(regex_chassisnumber, html_ad)

        # Special cases
        if registration and kilometers:
            print(registration, kilometers)
            try:
                list_price = listprice.get_listprice(str(registration), str(kilometers))
            #    print(list_price)
            except Exception as e:
                print('failed with exception:', e)
                list_price = 0
            #break
        else:
            registration = 0
        service = bool(re.search(regex_service, html_ad))
        
        
        #try:
        #    description = BeautifulSoup(re.findall(regex_description, html_ad)[0], "html5").text
        #except:
        #    description = ''

        # Add results to list
        car_list.append([registration, chassisnumber, service, kilometers, year, price, list_price, horsepower, seats, color, taxclass, gearbox, salestype, f'https://www.finn.no/car/used/ad.html?finnkode={finn_id}'])

    # Return result
    return car_list