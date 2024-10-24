from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
import threading
from app_logging import logger
import warnings
from bs4 import BeautifulSoup
from Functions import chrome_driver
import config

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


def get_stock_price(stock: str, is_in_original_currency: bool) -> float:
    logger.debug(f"[{threading.current_thread().name}] fetching stock price for {stock}")
    try:
        stock_price = get_stock_price_from_finnhub(stock, is_in_original_currency)
        if stock_price == 0.0 or stock_price is None:
            logger.warning(f"Stock price not found for {stock} from Finnhub, trying Yahoo Selenium")
            stock_price = get_stock_price_from_google(stock, is_in_original_currency)
        else:
            logger.debug(f"Stock price for {stock} is {stock_price} from Finnhub")
        return round(stock_price, 2)
    except Exception:  # bad practice but works for now, will fix it later
        stock_price = get_stock_price_from_yahoo_selenium(stock, is_in_original_currency)
        logger.debug(f"Stock price for {stock} is {stock_price} from Yahoo Selenium")
        return round(stock_price, 2)


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
    if crypto is not None:
        crypto = crypto.lower().replace(" ", "")
        logger.debug(f"Fetching the price of {crypto} in EUR")
        try:
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto}&vs_currencies=eur"
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                data = response.json()
                crypto_price = data[crypto]["eur"]
                logger.debug(f"The price of {crypto} in EUR is {crypto_price}")
                return crypto_price
        except Exception as e:
            logger.error(f"Failed to fetch the price from the API: {e}")
            return 0
    else:
        logger.error(f"Failed to fetch the price from the API: crypto is None")
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


def get_stock_price_from_finnhub(stock: str, is_in_original_currency: bool) -> float:
    try:
        url = f"https://finnhub.io/api/v1/quote?symbol={stock}&token={config.FINNHUB_API_KEY}"
        response = requests.get(url)
        data = response.json()

        if "c" in data:
            latest_price = data["c"]  # 'c' is the current price
            logger.debug(f"[{threading.current_thread().name}] Stock: {stock} latest price: {latest_price}")
            if latest_price is None:
                latest_price = data["pc"]  # 'pc' is the previous close
                logger.debug(f"[{threading.current_thread().name}] Stock: {stock} previous close: {latest_price}")

            if is_in_original_currency:
                return float(latest_price)

            stock_price_in_eur = usd_to_eur_convert(latest_price)
            return stock_price_in_eur
        else:
            logger.error(f"No price data found for {stock}")
            return 0.0

    except Exception as e:
        logger.error(f"Failed to fetch stock price from Finnhub: {e}")
        return 0.0


def get_stock_price_from_yahoo_selenium(stock: str, is_in_original_currency: bool) -> float:
    try:
        url = f"https://finance.yahoo.com/quote/{stock}/"
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/58.0.3029.110 Safari/537.36"
            )
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            price_span = soup.find("fin-streamer", {"data-symbol": stock, "data-field": "regularMarketPrice"})
            if price_span and price_span.text:
                price_text = price_span.text.strip().replace(",", "")
                latest_price = float(price_text)
                logger.debug(f"[{threading.current_thread().name}] Stock: {stock} latest price: {latest_price}")
                if is_in_original_currency:
                    return latest_price
                else:
                    stock_price_in_eur = usd_to_eur_convert(latest_price)
                    return stock_price_in_eur
            else:
                logger.error(f"No price data found for {stock}")
                return 0.0
        else:
            logger.error(f"Failed to retrieve data. HTTP Status code: {response.status_code}")
            return 0.0
    except Exception as e:
        logger.error(f"Failed to fetch stock price from Yahoo Finance: {e}")
        return 0.0
