from aktsiad import StockManager

JUR_EUR_STOCKS = {"EXXT": 56.011}

kelly_stocks_manager = StockManager("Kelly")

KELLY_RAHA = 0
KELLY_INVEST_RAHA = 0
Kelly_Invest_aktsiad = kelly_stocks_manager.stocks_value_combined(stock_dictionary=JUR_EUR_STOCKS, org_currency=True)

Kelly_Portfell_Kokku = round(KELLY_RAHA + KELLY_INVEST_RAHA + Kelly_Invest_aktsiad)
