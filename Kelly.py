from Aktsiad import StockManager

JUR_EUR_STOCKS = {
    "EGR1T.TL": 172,
    "HPR1T.TL": 23,
    "EXXT.DE": 45.863,
    "MAGIC.RG": 35,
    "IITU.L": 0.12,
}  # for some reason IITU is divided by 100

ETH_AMOUNT = 0.10581

kelly_stocks_manager = StockManager("Kelly")
ETH_EUR = kelly_stocks_manager.crypto_in_eur("ethereum") * ETH_AMOUNT

KELLY_RAHA = 0
KELLY_INVEST_RAHA = 0
Kelly_Invest_aktsiad = kelly_stocks_manager.stocks_value_combined(stock_dictionary=JUR_EUR_STOCKS, org_currency=True)

Kelly_Portfell_Kokku = round(KELLY_RAHA + KELLY_INVEST_RAHA + ETH_EUR + Kelly_Invest_aktsiad)
