import json
import os.path
import time
from datetime import date
from venv import logger
from dateutil import relativedelta

# Funderbean imports'
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from config import FUNDERBEAM_PASSWORD, FUNDERBEAM_USERNAME
from typing import Optional


def chrome_driver() -> WebDriver:
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-background-networking")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    # Define the local path to chromedriver
    chromedriver_path = "/Users/ignar/.wdm/drivers/chromedriver/mac64/130.0.6723.69/chromedriver-mac-arm64/chromedriver"

    # Check if chromedriver exists locally, otherwise install it
    if not os.path.exists(chromedriver_path):
        logger.info("Chromedriver not found locally. Installing with webdriver_manager...")
        chromedriver_path = ChromeDriverManager().install()

    # Initialize the Service with the determined path
    service = Service(executable_path=chromedriver_path)
    service.log_path = "null"

    # Start Chrome with the defined options and service
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def vilde_calculation(
    input_day: int, last_calculation_sum: float, new_sum_to_add: float, last_input_excel_date: str
) -> float:
    logger.debug(f"inputs are {input_day}, {last_calculation_sum}, {new_sum_to_add}, {last_input_excel_date}")
    if date.today().day == input_day and str(date.today()) != last_input_excel_date:
        new_vilde = float(last_calculation_sum)
        new_vilde += float(new_sum_to_add)
        return float(new_vilde)
    else:
        return float(last_calculation_sum)


def dividend_with_certain_date(total: float) -> float:
    after_tax = total - (total * 0.2)
    return after_tax


def what_path_for_file() -> Optional[str]:
    project_root = os.path.abspath(os.path.dirname(__file__))
    return project_root


def diff_months(date2: date, date1: date) -> int:
    difference = relativedelta.relativedelta(date2, date1)
    # convert years to months and add previous months
    total_months = difference.years * 12 + difference.months
    return total_months


def get_funderbeam_marketvalue() -> float:
    """
    26.08.2023 - Not used anymore as Funderbeam added 2FA and market value does not change that often anymore
    """
    driver = chrome_driver()
    url = "https://www.funderbeam.com/dashboard"
    driver.get(url)
    driver.find_element(By.NAME, "username").send_keys(FUNDERBEAM_USERNAME)
    driver.find_element(By.NAME, "password").send_keys(FUNDERBEAM_PASSWORD)
    # send enter for links, buttons'
    driver.find_element(By.CLASS_NAME, "button-primary").send_keys("\n")
    # Sleep so it could load role selection page, UPDATE: 21.04.2021 Before it was 1 sleep time, Funderbeam might have perf problems'
    time.sleep(5)
    # Select element nr 1, as nr 0 is personal role and nr 1 is company role. Need company role'
    driver.find_elements(By.CLASS_NAME, "cards__title")[1].click()
    # Sleep so it could load company dashboard, UPDATE: 21.04.2021 Before it was 1 sleep time, Funderbeam might have perf problems'
    time.sleep(5)
    # get data from direct url API'
    driver.get("https://www.funderbeam.com/api/user/tokenSummaryStatement")
    # parse only json part of the page source'
    content = driver.find_element(By.TAG_NAME, "pre").text
    parsed_json = json.loads(content)
    # UPDATE 4.06.2021 problems maybe fixed it'
    driver.quit()
    return parsed_json["totalValueInEur"]
