from dateutil import relativedelta
from datetime import date
import xlrd
import os.path
import pandas as pd
from dateutil.parser import parse

'# Funderbean imports'
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import json

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
    options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    '# get Chrome driver with path'
    driver = webdriver.Chrome("chromedriver.exe", options=options)
    '# url we want to parse'
    url = "https://www.funderbeam.com/dashboard"
    '# get url'
    driver.get(url)

    '# Pass file name'
    password_file = 'FunderPass'

    '# get password form file, read only'
    open_file = open(password_file + ".txt", 'r')
    for password in open_file:
        '# send username'
        driver.find_element_by_name('username').send_keys('ignarvalme@gmail.com')
        '# send password'
        driver.find_element_by_name('password').send_keys(password)
        '#send enter for links, buttons'
        driver.find_element_by_class_name('button-primary').send_keys("\n")
        '# Sleep so it could load role selection page, UPDATE: 21.04.2021 Before it was 1 sleep time, Funderbeam might have perf problems'
        time.sleep(5)
        '# Select element nr 1, as nr 0 is personal role and nr 1 is company role. Need company role'
        driver.find_elements_by_class_name('cards__title')[1].click()
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


def year_to_year_percent(path, excel_name, mm_dd, todays_total_portfolio):
    '# lisab file type'
    file_name = excel_name + ".xlsx"
    '# open excel file'
    rb = xlrd.open_workbook(path + file_name)
    first_sheet = rb.sheet_by_index(0)

    '# all dates and all values from total sum of portfolio'
    date_and_sum_dict = dict(zip(first_sheet.col_values(0), first_sheet.col_values(5)))

    amount_list = []
    date_list = []
    '# to filter out only give dates (mm_dd input) and sums'
    for date1, amount in date_and_sum_dict.items():
        if mm_dd in date1:

            amount_list.append(round(amount))
            date_list.append(date1)

            '# is same year as last row (for example 2022-01-01) and it is not January 1st, then add today s portfolio amount'
            if date.today().year == parse(date1).date().year and date.today().month != '1' and date.today().day != '1':
                amount_list.append(round(todays_total_portfolio))
                date_list.append(date.today())

    previous_amount_list = []
    percentage_increase_list = []

    '# to get previous vs current values and percentage increase'
    for previous, current in zip(amount_list, amount_list[1:]):
        percentage_increase = round(100*((current-previous)/previous))
        previous_amount_list.append(previous)
        percentage_increase_list.append(str(percentage_increase) + ' %')

    '# need to add 0 to the beginning of list, so dataframe would have exactly same amount of rows'
    if len(previous_amount_list) != len(date_list):
        '# pos and value added'
        previous_amount_list.insert(0, 0)

    if len(percentage_increase_list) != len(date_list):
        '# pos and value added'
        percentage_increase_list.insert(0, '0 %')

    data = {"Aasta": date_list,
             "Portfell eelmisel aastal": previous_amount_list,
             "Portfell see aasta": amount_list,
             "Protsendiline muutus": percentage_increase_list}

    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    df = pd.DataFrame(data)

    return df


#path = what_path_for_file()
#print(year_to_year_percent(path + 'Portfolio_calculator/', "Portfell", "01-01", 100))
#get_funderbeam_marketvalue()
