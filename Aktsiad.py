from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium.common.exceptions import WebDriverException, NoSuchWindowException
import requests
import threading
from app_logging import logger
import warnings
from bs4 import BeautifulSoup
from Functions import chrome_driver
import config
import time
from utils import get_default_user_agent
import yfinance as yf

warnings.filterwarnings("ignore", category=DeprecationWarning)

GOOGLE_BASE_URL = "https://www.google.com/search?q="
CONVERSION_RATE_CACHE = {}
WEB_SCRAPE_TIMEOUT = 10
API_TIMEOUT = 10
MAX_CONCURRENT_INSTANCES = 5


class StockManager:
    def __init__(self, portfolio_owner: str):
        self.portfolio_owner = portfolio_owner
        self.conversion_rate_cache = {}
        self.web_scrape_timeout = 10
        self.api_timeout = 10
        self.max_concurrent_instances = 5
        self.GOOGLE_BASE_URL = "https://www.google.com/search?q="

    def log_portfolio_query(self, stock: str):
        logger.debug(f"[{self.portfolio_owner}] Querying stock price for {stock}")

    def clean_string(self, input_string: str) -> str:
        input_string = self.replace_comma(input_string)
        input_string = self.replace_whitespaces(input_string)
        return input_string

    def replace_comma(self, stat: str) -> str:
        stat = str(stat)
        return stat.replace(",", ".") if "," in stat or "." in stat else stat

    def replace_whitespaces(self, stat: str) -> str:
        stat = str(stat)
        if " " in stat or " " in stat:
            stat = stat.replace(" ", "").replace(" ", "")
        return stat

    def add_de_suffix(self, stock_symbol: str) -> str:
        return stock_symbol + ".DE"

    def get_stock_price_from_google(self, stock: str, is_in_original_currency: bool, max_retries=3) -> float:
        driver = None  # Initialize driver to None for safety
        try:
            self.log_portfolio_query(stock)
            retries = 0
            while retries < max_retries:
                try:
                    # Initialize the Chrome driver
                    if driver is None:
                        driver = chrome_driver()

                    url = self.GOOGLE_BASE_URL + stock + " stock"
                    driver.get(url)

                    time.sleep(2)  # Give the page some time to load
                    soup = BeautifulSoup(driver.page_source, "lxml")

                    # Check if the stock price element is present
                    stock_price_span = soup.find("span", jsname="vWLAgc")
                    if stock_price_span:
                        str_price_org_currency = stock_price_span.text.strip(",.-").replace(" ", "")
                        str_price_org_currency = str_price_org_currency.replace(",", ".")  # Ensure float format
                        stock_price: float = float(str_price_org_currency)

                        logger.debug(
                            f"[{self.portfolio_owner}] [{threading.current_thread().name}] Fetched stock price {stock_price} for {stock} from Google"
                        )

                        # Return the result based on the currency flag
                        if is_in_original_currency:
                            return stock_price
                        else:
                            stock_price_in_eur = self.usd_to_eur_convert(stock_price)
                            return stock_price_in_eur
                    else:
                        logger.warning(
                            f"[{self.portfolio_owner}] [{threading.current_thread().name}] Google Stock price element not found, retrying..."
                        )
                        retries += 1
                        if retries >= max_retries:
                            return 0.0  # Return 0.0 if max retries reached

                except NoSuchWindowException:
                    logger.warning(f"[{self.portfolio_owner}] Window unexpectedly closed, retrying... Attempt {retries + 1}/{max_retries}")
                    retries += 1
                    driver.quit()  # Close the invalid driver and retry
                    driver = None  # Reset driver to trigger reinitialization
                    time.sleep(1)  # Brief wait before retrying

                except WebDriverException as e:
                    logger.error(f"[{self.portfolio_owner}] WebDriver error on attempt {retries + 1}: {e}")
                    retries += 1
                    driver.quit()
                    driver = None
                    time.sleep(1)

            # Return 0 if unable to fetch after retries
            logger.error(
                f"[{self.portfolio_owner}] [{threading.current_thread().name}] Failed to fetch stock price for {stock} after {max_retries} attempts."
            )
            return 0.0

        except Exception as e:
            logger.error(f"[{self.portfolio_owner}] Unexpected error fetching stock price for {stock}: {e}")
            raise e  # Re-raise the exception after logging

        finally:
            # Ensure driver quits regardless of success or failure
            if driver:
                try:
                    driver.quit()
                except WebDriverException:
                    pass  # Ignore errors if driver is already closed

    def get_stock_price(self, stock: str, is_in_original_currency: bool) -> float:
        self.log_portfolio_query(stock)
        try:
            stock_price = self.get_stock_price_from_finnhub(stock, is_in_original_currency)
            if stock_price == 0.0 or stock_price is None:
                logger.warning(f"[{self.portfolio_owner}] Stock price not found for {stock} from Finnhub, trying yfinance")
                stock_price = self.get_stock_price_from_yfinance(stock, is_in_original_currency)
                if stock_price == 0.0 or stock_price is None:
                    logger.warning(f"[{self.portfolio_owner}] Stock price not found for {stock} from yfinance, trying Google Selenium")
                    stock_price = self.get_stock_price_from_google(stock, is_in_original_currency)
                    if stock_price == 0.0 or stock_price is None:
                        logger.warning(f"[{self.portfolio_owner}] Stock price not found for {stock} from Google, trying Yahoo Selenium")
                        stock_price = self.get_stock_price_from_yahoo_selenium(stock, is_in_original_currency)
            else:
                logger.debug(f"[{self.portfolio_owner}] Stock price for {stock} is {stock_price} from Web Scraper/Finnhub")
            return round(stock_price, 2)
        except Exception:  # bad practice but works for now, will fix it later
            stock_price = self.get_stock_price_from_yahoo_selenium(stock, is_in_original_currency)
            logger.debug(f"[{self.portfolio_owner}] Stock price for {stock} is {stock_price} from Yahoo Selenium")
            return round(stock_price, 2)

    def stocks_value_combined(self, stock_dictionary: dict, org_currency: bool) -> int:
        """Returns total value of stocks in portfolio,
        input: stock dictionary, org_currency = True/False"""
        total_value = 0
        with ThreadPoolExecutor(max_workers=self.max_concurrent_instances) as executor:
            future_to_stock = {executor.submit(self.get_stock_price, sym, org_currency): sym for sym in stock_dictionary}

            for future in as_completed(future_to_stock):
                sym = future_to_stock[future]
                try:
                    stock_price = future.result()
                    if stock_price is None:
                        continue
                    total_value += stock_price * stock_dictionary[sym]
                    logger.info(f"[{self.portfolio_owner}] Stock price for {sym} is {stock_price}")
                except Exception as exc:
                    logger.error(f"[{self.portfolio_owner}] {sym} generated an exception: {exc}")

        return round(total_value)

    def stock_amount_value(self, stock_symbol: str, org_currency: bool, stocks_dictionary: dict) -> float:
        """Returns total value of stocks in portfolio,
        input: stock dictionary, org_currency = True/False"""
        price = self.get_stock_price(stock_symbol, org_currency)
        value = price * stocks_dictionary[stock_symbol]
        return round(value, 2)

    def stocks_portfolio_percentages(self, portfolio_size: int, stocks_dictionary: dict, org_currency: bool) -> None:
        """Returns total value of stocks in portfolio,
        input: portfolio size, stock dictionary, org_currency = True/False"""
        for sym, amount in stocks_dictionary.items():
            value = self.stock_amount_value(sym, org_currency, stocks_dictionary)
            value = round(value, 2)
            percentage = value / portfolio_size * 100
            percentage = round(percentage, 2)
            print(
                f"[{self.portfolio_owner}] Portfelli suurus {portfolio_size} € - Aktsia {sym} väärtus {value} € - Kogus {amount} - Portfellist {percentage} %"
            )

    def crypto_in_eur(self, crypto: str) -> float:
        if crypto is not None:
            crypto = crypto.lower().replace(" ", "")
            logger.debug(f"[{self.portfolio_owner}] Fetching the price of {crypto} in EUR")
            try:
                url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto}&vs_currencies=eur"
                response = requests.get(url, timeout=self.web_scrape_timeout)
                if response.status_code == 200:
                    data = response.json()
                    crypto_price = data[crypto]["eur"]
                    logger.debug(f"[{self.portfolio_owner}] The price of {crypto} in EUR is {crypto_price}")
                    return crypto_price
            except Exception as e:
                logger.error(f"[{self.portfolio_owner}] Failed to fetch the price from the API: {e}")
                return 0
        else:
            logger.error(f"[{self.portfolio_owner}] Failed to fetch the price from the API: crypto is None")
            return 0

    def get_usd_to_eur_conversion_rate(self) -> float:
        if "USD_EUR" not in self.conversion_rate_cache:
            logger.debug(f"[{self.portfolio_owner}] Fetching USD to EUR conversion rate")
            url = "https://api.exchangerate-api.com/v4/latest/USD"
            response = requests.get(url, timeout=self.web_scrape_timeout)
            if response.status_code == 200:
                data = response.json()
                self.conversion_rate_cache["USD_EUR"] = data["rates"]["EUR"]
            else:
                logger.error(f"[{self.portfolio_owner}] Failed to fetch conversion rate from {url}: {response.text}")
        return self.conversion_rate_cache["USD_EUR"]

    def usd_to_eur_convert(self, value_amount: float) -> float:
        conversion_rate = self.get_usd_to_eur_conversion_rate()
        logger.debug(f"[{self.portfolio_owner}] Converting {value_amount} USD to EUR with conversion rate {conversion_rate}")
        return value_amount * conversion_rate

    def get_stock_price_from_finnhub(self, stock: str, is_in_original_currency: bool) -> float:
        try:
            url = f"https://finnhub.io/api/v1/quote?symbol={stock}&token={config.FINNHUB_API_KEY}"
            response = requests.get(url, timeout=self.api_timeout)
            data = response.json()

            if "c" in data:
                latest_price = data["c"]  # 'c' is the current price
                logger.debug(f"[{self.portfolio_owner}] [{threading.current_thread().name}] Stock: {stock} latest price: {latest_price}")
                if latest_price is None:
                    latest_price = data["pc"]  # 'pc' is the previous close
                    logger.debug(f"[{self.portfolio_owner}] [{threading.current_thread().name}] Stock: {stock} previous close: {latest_price}")

                if is_in_original_currency:
                    return float(latest_price)

                stock_price_in_eur = self.usd_to_eur_convert(latest_price)
                return stock_price_in_eur
            return 0.0

        except Exception as e:
            logger.error(f"[{self.portfolio_owner}] Failed to fetch stock price from Finnhub: {e}")
            return 0.0

    def get_stock_price_from_yahoo_selenium(self, stock: str, is_in_original_currency: bool) -> float:
        try:
            url = f"https://finance.yahoo.com/quote/{stock}/"
            headers = {
                "User-Agent": get_default_user_agent(),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Connection": "keep-alive",
            }

            response = requests.get(url, headers=headers, timeout=self.web_scrape_timeout)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                price_span = soup.find("fin-streamer", {"data-symbol": stock, "data-field": "regularMarketPrice"})
                if price_span and price_span.text:
                    price_text = price_span.text.strip().replace(",", "")
                    latest_price = float(price_text)
                    logger.debug(f"[{self.portfolio_owner}] [{threading.current_thread().name}] Stock: {stock} latest price: {latest_price}")
                    if is_in_original_currency:
                        return latest_price
                    else:
                        stock_price_in_eur = self.usd_to_eur_convert(latest_price)
                        return stock_price_in_eur
                else:
                    logger.error(f"[{self.portfolio_owner}] No price data found for {stock}")
                    return 0.0
            else:
                logger.error(f"[{self.portfolio_owner}] Failed to retrieve data. HTTP Status code: {response.status_code}")
                return 0.0
        except Exception as e:
            logger.error(f"[{self.portfolio_owner}] Failed to fetch stock price from Yahoo Finance: {e}")
            return 0.0

    def get_stock_price_from_yfinance(self, stock: str, is_in_original_currency: bool) -> float:
        try:
            ticker = yf.Ticker(stock)
            history_data = ticker.history(period="1d")
            
            if history_data.empty:
                logger.warning(f"[{self.portfolio_owner}] No historical data found for {stock}")
                return 0.0  # Return a default value if no data is found

            latest_price = history_data.iloc[0]["Close"]
            logger.debug(f"[{self.portfolio_owner}] [{threading.current_thread().name}] Stock: {stock} latest price: {latest_price}")
            
            if is_in_original_currency:
                return latest_price
            else:
                stock_price_in_eur = self.usd_to_eur_convert(latest_price)
                return stock_price_in_eur
        except Exception as e:
            logger.error(f"[{self.portfolio_owner}] Failed to fetch stock price from yfinance: {e}")
            return 0.0
