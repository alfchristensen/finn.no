from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

def get_listprice(registration, kilometers):

    print(f'https://www.kvdnorge.no/bilvardering?regnr={registration}&distance={kilometers}')
    
    # prepare the option for the chrome driver
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('page_load_strategy=normal')

    # start chrome browser
    browser = webdriver.Chrome(options=options)
    browser.get(f'https://www.kvdnorge.no/bilvardering?regnr={registration}&distance={kilometers}')
    try:
        WebDriverWait(browser, 5).until(EC.text_to_be_present_in_element((By.XPATH, '//*[contains(@class, "valuation-price dealer-price")]'), 'kr'))
    finally:
        html_result = browser.page_source
    browser.quit()
    regex_listprice = r'(?:<div class=\"valuation-price dealer-price\">)([\d]{3})(?:[\s])([\d]{3})(?:[\s]kr</div>)'
    listprice = int(str(re.findall(regex_listprice, html_result)[0][0]) + str(re.findall(regex_listprice, html_result)[0][1]))

    return listprice

#listprice = get_listprice('NV58051', '231850')

#print(listprice)
