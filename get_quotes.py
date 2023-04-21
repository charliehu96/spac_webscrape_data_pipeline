from bs4 import BeautifulSoup
import requests
import csv
import re
import pandas as pd
from iexfinance.stocks import Stock

CSV_NAME = 'sample.csv'
API_TOKEN = 'sk_0ab21fe164844d71b254935ad8aef6d2'

def main():
    df = pd.read_csv(CSV_NAME)
    df = get_realtime_quotes(df)
    df = get_historic_quotes(df)
    print(df)
    write_to_csv(df)
    

def get_historic_quotes(df):
    ticker_list = ','.join(df['Ticker'])
    params = {
        "token": API_TOKEN,
        "types": "chart",
        "range": "6m",
        "symbols": ticker_list
    }
    r = requests.get(f'https://cloud.iexapis.com/stable/stock/market/batch', params=params).json()
    yesterday_price_list = []
    yesterday_volume_list = []
    five_day_price_list = []
    five_day_volume_list = []
    thirty_day_price_list = []
    thirty_day_volume_list = []
    six_month_price_list = []
    six_month_volume_list = []

    for ticker in df['Ticker']:
        # print(ticker)
        try:
            yesterday_price_list.append(r[ticker]['chart'][-1]['close'])
            yesterday_volume_list.append(r[ticker]['chart'][-1]['volume'])

            five_day_price_hold = []
            for date in r[ticker]['chart'][-5:]:
                five_day_price_hold.append(date['close'])
            five_day_price_list.append(sum(five_day_price_hold) / len(five_day_price_hold))

            five_day_volume_hold = []
            for date in r[ticker]['chart'][-5:]:
                five_day_volume_hold.append(date['volume'])
            five_day_volume_list.append(sum(five_day_volume_hold) / len(five_day_volume_hold))

            thirty_day_price_hold = []
            for date in r[ticker]['chart'][-20:]:
                thirty_day_price_hold.append(date['close'])
            thirty_day_price_list.append(sum(thirty_day_price_hold) / len(thirty_day_price_hold))

            thirty_day_volume_hold = []
            for date in r[ticker]['chart'][-20:]:
                thirty_day_volume_hold.append(date['volume'])
            thirty_day_volume_list.append(sum(thirty_day_volume_hold) / len(thirty_day_volume_hold))

            six_month_price_hold = []
            for date in r[ticker]['chart']:
                six_month_price_hold.append(date['close'])
            six_month_price_list.append(sum(six_month_price_hold) / len(six_month_price_hold))

            six_month_volume_hold = []
            for date in r[ticker]['chart']:
                six_month_volume_hold.append(date['volume'])
            six_month_volume_list.append(sum(six_month_volume_hold) / len(six_month_volume_hold))

        except:
            yesterday_price_list.append(None)
            yesterday_volume_list.append(None)
            five_day_price_list.append(None)
            five_day_volume_list.append(None)
            thirty_day_price_list.append(None)
            thirty_day_volume_list.append(None)
            six_month_price_list.append(None)
            six_month_volume_list.append(None)


    df['Yesterday Price'] = yesterday_price_list
    df['Yesterday Volume'] = yesterday_volume_list
    df['5 Day Avg Price'] = five_day_price_list
    df['% Change from 5 Day Avg Price'] = ((df['Yesterday Price'] - df['5 Day Avg Price']) / df['5 Day Avg Price']) * 100
    df['5 Day Avg Volume'] = five_day_volume_list
    df['% Change from 5 Day Avg Volume'] = ((df['Yesterday Volume'] - df['5 Day Avg Volume']) / df['5 Day Avg Volume']) * 100
    df['30 Day Avg Price'] = thirty_day_price_list
    df['% Change from 30 Day Avg Price'] = ((df['Yesterday Price'] - df['30 Day Avg Price']) / df['30 Day Avg Price']) * 100
    df['30 Day Avg Volume'] = thirty_day_volume_list
    df['% Change from 30 Day Avg Volume'] = ((df['Yesterday Volume'] - df['30 Day Avg Volume']) / df['30 Day Avg Volume']) * 100
    df['6 Month Avg Price'] = six_month_price_list
    df['% Change from 6 Month Avg Price'] = ((df['Yesterday Price'] - df['6 Month Avg Price']) / df['6 Month Avg Price']) * 100
    df['6 Month Avg Volume'] = six_month_volume_list
    df['% Change from 6 Month Avg Volume'] = ((df['Yesterday Volume'] - df['6 Month Avg Volume']) / df['6 Month Avg Volume']) * 100
    return df

def get_realtime_quotes(df):
    ticker_list = ','.join(df['Ticker'])
    params = {
        "token": API_TOKEN,
        "types": "quote",
        "symbols": ticker_list
    }

    r = requests.get(f'https://cloud.iexapis.com/stable/stock/market/batch', params=params).json()
    # print(r)
    price_list = []
    volume_list = []
    marketcap_list = []
    avgvolume_list = []
    try:
        for ticker in df['Ticker']:
            price_list.append(r[ticker]['quote']['latestPrice'])
            volume_list.append(r[ticker]['quote']['volume'])
            marketcap_list.append(r[ticker]['quote']['marketCap'])
            avgvolume_list.append(r[ticker]['quote']['avgTotalVolume'])
    except:
        price_list.append(None)
        volume_list.append(None)
        marketcap_list.append(None)
        avgvolume_list.append(None)

    print(volume_list)
    df['Price'] = price_list
    df['Volume'] = volume_list
    df['MarketCap'] = marketcap_list
    df['AvgVolume'] = avgvolume_list

    return df

def write_to_csv(df):
    df.to_csv(r'spac_quotes.csv', index=False)

def get_quotes_robinhood(df):
    robinhood_url = 'https://robinhood.com/stocks/'
    price_list = []
    volume_list = []
    url_list = []

    for ticker in df['Ticker']:
        try:
            stock_url = robinhood_url + ticker
            r = requests.get(stock_url).text
            price = re.search('Market Price.*Commi', r).group().split('$')[1].split('<')[0]
            volume = re.search('Volume.*52 Week High', r).group().split('Volume')[2].split('>')[4].split('<')[0]

            price_list.append(price)
            volume_list.append(volume)
            url_list.append(stock_url)
        except: 
            # print(e)
            price_list.append(None)
            volume_list.append(None)
            url_list.append(None)
        
    df['Price'] = price_list
    df['Volume'] = volume_list
    df['Link'] = url_list

    return df


if __name__ == '__main__':
    main()  