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


def chrome_driver():
    options = Options()
    '# parse without displaying Chrome'
    options.add_argument("--headless")
    options.add_argument('--no-sandbox')  # Bypass OS security model UPDATE 4.06.2021 problems maybe fixed it
    '# UPDATE 25.01.2021 to avoid cannot find Chrome binary error'
    # options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    driver = webdriver.Chrome(r"D:\PycharmProjects\chromedriver.exe", options=options)
    return driver

def vilde_calculation(input_day, last_calculation_sum, new_sum_to_add, last_input_excel_date):
    if date.today().day == input_day and str(date.today()) != last_input_excel_date:
        new_vilde = float(last_calculation_sum)
        new_vilde += float(new_sum_to_add)
        return new_vilde
    else:
        return float(last_calculation_sum)


def dividend_with_certain_date(total):
    after_tax = total - (total * 0.2)
    return after_tax


def what_path_for_file():
    if os.path.exists(path_home):
        return str(path_home)
    elif os.path.exists(path_laptop):
        return str(path_laptop)


def diff_months(date2, date1):
    difference = relativedelta.relativedelta(date2, date1)
    # convert years to months and add previous months
    total_months = difference.years*12+difference.months
    return total_months


def get_funderbeam_marketvalue():
    driver = chrome_driver()
    url = "https://www.funderbeam.com/dashboard"
    driver.get(url)
    driver.find_element(By.NAME, 'username').send_keys(funderbeam_username)
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
    '# parse only json part of the page source'
    content = driver.find_element(By.TAG_NAME, 'pre').text
    parsed_json = json.loads(content)
    '# UPDATE 4.06.2021 problems maybe fixed it'
    driver.quit()
    return parsed_json['totalValueInEur']


def get_funderbeam_syndicate_listings():
    driver = chrome_driver()
    url = "https://www.funderbeam.com/dashboard"
    driver.get(url)
    '# login to funderbeam'
    driver.find_element(By.NAME, 'username').send_keys(funderbeam_username)
    driver.find_element(By.NAME, 'password').send_keys(funderbeam_password)
    '#send enter for links, buttons'
    driver.find_element(By.CLASS_NAME, 'button-primary').send_keys("\n")
    '# Sleep so it could load role selection page, UPDATE: 21.04.2021 Before it was 1 sleep time, Funderbeam might have perf problems'
    time.sleep(5)
    '# Select element nr 1, as nr 0 is personal role and nr 1 is company role. Need company role'
    driver.find_elements(By.CLASS_NAME, 'cards__title')[1].click()
    '# Sleep so it could load company dashboard, UPDATE: 21.04.2021 Before it was 1 sleep time, Funderbeam might have perf problems'
    time.sleep(5)
    driver.get('https://www.funderbeam.com/api/user/tokenSummaryStatement')
    '# parse only json part of the page source'
    content = driver.find_element(By.TAG_NAME, 'pre').text
    # without dump's it gives error ValueError: Invalid file path or buffer object type: <class 'dict'>
    parsed_json = json.dumps(content)
    parsed_json = json.loads(parsed_json)
    # without lines=true it gives an error
    df = pd.read_json(parsed_json, lines=True)
    # drop empty or columns that are not needed.
    # where 1 is the axis number (0 for rows and 1 for columns.)
    df = df.drop(['portfolioCompanies', 'portfolioIndustries', 'portfolioCountries'], axis=1)
    json_struct = json.loads(df.to_json(orient="records"))
    # without record_prefix it gives an ValueError: Conflicting metadata name totalGainPct, need distinguishing prefix
    df = pd.json_normalize(data=json_struct, record_path='rows', record_prefix='_', meta=["totalGainInEur", "totalGainPct",
                                                                                          "totalDayChangeInEur", "totalDayChangePct",
                                                                                          "totalValueInEur"])
    list_from_df = df.values.tolist()
    '# UPDATE 4.06.2021 problems maybe fixed it'
    driver.quit()
    return list_from_df

# get_funderbeam_syndicate_listings()
