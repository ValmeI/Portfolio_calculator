import Aktsiad

jur_eur_stocks = {
                  "EGR1T": 172,
                  "HPR1T": 23,
                  "EXXT": 12.109
                 }

ETH_amount = 0.10581

ETH_EUR = Aktsiad.crypto_in_eur('Ethereum') * ETH_amount

Kelly_raha = 0
Kelly_Invest_raha = 0 + 241 #textmagic
Kelly_Invest_aktsiad = Aktsiad.stocks_value_combined(stock_dictionary=jur_eur_stocks, org_currency=True)

Kelly_Portfell_Kokku = round(Kelly_raha + Kelly_Invest_raha + ETH_EUR + Kelly_Invest_aktsiad)

