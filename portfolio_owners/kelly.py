from aktsiad import StockManager

JUR_EUR_STOCKS = {"EXXT": 56.011}

ETH_AMOUNT = 0

kelly_stocks_manager = StockManager("Kelly")
ETH_EUR = kelly_stocks_manager.crypto_in_eur("ethereum") * ETH_AMOUNT

KELLY_RAHA = 0
KELLY_INVEST_RAHA = 0
Kelly_Invest_aktsiad = kelly_stocks_manager.stocks_value_combined(stock_dictionary=JUR_EUR_STOCKS, org_currency=True)

Kelly_Portfell_Kokku = round(KELLY_RAHA + KELLY_INVEST_RAHA + ETH_EUR + Kelly_Invest_aktsiad)
