from ib_insync import IB, Stock
from typing import Optional
import math
from app_logging import logger
import config


class IBPriceFetcher:
    def __init__(self):
        self.ib = IB()
        self.connect()

    def connect(self):
        try:
            self.ib.connect("127.0.0.1", 4001, clientId=1, timeout=config.API_TIMEOUT)
            self.ib.reqMarketDataType(3)  # Use delayed data if real-time isn't available
            logger.info("Successfully connected to IB Gateway")
        except ConnectionRefusedError:
            logger.error("Check if IB Gateway is running and accessible or try to install it first with shell scripts")
            raise
        except Exception as e:
            logger.error(f"Failed to connect to IB Gateway: {e}")
            raise

    def reconnect(self):
        try:
            # self.disconnect()
            self.connect()
        except Exception as e:
            logger.error(f"Failed to reconnect to IB Gateway: {e}")
            raise

    def get_stock_price(self, symbol: str, currency: str = "USD") -> Optional[float]:
        try:
            if not self.ib.isConnected():
                logger.warning("Lost IB Gateway connection. Reconnecting...")
                self.connect()
            contract = Stock(symbol, "SMART", currency)
            market_data = self.ib.reqMktData(contract, snapshot=True)
            self.ib.sleep(1)  # Wait for market data to update on IB Gateway

            if market_data.last is None:
                logger.warning(f"No price data available for {symbol} from IB Gateway")
                return None
            if math.isnan(market_data.last):
                logger.warning(f"No price data available for {symbol} from IB Gateway")
                self.reconnect()
                return None
            logger.info(f"Successfully fetched price for {symbol} from IB Gateway: {market_data.last} {currency}")
            return market_data.last
        
        except Exception as e:
            logger.error(f"Error fetching price for {symbol}: {e}")
            return None

    def disconnect(self):
        try:
            self.ib.disconnect()
            logger.info("Successfully disconnected from IB Gateway")
        except Exception as e:
            logger.error(f"Error disconnecting from IB Gateway: {e}")

print(IBPriceFetcher().get_stock_price("AAPL"))