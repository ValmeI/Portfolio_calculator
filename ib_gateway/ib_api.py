from ib_insync import IB, Stock
from typing import Optional
from app_logging import logger
import config


class IBPriceFetcher:
    def __init__(self):
        self.ib = IB()
        self._is_connected = False
        self.connect()

    def connect(self):
        try:
            if not self._is_connected:
                self.ib.connect("127.0.0.1", 4001, clientId=1, timeout=config.API_TIMEOUT)
                self.ib.reqMarketDataType(3)  # Use delayed data if real-time isn't available
                self._is_connected = True
                logger.info("Successfully connected to IB Gateway")
        except ConnectionRefusedError:
            logger.error("Check if IB Gateway is running and accessible or try to install it first with shell scripts")
            raise
        except Exception as e:
            logger.error(f"Failed to connect to IB Gateway: {e}")
            raise

    def reconnect(self):
        try:
            self.disconnect()
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
            bars = self.ib.reqHistoricalData(
                contract,
                endDateTime="",  # Latest available data
                durationStr="1 D",  # Fetch last 1 day
                barSizeSetting="1 day",  # Daily close price
                whatToShow="TRADES",
                useRTH=True,  # Regular Trading Hours only
                formatDate=1,
            )

            if not bars:
                logger.warning(f"No historical data available for {symbol} on IB Gateway")
                return None

            close_price = bars[-1].close
            logger.info(f"Fetched historical close price for {symbol}: {close_price} {currency} from IB Gateway")
            return round(close_price, 2)

        except Exception as e:
            logger.error(f"Error fetching price for {symbol}: {e} from IB Gateway")
            return None

    def disconnect(self):
        try:
            if self._is_connected:
                self.ib.disconnect()
                self._is_connected = False
                logger.info("Successfully disconnected from IB Gateway")
        except Exception as e:
            logger.error(f"Error disconnecting from IB Gateway: {e}")

    def __del__(self):
        """Ensure cleanup on object destruction"""
        self.disconnect()
