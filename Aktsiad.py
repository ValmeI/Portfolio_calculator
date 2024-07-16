import queue
import re
import threading
import warnings

import yfinance as yf
from bs4 import BeautifulSoup

from Functions import chrome_driver

warnings.filterwarnings("ignore", category=DeprecationWarning)

stock_prices_queue = queue.Queue()
GOOGLE_BASE_URL = "https://www.google.com/search?q="


def replace_comma_google(stat) -> str:
    stat = str(stat)
    if "," in stat:
        stat = stat.replace(",", ".")
        return stat
    return stat


def replace_whitespaces(stat) -> str:
    stat = str(stat)
    if " " in stat:
        stat = stat.replace(" ", "")
        return stat
    elif " " in stat:
        stat = stat.replace(" ", "")
        return stat
    return stat


def stock_price_from_google(stock, original_currency) -> float:
    driver = chrome_driver()
    url = GOOGLE_BASE_URL + stock + " stock"
    driver.get(url)
    convert_html = driver.page_source
    soup = BeautifulSoup(convert_html, 'lxml')
    # 12.12.2022 UPDATE, Because of Google doesn't show preview for example EXSA.DE anymore for some reason.
    try:
        # 27.01 Update, parse from google search'
        # 24.06.2022 added replace , with nothing'
        str_price_org_currency = soup.find('span', jsname='vWLAgc').text.strip(',.-').replace(' ', '')#.replace(',', '')
        # 27.01.2020 UPDATE replace comma from google'
    except: # bad practice but works for now will fix it later
        # hack for getting the price for stocks, that google doesn't show preview for example EXSA.DE
        stock = yf.Ticker(stock)
        one_day_close_price = stock.history(period="1d")['Close'][0]
        str_price_org_currency = round(one_day_close_price)

    str_price_org_currency = replace_comma_google(str_price_org_currency)
    if original_currency:
        stock_prices_queue.put({stock: float(str_price_org_currency)})
        driver.quit()
        return float(str_price_org_currency)
    convert_url = GOOGLE_BASE_URL + str_price_org_currency + "+usd+to+eur+currency+converter"
    driver.get(convert_url)
    convert_html = driver.page_source
    soup = BeautifulSoup(convert_html, 'lxml')
    to_eur_convert = soup.find('span', class_='DFlfde SwHCTb').text
    to_eur_convert = replace_whitespaces(to_eur_convert)#.replace(',', '')
    to_eur_convert = replace_comma_google(to_eur_convert)
    to_eur_convert = re.sub("[^0-9.,]", "", to_eur_convert)
    # UPDATE 4.06.2021 problems maybe fixed it'
    driver.quit()
    stock_prices_queue.put({stock: float(to_eur_convert)})
    return float(to_eur_convert)


def stocks_value_combined(stock_dictionary: dict, org_currency: bool) -> int:
    """Returns total value of stocks in portfolio, 
    input: stock dictionary, org_currency = True/False"""
    total_value = 0
    threads = []
    for sym, amount in stock_dictionary.items():
        thread = threading.Thread(target=stock_price_from_google, args=(sym, org_currency))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
    # query the queue for the results
    while not stock_prices_queue.empty():
        item = stock_prices_queue.get()
        for key, value in item.items():
            for sym, amount in stock_dictionary.items():
                # Changed on 14.07.2023 as key values was returned now as "yfinance.Ticker object <EXXT.DE>" and so on
                if sym in str(key):
                    total_value += value * amount
    return round(total_value)


def stock_amount_value(stock_symbol, org_currency, stocks_dictionary):
    """Returns total value of stocks in portfolio,
    input: stock dictionary, org_currency = True/False"""
    price = stock_price_from_google(stock_symbol, org_currency)
    value = price * stocks_dictionary[stock_symbol]
    return round(value, 2)


def stocks_portfolio_percentages(portfolio_size: int, stocks_dictionary: dict, org_currency: bool) -> None:
    """Returns total value of stocks in portfolio,
    input: portfolio size, stock dictionary, org_currency = True/False"""
    for sym, amount in stocks_dictionary.items():
        value = stock_amount_value(sym, org_currency, stocks_dictionary)
        value = round(value, 2)
        percentage = value / portfolio_size * 100
        percentage = round(percentage, 2)
        print(f"Portfelli suurus {portfolio_size} € - Aktsia {sym} väärtus {value} € - Kogus {amount} - Portfellist {percentage} %")


def crypto_in_eur(crypto) -> float:
    driver = chrome_driver()
    url = GOOGLE_BASE_URL + crypto + "  price eur"
    driver.get(url)
    convert_html = driver.page_source
    soup = BeautifulSoup(convert_html, 'lxml')
    try:
        str_price_org_currency = soup.find('span', class_='pclqee').text
    except AttributeError:
        print("Crypto price not found")
        driver.quit()
        return float(0)
    str_price_org_currency = replace_comma_google(str_price_org_currency)
    str_price_org_currency = replace_whitespaces(str_price_org_currency)#.replace(',', '')
    # UPDATE 4.06.2021 problems maybe fixed it'
    driver.quit()
    return float(str_price_org_currency)


def usd_to_eur_convert(number: int) -> float:
    driver = chrome_driver()
    convert_url = GOOGLE_BASE_URL + str(number) + "+usd+to+eur+currency+converter"
    driver.get(convert_url)
    convert_html = driver.page_source
    soup = BeautifulSoup(convert_html, 'lxml')
    to_eur_convert = soup.find('span', class_='DFlfde SwHCTb').text
    to_eur_convert = replace_whitespaces(to_eur_convert)
    to_eur_convert = replace_comma_google(to_eur_convert)
    to_eur_convert = re.sub("[^0-9.,]", "", to_eur_convert)
    driver.quit()
    return float(to_eur_convert)
