from distutils.command import clean
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


def clean_string(input_string: str) -> str:
    input_string = replace_comma(input_string)
    input_string = replace_whitespaces(input_string)
    return input_string


def replace_comma(stat: str) -> str:
    stat = str(stat)
    if "," in stat:
        stat = stat.replace(",", ".")
        return stat
    return stat


def replace_whitespaces(stat: str) -> str:
    stat = str(stat)
    if " " in stat:
        stat = stat.replace(" ", "")
        return stat
    elif " " in stat:
        stat = stat.replace(" ", "")
        return stat
    return stat


def get_stock_price_from_yfinance(stock: str, original_currency: bool) -> float:
    yahoo_stock = yf.Ticker(stock)
    one_day_close_price = yahoo_stock.history(period="1d")["Close"][0]
    str_price_org_currency = round(one_day_close_price)
    if original_currency:
        return float(str_price_org_currency)
    to_eur_convert = usd_to_eur_convert(stock, str_price_org_currency)
    return float(to_eur_convert)


def get_stock_price_from_google(stock: str, original_currency: bool) -> float:
    driver = chrome_driver()
    url = GOOGLE_BASE_URL + stock + " stock"
    driver.get(url)
    convert_html = driver.page_source
    soup = BeautifulSoup(convert_html, "lxml")
    try:
        str_price_org_currency = soup.find("span", jsname="vWLAgc").text.strip(",.-").replace(" ", "")
    except:  # bad practice but works for now will fix it later
        print(f"Stock price not found for {stock} in Google search")
        driver.quit()
        return float(0)
    str_price_org_currency = replace_comma(str_price_org_currency)
    if original_currency:
        driver.quit()
        return float(str_price_org_currency)
    to_eur_convert = usd_to_eur_convert(stock, str_price_org_currency)
    driver.quit()
    return float(to_eur_convert)


def get_stock_price(stock: str, original_currency: bool) -> float:
    try:
        stock_price = get_stock_price_from_yfinance(stock, original_currency)
        stock_prices_queue.put({stock: float(stock_price)})
        print(f"Stock price for {stock} is {stock_price} from Yahoo Finance")
        return stock_price
    except:  # bad practice but works for now will fix it later
        stock_price = get_stock_price_from_google(stock, original_currency)
        stock_prices_queue.put({stock: float(stock_price)})
        print(f"Stock price for {stock} is {stock_price} from Google Search")
        return stock_price


def stocks_value_combined(stock_dictionary: dict, org_currency: bool) -> int:
    """Returns total value of stocks in portfolio,
    input: stock dictionary, org_currency = True/False"""
    total_value = 0
    threads = []
    for sym, amount in stock_dictionary.items():
        thread = threading.Thread(target=get_stock_price, args=(sym, org_currency))
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


def stock_amount_value(stock_symbol: str, org_currency: bool, stocks_dictionary: dict) -> float:
    """Returns total value of stocks in portfolio,
    input: stock dictionary, org_currency = True/False"""
    price = get_stock_price(stock_symbol, org_currency)
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
        print(
            f"Portfelli suurus {portfolio_size} € - Aktsia {sym} väärtus {value} € - Kogus {amount} - Portfellist {percentage} %"
        )


def crypto_in_eur(crypto: str) -> float:
    driver = chrome_driver()
    url = GOOGLE_BASE_URL + crypto + "  price eur"
    driver.get(url)
    convert_html = driver.page_source
    soup = BeautifulSoup(convert_html, "lxml")
    try:
        str_price_org_currency = soup.find("span", class_="pclqee").text
    except AttributeError:
        print("Crypto price not found")
        driver.quit()
        return float(0)
    str_price_org_currency = clean_string(str_price_org_currency)
    # UPDATE 4.06.2021 problems maybe fixed it'
    driver.quit()
    return float(str_price_org_currency)


def usd_to_eur_convert(stock: str, value_amount: float) -> float:
    print(f"Converting {stock} price of {value_amount} USD to EUR")
    driver = chrome_driver()
    convert_url = GOOGLE_BASE_URL + str(value_amount) + "+usd+to+eur+currency+converter"
    driver.get(convert_url)
    convert_html = driver.page_source
    soup = BeautifulSoup(convert_html, "lxml")
    to_eur_convert = soup.find("span", class_="DFlfde SwHCTb").text
    to_eur_convert = clean_string(to_eur_convert)
    to_eur_convert = re.sub("[^0-9.,]", "", to_eur_convert)
    driver.quit()
    return float(to_eur_convert)
