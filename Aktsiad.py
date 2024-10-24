from concurrent.futures import ThreadPoolExecutor, as_completed
from math import log
import threading
from tkinter import N
import requests
from app_logging import logger
import warnings
import yfinance as yf
from bs4 import BeautifulSoup
from Functions import chrome_driver
import logging

warnings.filterwarnings("ignore", category=DeprecationWarning)

GOOGLE_BASE_URL = "https://www.google.com/search?q="
CONVERSION_RATE_CACHE = {}


def clean_string(input_string: str) -> str:
    input_string = replace_comma(input_string)
    input_string = replace_whitespaces(input_string)
    return input_string


def replace_comma(stat: str) -> str:
    stat = str(stat)
    return stat.replace(",", ".") if "," in stat or "." in stat else stat


def replace_whitespaces(stat: str) -> str:
    stat = str(stat)
    if " " in stat or " " in stat:
        stat = stat.replace(" ", "").replace(" ", "")
    return stat


def add_de_suffix(stock_symbol: str) -> str:
    return stock_symbol + ".DE"


def get_stock_price_from_yfinance(stock: str, original_currency: bool) -> float:
    try:
        # Suppress "No data found, symbol may be delisted"
        logging.getLogger("yfinance").setLevel(logging.CRITICAL)
        yahoo_stock = yf.Ticker(stock)
        stock_history = yahoo_stock.history(period="2d")
        if stock_history.empty:
            stock = add_de_suffix(stock)
            yahoo_stock = yf.Ticker(stock)
            stock_history = yahoo_stock.history(period="2d")
        one_day_close_price = stock_history["Close"][0]
        stock_price = round(one_day_close_price)
    except IndexError:
        logger.warning(f"Could not fetch stock price for {stock}")
    if original_currency:
        try:
            return stock_price
        except ValueError:
            logger.error(f"Could not convert {stock_price} to float")
    stock_price_in_eur = usd_to_eur_convert(stock_price)
    return stock_price_in_eur


def get_stock_price_from_google(stock: str, is_in_original_currency: bool) -> float:
    try:
        logger.debug(f"[{threading.current_thread().name}] fetching stock price for {stock} from Google")
        driver = None
        if driver is None:
            driver = chrome_driver()
        url = GOOGLE_BASE_URL + stock + " stock"
        driver.get(url)
        convert_html = driver.page_source
        soup = BeautifulSoup(convert_html, "lxml")
        str_price_org_currency = soup.find("span", jsname="vWLAgc").text.strip(",.-").replace(" ", "")
        str_price_org_currency = replace_comma(str_price_org_currency)
        stock_price: float = float(str_price_org_currency)
        logger.debug(
            f"[{threading.current_thread().name}] fetched stock price {stock_price} from stock {stock} from Google"
        )
        if is_in_original_currency:
            driver.quit()
            return stock_price
        stock_price_in_eur = usd_to_eur_convert(stock_price)
        driver.quit()
        return stock_price_in_eur
    except Exception as e:
        # bad practice but works for now will fix it later
        logger.error(f"Stock price not found for {stock} in Google search, error: {e}")
        driver.quit()
        raise e


def get_stock_price(stock: str, original_currency: bool) -> float:
    logger.debug(f"[{threading.current_thread().name}] fetching stock price for {stock}")
    try:
        stock_price = get_stock_price_from_yfinance(stock, original_currency)
        if stock_price == 0.0:
            logger.warning(f"Stock price not found for {stock} from Yahoo Finance, trying Google Search")
            stock_price = get_stock_price_from_google(stock, original_currency)
        else:
            logger.debug(f"Stock price for {stock} is {stock_price} from Yahoo Finance")
        return stock_price
    except Exception:  # bad practice but works for now, will fix it later
        stock_price = get_stock_price_from_google(stock, original_currency)
        return stock_price


def stocks_value_combined(stock_dictionary: dict, org_currency: bool) -> int:
    """Returns total value of stocks in portfolio,
    input: stock dictionary, org_currency = True/False"""
    total_value = 0

    with ThreadPoolExecutor() as executor:
        future_to_stock = {executor.submit(get_stock_price, sym, org_currency): sym for sym in stock_dictionary}

        for future in as_completed(future_to_stock):
            sym = future_to_stock[future]
            try:
                stock_price = future.result()
                if stock_price is None:
                    continue
                total_value += stock_price * stock_dictionary[sym]
            except Exception as exc:
                logger.error(f"{sym} generated an exception: {exc}")

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
    if crypto is None:
        logger.error("Crypto is None")
    return 0
    crypto = crypto.lower().replace(" ", "")
    logger.debug(f"Fetching the price of {crypto} in EUR")
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto}&vs_currencies=eur"
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            data = response.json()
            return data[crypto]["eur"]
    except Exception as e:
        logger.error(f"Failed to fetch the price from the API: {e}")
        return 0


def get_usd_to_eur_conversion_rate() -> float:
    if "USD_EUR" not in CONVERSION_RATE_CACHE:
        logger.debug("Fetching USD to EUR conversion rate")
        url = "https://api.exchangerate-api.com/v4/latest/USD"
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            data = response.json()
            CONVERSION_RATE_CACHE["USD_EUR"] = data["rates"]["EUR"]
        else:
            logger.error(f"Failed to fetch conversion rate from {url}: {response.text}")
    return CONVERSION_RATE_CACHE["USD_EUR"]


def usd_to_eur_convert(value_amount: float) -> float:
    conversion_rate = get_usd_to_eur_conversion_rate()
    logger.debug(f"Converting {value_amount} USD to EUR with conversion rate {conversion_rate}")
    return value_amount * conversion_rate
