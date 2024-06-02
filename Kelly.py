import Aktsiad

JUR_EUR_STOCKS = {
                "EGR1T": 172,
                "HPR1T": 23,
                "EXXT.DE": 39.671,
                "MAGIC.RG": 35
                }

ETH_AMOUNT = 0.10581

ETH_EUR = Aktsiad.crypto_in_eur('Ethereum') * ETH_AMOUNT

KELLY_RAHA = 0
KELLY_INVEST_RAHA = 0
Kelly_Invest_aktsiad = Aktsiad.stocks_value_combined(stock_dictionary=JUR_EUR_STOCKS, org_currency=True)

Kelly_Portfell_Kokku = round(KELLY_RAHA + KELLY_INVEST_RAHA + ETH_EUR + Kelly_Invest_aktsiad)
