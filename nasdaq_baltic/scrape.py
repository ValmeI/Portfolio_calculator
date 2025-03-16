import requests
from bs4 import BeautifulSoup
import config
from typing import Optional
from app_logging import logger


class NasdaqBalticPriceScrape:
    def __init__(self, portfolio_owner: str):
        self.url = "https://nasdaqbaltic.com/statistics/et/shares"
        self.portfolio_owner = portfolio_owner

    def get_stock_price(self, symbol: str) -> Optional[float]:
        try:
            response = requests.get(self.url, timeout=config.WEB_SCRAPE_TIMEOUT)
            soup = BeautifulSoup(response.text, "html.parser")
            stock_row = soup.find("td", string=symbol)
            if not stock_row:
                logger.warning(f"Stock {symbol} not found on Nasdaq Baltic")
                return None

            price_column = stock_row.find_next_sibling("td")
            price = price_column.text.strip().replace(",", ".")

            logger.info(f"[{self.portfolio_owner}] Stock: {symbol} latest price: {price} EUR from Nasdaq Baltic")
            return float(price)

        except Exception as e:
            logger.error(f"[{self.portfolio_owner}] Failed to fetch stock price from Nasdaq Baltic: {e}")
            return None
