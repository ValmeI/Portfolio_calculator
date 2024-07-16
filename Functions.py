import json
import os.path
import time
from datetime import date
from dateutil import relativedelta
# Funderbean imports'
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from config import funderbeam_password, funderbeam_username


PATH_HOME_DESKTOP_PC = r"D:\PycharmProjects/"
PATH_WIN_LAPTOP = r"C:\PycharmProjects/"
PATH_LINUX_LAPTOP = r"/home/ignar-valme-p42/personal_git/Portfolio_calculator/"
PATH_MACBOOK = r"/Users/ignar/Documents/git/Portfolio_calculator"


def chrome_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument('--no-sandbox')  # Bypass OS security model UPDATE 4.06.2021 problems maybe fixed it
    options.add_argument("--log-level=3")  # Adjust the log level
    options.add_argument('--disable-gpu')  # Disabling GPU
    options.add_experimental_option('excludeSwitches', ['enable-logging'])  # This line disables the DevTools logging
    #service = Service(executable_path=r"D:\PycharmProjects\chromedriver.exe")
    service = Service(ChromeDriverManager().install())
    service.log_path = "null"  # Disable driver logs
    service.enable_logging = False  # Disable driver logs
    # UPDATE 25.01.2021 to avoid cannot find Chrome binary error
    # options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    driver = webdriver.Chrome(service=service, options=options)
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
    if os.path.exists(PATH_HOME_DESKTOP_PC):
        return str(PATH_HOME_DESKTOP_PC)
    elif os.path.exists(PATH_WIN_LAPTOP):
        return str(PATH_WIN_LAPTOP)
    elif os.path.exists(PATH_LINUX_LAPTOP):
        return str(PATH_LINUX_LAPTOP)
    elif os.path.exists(PATH_MACBOOK):
        return str(PATH_MACBOOK)
    else:
        print(f"WARNING: Current Device path is not found: {os.getcwd()}")
        return None


def diff_months(date2, date1):
    difference = relativedelta.relativedelta(date2, date1)
    # convert years to months and add previous months
    total_months = difference.years*12+difference.months
    return total_months


def get_funderbeam_marketvalue():
    """
    26.08.2023 - Not used anymore as Funderbeam added 2FA and market value does not change that often anymore
    """
    driver = chrome_driver()
    url = "https://www.funderbeam.com/dashboard"
    driver.get(url)
    driver.find_element(By.NAME, 'username').send_keys(funderbeam_username)
    driver.find_element(By.NAME, 'password').send_keys(funderbeam_password)
    #send enter for links, buttons'
    driver.find_element(By.CLASS_NAME, 'button-primary').send_keys("\n")
    # Sleep so it could load role selection page, UPDATE: 21.04.2021 Before it was 1 sleep time, Funderbeam might have perf problems'
    time.sleep(5)
    # Select element nr 1, as nr 0 is personal role and nr 1 is company role. Need company role'
    driver.find_elements(By.CLASS_NAME, 'cards__title')[1].click()
    # Sleep so it could load company dashboard, UPDATE: 21.04.2021 Before it was 1 sleep time, Funderbeam might have perf problems'
    time.sleep(5)
    # get data from direct url API'
    driver.get('https://www.funderbeam.com/api/user/tokenSummaryStatement')
    # parse only json part of the page source'
    content = driver.find_element(By.TAG_NAME, 'pre').text
    parsed_json = json.loads(content)
    # UPDATE 4.06.2021 problems maybe fixed it'
    driver.quit()
    return parsed_json['totalValueInEur']
