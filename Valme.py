import Aktsiad
import Morr
import Excel_functions
import Functions as F
from datetime import date
from Functions import what_path_for_file

path = what_path_for_file()

fys_eur_stocks = {"TKM1T": 355,
                  "EFT1T": 113
                  }

jur_usa_stocks = {"AAPL": 69,
                  "TSLA": 15,
                  "AMD": 78,
                  "MSFT": 10,
                  "AMZN": 56,
                  "GOOGL": 36,
                  "NIO": 93,
                  "XPEV": 72,
                  "NKE": 11,
                  "NVDA": 1,
                  "INTC": 25,
                  "SNOW": 6
                  }

'# Crypto Amounts'
BTC_amount = 0.021538
ETH_amount = 0.12037

ETH_EUR = Aktsiad.crypto_in_eur('Ethereum') * ETH_amount
Bitcoin_EUR = Aktsiad.crypto_in_eur('bitcoin') * BTC_amount

'#Vanad ja refinants Akadeemia laenu kuupäevad yyyy.mm.dd'
Vana_Aka42_63_Laen_Kuupäev = date(2016, 2, 16)
Vana_Aka38_20_Laen_Kuupäev = date(2017, 5, 9)

Aka42_63_Laen_Kuupäev = date(2018, 12, 5)
# Aka38_20_Laen_Kuupäev = date(2018, 12, 5)
Vilde90_193_Laen_Kuupäev = date(2019, 4, 9)

# emale võlg 10k
FüsIsikRaha = -10000
FysIsikAktsaid = Aktsiad.stocks_value_combined(stock_dictionary=fys_eur_stocks, org_currency=True)

'# Vaba raha ja aktsiad kokku'
FysIsik = round(FüsIsikRaha + FysIsikAktsaid)

CleveronAktsia = 4 * 1050
JurAktsiad = round(Aktsiad.stocks_value_combined(stock_dictionary=jur_usa_stocks, org_currency=False) + CleveronAktsia)
Jur_Krypto = round(Bitcoin_EUR + ETH_EUR)

'#jur isiku raha LHV'
JurRaha = 1800
'# get Funderbeam total'
JurFunderBeam = F.get_funderbeam_marketvalue()
Jur_IB_Raha = -100
JurIsik = round(JurRaha + JurFunderBeam + Jur_IB_Raha + JurAktsiad + Morr.ValCapitalRaha / 2 + Jur_Krypto)
'# Mörr on väike karu'


'# Raha ehk likviitsus,ka Krypto, jur ja fys kokku'
RahaKokku = round(FüsIsikRaha + JurRaha + Morr.ValCapitalRaha / 2 + Jur_IB_Raha + Jur_Krypto)

'# üür'
vilde_isa = 240
vilde_laen = 170.31 # alates oktoobrist on tegelikult 163.35 EUR kuu
vilde_kindlustus = 6.91
'# ehk kuupäev millal arvutust tehakse'
arvutamise_kp = 1

Uus_vilde_summa = F.vilde_calculation(input_day=arvutamise_kp,
                                      last_calculation_sum=Excel_functions.get_last_row(excel_name="Portfell", column_number=9),
                                      new_sum_to_add=round(F.dividend_with_certain_date(vilde_isa) - vilde_laen - vilde_kindlustus, 2),
                                      last_input_excel_date=Excel_functions.get_last_row(excel_name="Portfell", column_number=1)
                                      )

'# to avoid too many decimal places'
Uus_vilde_summa = round(Uus_vilde_summa, 2)
