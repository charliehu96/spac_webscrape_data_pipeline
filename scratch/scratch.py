import csv
import re
import pandas as pd
import requests
from bs4 import BeautifulSoup
import yfinance
from alpha_vantage.timeseries import TimeSeries

API_KEY = 'WHXQSQM1UJHHWOO0'
# with open('spac.html', 'r') as f:
#     html_string = f.read()

# soup = BeautifulSoup(html_string, 'lxml')
# # print(soup.prettify())
# company_link = []
# for tr in soup.find_all('tr'):
#     try:
#         company_link.append(tr.td.a.get('href'))
#     except:
#         pass
# # print(company_link)

# ticker = yfinance.Ticker("CGROW")
# print(ticker.info)
# hist = ticker.history(period='6mo')
# print(hist)


# for link in company_link:
# def scratch():
#     spac_list = []
#     ticker_list = []
#     with open('spac_page.html', 'r', encoding="utf8") as f:
#         spac_page = f.read()

#     company_name = "x"
#     tickers = re.search('equities=.*logo',spac_page).group()
#     tickers = tickers.split('=')[1].split('&')[0].split('%3B')
#     ticker_list.extend(tickers)

#     company_list = [company_name]*len(tickers)

#     new_list = zip(company_list,ticker_list)

#     df = pd.DataFrame(new_list, columns=['Company Name','Ticker'])
#     print(df)

#     df = df.reindex(df.columns.tolist() + ['Price','Volume','Link'], axis=1)
#     print(df['Ticker'][0])

#     # art = yfinance.Ticker('ACAM')
#     # print(art.info['volume'])


# robinhood_url = 'https://robinhood.com/stocks/'
# ticker = 'CFFAU'

# new_url = robinhood_url + ticker
# r = requests.get(new_url).text
# print(r)
