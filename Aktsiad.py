from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
import threading
import queue
import chromedriver_autoinstaller
# ignore DeprecationWarning
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

'''Check if the current version of chromedriver exists
and if it doesn't exist, download it automatically,
then add chromedriver to path'''
chromedriver_autoinstaller.install()
stock_prices_queue = queue.Queue()


# removes comma in numbers. Is needed to convert to float. Numbers like 1,0000 and so on
def replace_comma_google(stat):
    stat = str(stat)
    if "," in stat:
        stat = stat.replace(",", ".")
        return stat
    else:
        return stat


# removes whitespaces in numbers. Is needed to convert to float. Numbers like 1 000 and so on
def replace_whitespaces(stat):
    stat = str(stat)
    if " " in stat:
        stat = stat.replace(" ", "")
        return stat
    elif " " in stat:
        stat = stat.replace(" ", "")
        return stat
    else:
        return stat


def stock_price_from_google(stock, original_currency):

    options = Options()
    '# add options to chrome, to run it headless as not opening it'
    options.add_argument("--headless")
    options.add_argument('--no-sandbox')  # Bypass OS security model UPDATE 4.06.2021 problems maybe fixed it
    '# UPDATE 25.01.2021 to avoid cannot find Chrome binary error'
    #options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    driver = webdriver.Chrome("chromedriver.exe", options=options)
    url = "https://www.google.com/search?q=" + stock + " stock"
    driver.get(url)

    convert_html = driver.page_source
    soup = BeautifulSoup(convert_html, 'lxml')

    # 12.12.2022 UPDATE, Because of Google doesn't show preview for example EXSA.DE anymore for some reason.
    try:
        '# 27.01 Update, parse from google search'
        '# 24.06.2022 added replace , with nothing'
        str_price_org_currency = soup.find('span', jsname='vWLAgc').text.strip(',.-').replace(' ', '')#.replace(',', '')
        '# 27.01.2020 UPDATE replace comma from google'
    except:
        # hack for getting the price for stocks, that google doesn't show preview for example EXSA.DE
        import yfinance as yf
        stock = yf.Ticker(stock)
        one_day_close_price = stock.history(period="1d")['Close'][0]
        str_price_org_currency = round(one_day_close_price)

    str_price_org_currency = replace_comma_google(str_price_org_currency)
    if original_currency:

        stock_prices_queue.put({stock: float(str_price_org_currency)})
        driver.quit()
        '#Returns original currency'
        return float(str_price_org_currency)
    else:
        '#Converts and Returns currency in euros'

        '# UPDATE 25.08.2018 USD to EUR converting page started using JS and I needed to use Selenium and Soup but'
        '# UPDATE 25.08.2018 opening every page in Chrome and parsing made it much more slower'
        '# UPDATE 14.01.2021 use Google as currency converter service'
        convert_url = "https://www.google.com/search?q=" + str_price_org_currency + "+usd+to+eur+currency+converter"
        driver.get(convert_url)
        convert_html = driver.page_source
        soup = BeautifulSoup(convert_html, 'lxml')
        to_eur_convert = soup.find('span', class_='DFlfde SwHCTb').text
        '# 24.06.2022 added replace , with nothing'
        to_eur_convert = replace_whitespaces(to_eur_convert)#.replace(',', '')
        '# 27.01.2020 UPDATE replace comma from convert'
        to_eur_convert = replace_comma_google(to_eur_convert)
        '# 15.10.2021 UPDATE only keep numbers and ,.'
        to_eur_convert = re.sub("[^0-9.,]", "", to_eur_convert)
        '# UPDATE 4.06.2021 problems maybe fixed it'
        driver.quit()
        stock_prices_queue.put({stock: float(to_eur_convert)})
        return float(to_eur_convert)


# Stock list input and True/False as do you want it to bet original currency or in euros'
def stocks_value_combined(stock_dictionary, org_currency):
    total_value = 0
    threads = []
    for sym, amount in stock_dictionary.items():
        thread = threading.Thread(target=stock_price_from_google, args=(sym, org_currency))
        thread.start()
        threads.append(thread)

    # wait till all the threads are done
    for thread in threads:
        thread.join()
    # query the queue for the results
    while not stock_prices_queue.empty():
        item = stock_prices_queue.get()
        for key, value in item.items():
            for sym, amount in stock_dictionary.items():
                """Changed on 14.07.2023 as key values was returned now as "yfinance.Ticker object <EXXT.DE>" and so on"""
                if sym in str(key):
                    total_value += value * amount
    return round(total_value)


# Single stock price, input symbol, org_currency = True/False and stock dictionary
def stock_amount_value(stock_symbol, org_currency, stocks_dictionary):
        amount = stocks_dictionary[stock_symbol]
        price = stock_price_from_google(stock_symbol, org_currency)
        value = price * stocks_dictionary[stock_symbol]
        return value


# Portfolio stocks %, input: Portfolio size, stock dictionary, org_currency = True/False
def stocks_portfolio_percentages(portfolio_size, stocks_dictionary, org_currency):
    for sym, amount in stocks_dictionary.items():
        value = stock_amount_value(sym, org_currency, stocks_dictionary)
        value = round(value, 2)
        percentage = value / portfolio_size * 100
        percentage = round(percentage, 2)
        print("Portfelli suurus {} € - Aktsia {} väärtus {} € - Kogus {} - Portfellist {} %"
              .format(portfolio_size, sym, value, amount, percentage))


# convert bitcoin to eur
def crypto_in_eur(crypto):

    options = Options()
    '# add options to chrome, to run it headless as not opening it'
    options.add_argument("--headless")
    options.add_argument('--no-sandbox')  # Bypass OS security model UPDATE 4.06.2021 problems maybe fixed it
    #options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    driver = webdriver.Chrome("chromedriver.exe", options=options)
    url = "https://www.google.com/search?q=" + crypto + "  price eur"
    driver.get(url)
    convert_html = driver.page_source
    soup = BeautifulSoup(convert_html, 'lxml')
    str_price_org_currency = soup.find('span', class_='pclqee').text
    str_price_org_currency = replace_comma_google(str_price_org_currency)
    str_price_org_currency = replace_whitespaces(str_price_org_currency)#.replace(',', '')
    '# UPDATE 4.06.2021 problems maybe fixed it'
    driver.quit()
    return float(str_price_org_currency)


def usd_to_eur_convert(number):

    options = Options()
    '# add options to chrome, to run it headless as not opening it'
    options.add_argument("--headless")
    options.add_argument('--no-sandbox')  # Bypass OS security model UPDATE 4.06.2021 problems maybe fixed it
    '# UPDATE 25.01.2021 to avoid cannot find Chrome binary error'
    #options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    driver = webdriver.Chrome("chromedriver.exe", options=options)
    convert_url = "https://www.google.com/search?q=" + str(number) + "+usd+to+eur+currency+converter"
    driver.get(convert_url)
    convert_html = driver.page_source
    '# scrape with BeautifulSoup'
    soup = BeautifulSoup(convert_html, 'lxml')
    to_eur_convert = soup.find('span', class_='DFlfde SwHCTb').text
    to_eur_convert = replace_whitespaces(to_eur_convert)
    '# 27.01.2020 UPDATE replace comma from convert'
    to_eur_convert = replace_comma_google(to_eur_convert)
    '# 15.10.2021 UPDATE only keep numbers and ,.'
    to_eur_convert = re.sub("[^0-9.,]", "", to_eur_convert)
    '# UPDATE 4.06.2021 problems maybe fixed it'
    driver.quit()
    return float(to_eur_convert)


'''print("AAPL", stock_price_from_google("AAPL", True))
print("TSLA", stock_price_from_google("TSLA", False))
print("AMD", stock_price_from_google("AMD", False))
print("MSFT", stock_price_from_google("MSFT", False))
print("AMZN", stock_price_from_google("AMZN", False))
print("GOOGL", stock_price_from_google("GOOGL", False))
print("NIO", stock_price_from_google("NIO", False))
print("XPEV", stock_price_from_google("XPEV", False))
print("NKE", stock_price_from_google("NKE", False))
print("NFLX", stock_price_from_google("NFLX", False))
print("NVDA", stock_price_from_google("NVDA", False))
print("INTC", stock_price_from_google("INTC", False))
print("SNOW", stock_price_from_google("SNOW", False))'''

'''
stock_dictionary_test = {"AAPL": 1, "TSLA": 1, "AMD": 1, "MSFT": 1, "AMZN": 1, "GOOGL": 1, "NIO": 1, "XPEV": 1, "NKE": 1, "NFLX": 1, "NVDA": 1, "INTC": 1, "SNOW": 1}
#stock_dictionary_test = {"AAPL": 1, "TSLA": 1}
from datetime import datetime
print('Start time: ', datetime.now())
res = stocks_value_combined(jur_usa_stocks, True)
print('stocks_value_combined', res)
# loop stock_prices_queue queue while empty
#while not stock_prices_queue.empty():
    #print(stock_prices_queue.get())
print('End time: ', datetime.now())

'''