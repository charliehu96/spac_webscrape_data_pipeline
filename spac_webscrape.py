from bs4 import BeautifulSoup
import requests
import csv
import re
import pandas as pd

USERNAME='anthony-nie@hotmail.com'
PASSWORD='CoaseTheorem'
login_url = 'https://spacinsider.com/my-account/'
spac_url = 'https://spacinsider.com/spac-profiles/'

    
def main():
    with requests.Session() as c:
        authentication(c)

        spac_list = retrieve_list_of_spac(c)
        df = pd.DataFrame(spac_list, columns=['Company Name','Ticker'])
        write_to_csv(df)


    # df = df.reindex(df.columns.tolist() + ['Price','Volume','Link'], axis=1)
    # df = get_quotes(df)
    
    


def authentication(c):
        #Authentication to login to website
        initial = c.get(login_url).text
        cookie = re.search('woocommerce-login-nonce.+input', initial).group()
        cookie = cookie.split('value')[1].split('"')[1]

        login_data = {
            'username': USERNAME, 
            'password': PASSWORD, 
            '_wp_http_referer': '/my-account/', 
            'login': 'Log in', 
            'woocommerce-login-nonce': cookie
        }
        headers = {'referer': 'https://spacinsider.com/my-account/'}
        c.post(login_url, data=login_data, headers=headers)

def retrieve_list_of_spac(c):
    print('Beginning webscrape to retrieve list of SPAC companies')
    ticker_list = []
    company_list = []
    #Request web page with spac list
    page = c.get(spac_url).text

    #Webscrape of list of spacs to get individual spac page
    soup = BeautifulSoup(page, 'lxml')
    for tr in soup.find_all('tr'):
        try:
            if(tr.td.a.text) == '<':
                continue
            #Retrieve spac company name
            company_name = tr.td.a.text
            
            #Retrieve spac company website link
            company_link = tr.td.a.get('href')
            company_page = c.get(company_link).text

            #Retrieve tickers from spac company website link
            tickers = re.search('equities=.*logo', company_page).group()
            tickers = tickers.split('=')[1].split('&')[0].split('%3B')

            #Writes tickers and company names for one spac page into lists
            ticker_list.extend(tickers)
            company_list.extend([company_name]*len(tickers))
            # print(ticker_list)
        except:
            pass

    print('Completed webscrape')
    return zip(company_list,ticker_list)


def write_to_csv(df):
    df.to_csv(r'spac_list.csv', index=False)


def get_quotes(df):
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