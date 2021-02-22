from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

def get_listprice(registration, kilometers):

    #print(f'https://www.kvdnorge.no/bilvardering?regnr={registration}&distance={kilometers}')
    
    # prepare the option for the chrome driver
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('page_load_strategy=normal')

    # start chrome browser
    browser = webdriver.Chrome(executable_path='/home/vmd/git/finn.no/chromedriver', options=options)
    #browser.get(f'https://www.kvdnorge.no/bilvardering?regnr={registration}&distance={kilometers}')
    try:
        browser.get(f'https://www.kvdnorge.no/bilvardering?regnr={registration}&distance={kilometers}')
        WebDriverWait(browser, 30).until(EC.text_to_be_present_in_element((By.XPATH, '//*[contains(@class, "valuation-price dealer-price")]'), 'kr'))
        html_result = browser.page_source
        browser.quit()
        regex_listprice = r'(?:<div class=\"valuation-price dealer-price\">)([\d]{3})(?:[\s])([\d]{3})(?:[\s]kr</div>)'
        list_price = int(str(re.findall(regex_listprice, html_result)[0][0]) + str(re.findall(regex_listprice, html_result)[0][1]))
    except TimeoutError as e:
        print('timeout error:', e)
        list_price = 0

    return list_price

#listprice = get_listprice('NV58051', '231850')

#print(listprice)
