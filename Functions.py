from dateutil import relativedelta
from datetime import date
import os.path

from selenium.webdriver.common.by import By

'# Funderbean imports'
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import json
import pandas as pd
from config import funderbeam_username, funderbeam_password

import chromedriver_autoinstaller

'''Check if the current version of chromedriver exists
and if it doesn't exist, download it automatically,
then add chromedriver to path'''
chromedriver_autoinstaller.install()

'#kodu path'
path_home = r"D:\PycharmProjects/"

'#Laptop path'
path_laptop = r"C:\PycharmProjects/"

'#töö path'
path_work = r"V:\rik_oigusk\Päringud\Krmr\Ignar Valme\PythonProjects/"


def vilde_calculation(input_day, last_calculation_sum, new_sum_to_add, last_input_excel_date):
    if date.today().day == input_day and str(date.today()) != last_input_excel_date:
        new_vilde = float(last_calculation_sum)
        new_vilde += float(new_sum_to_add)
        return new_vilde
    else:
        return float(last_calculation_sum)


def dividend_with_certain_date(sum):
    after_tax = sum - (sum * 0.2)
    return after_tax


def what_path_for_file():
    if os.path.exists(path_home):
        return str(path_home)

    elif os.path.exists(path_work):
        return str(path_work)

    elif os.path.exists(path_laptop):
        return str(path_laptop)


def diff_months(date2, date1):
    '#saada, et palju on tänase ja laenu kuupäevade vahe'
    difference = relativedelta.relativedelta(date2, date1)
    '#konventeerida aastad kuudeks ja liita leitud kuud'
    total_months = difference.years*12+difference.months
    return total_months


'# get funderbeam_marketvalue'


def get_funderbeam_marketvalue():
    options = Options()
    '# parse without displaying Chrome'
    options.add_argument("--headless")
    options.add_argument('--no-sandbox')  # Bypass OS security model UPDATE 4.06.2021 problems maybe fixed it
    '# UPDATE 25.01.2021 to avoid cannot find Chrome binary error'
    #options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    '# get Chrome driver with path'
    driver = webdriver.Chrome("chromedriver.exe", options=options)
    '# url we want to parse'
    url = "https://www.funderbeam.com/dashboard"
    '# get url'
    driver.get(url)
    '# login to funderbeam'
    '# send username'
    driver.find_element(By.NAME, 'username').send_keys(funderbeam_username)
    '# send password'
    driver.find_element(By.NAME, 'password').send_keys(funderbeam_password)
    '#send enter for links, buttons'
    driver.find_element(By.CLASS_NAME, 'button-primary').send_keys("\n")
    '# Sleep so it could load role selection page, UPDATE: 21.04.2021 Before it was 1 sleep time, Funderbeam might have perf problems'
    time.sleep(5)
    '# Select element nr 1, as nr 0 is personal role and nr 1 is company role. Need company role'
    driver.find_elements(By.CLASS_NAME, 'cards__title')[1].click()
    '# Sleep so it could load company dashboard, UPDATE: 21.04.2021 Before it was 1 sleep time, Funderbeam might have perf problems'
    time.sleep(5)
    '# get data from direct url API'
    driver.get('https://www.funderbeam.com/api/user/tokenSummaryStatement')
    '# get page source'
    driver.page_source
    '# parse only json part of the page source'
    content = driver.find_element_by_tag_name('pre').text
    parsed_json = json.loads(content)
    '# to get only marketValueTotal'
    '# 13.05.2022 old pars, before API change'
    #parsed_market_value = parsed_json['totals'][0]['marketValueTotal']
    '# 13.05.2022 new API parse'
    parsed_market_value = parsed_json['totalValueInEur']
    '# UPDATE 4.06.2021 problems maybe fixed it'
    driver.quit()

    return parsed_market_value


def get_funderbeam_companys():
    options = Options()
    '# parse without displaying Chrome'
    options.add_argument("--headless")
    options.add_argument('--no-sandbox')  # Bypass OS security model UPDATE 4.06.2021 problems maybe fixed it
    '# UPDATE 25.01.2021 to avoid cannot find Chrome binary error'
    #options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    '# get Chrome driver with path'
    driver = webdriver.Chrome("chromedriver.exe", options=options)
    '# url we want to parse'
    url = "https://www.funderbeam.com/dashboard"
    '# get url'
    driver.get(url)
    '# login to funderbeam'
    '# send username'
    driver.find_element(By.NAME, 'username').send_keys(funderbeam_username)
    '# send password'
    driver.find_element(By.NAME, 'password').send_keys(funderbeam_password)
    '#send enter for links, buttons'
    driver.find_element(By.CLASS_NAME, 'button-primary').send_keys("\n")
    '# Sleep so it could load role selection page, UPDATE: 21.04.2021 Before it was 1 sleep time, Funderbeam might have perf problems'
    time.sleep(5)
    '# Select element nr 1, as nr 0 is personal role and nr 1 is company role. Need company role'
    driver.find_elements(By.CLASS_NAME, 'cards__title')[1].click()
    '# Sleep so it could load company dashboard, UPDATE: 21.04.2021 Before it was 1 sleep time, Funderbeam might have perf problems'
    time.sleep(5)
    '# get data from direct url API'
    driver.get('https://www.funderbeam.com/api/user/tokenSummaryStatement')
    '# get page source'
    driver.page_source
    '# parse only json part of the page source'
    content = driver.find_element(By.TAG_NAME, 'pre').text

    # without dumps it gives error ValueError: Invalid file path or buffer object type: <class 'dict'>
    parsed_json = json.dumps(content)
    parsed_json = json.loads(parsed_json)
    #print(parsed_json)

    pd.set_option('display.max_rows', None)
    pd.set_option('display.width', None)
    # without lines=true it gives an error
    df = pd.read_json(parsed_json, lines=True)
    #print(df)
    #df.to_excel(r'D:\PycharmProjects\Portfolio_calculator\export_dataframe.xlsx', index=False, header=True)
    df = pd.json_normalize(df['rows'])
    #df.to_excel(r'D:\PycharmProjects\Portfolio_calculator\export_dataframe2.xlsx', index=False, header=True)
    print(df)
    '''df = pd.json_normalize(data=parsed_json, record_path='rows', meta=[#"totalGainInEur",
                                                 #"totalGainPct",
                                                 "totalDayChangeInEur",
                                                 "totalDayChangePct",
                                                 "totalValueInEur"])'''
    print(df.head())
    '# UPDATE 4.06.2021 problems maybe fixed it'
    driver.quit()

    #return parsed_market_value

get_funderbeam_companys()

#path = what_path_for_file()
#print(year_to_year_percent(path + 'Portfolio_calculator/', "Portfell", "01-01", 100))
#get_funderbeam_marketvalue()
