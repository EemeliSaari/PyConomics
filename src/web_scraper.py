import bs4 as bs
import pandas as pd
import requests
import pandas_datareader.data as web
from time import sleep
from datetime import datetime, date
from src.queries import YahooQuery

def get_price_yahoo(symbol, market, enddate, startdate='01.01.2018'):
    """
    """
    yahoo = YahooQuery(symbol, market)
    raw = yahoo.get_historic(startdate, enddate, '1d')
    sleep(0.5)
    
    #print(raw)


def get_price_google(symbol, startdate, enddate, market='HEL', time_out=0):
    """
    Converts a scrapped list from Google's Finance history 
    page to a panda data set for further use.

    *NOTE* THIS FUNCTION ONLY WORKS IN SPECIFIC NETWORK CONDITIONS
    WHERE GOOGLE'S RECAPTCHA WON'T DETECT THE AUTOMATED QUERIES 

    :param symbol: ticker of the stock company
    :param startdate: start date of the data frame
    :param enddate: end date for the data frame
    :param market: market that we're using available:HEL (default)
    :param time_out: if process needs to wait a brief amount of time between each request
    :return: a pandas DataFrame that is in a format: 
                header= [date;open;high;low;close;volume]
    """
    i = 0
    rows = 200
    data = []
    while True:
        try:
            url = 'https://www.google.com/finance/historical?q={:s}%3A{:s}&startdate={:s}&enddate={:s}&start={:d}&num={:d}'.format(market, symbol, startdate, enddate, i, rows)
            response = requests.get(url)
            soup = bs.BeautifulSoup(response.text, 'lxml')
            # Scrap the response 
            table = soup.find('table', {'class':'gf-table historical_price'})
            
            for head in table.findAll('tr')[1:]:
                date = [head.find('td', {'class':'lm'}).text.strip()]

                rest = []
                for p in head.findAll('td', {'class':'rgt'}): 
                    rest.append(p.text.strip())

                data.append(date + rest)

            i += rows

        except AttributeError:
            break

    header = ['date', 'open', 'high', 'low', 'close', 'volume']

    return data, header


def get_omx_markets():
    """Scrapes the information about the omx nordic markets."""

    url = 'http://www.nasdaqomxnordic.com/shares/listed-companies/nordic-large-cap'
    response = requests.get(url)
    soup = bs.BeautifulSoup(response.text, 'lxml')

    table = soup.find('article', {'class':'nordic-article'})
    raw = [x.find_all('a')[0].text.split(' ') for x in table.find_all('li') if x.find_all('a', href=True)]

    return([x[1] for x in raw if 'Nasdaq' in x and len(x) == 2])


def get_omx_data(market, *targets):
    """
    Scrapes a Nasdq Nordic website based on markets location and searched attribute.

    :param market:
    :param target: attribute we're looking for: 0 = name
                                                1 = symbol (default)
                                                2 = currency
                                                3 = ISIN
                                                4 = sector
                                                5 = sector code
                                                6 = fact sheet (pdf file)
    :return:list of target attributes
    """
    try:
        url = 'http://www.nasdaqomxnordic.com/shares/listed-companies/{:s}'.format(market)
        response = requests.get(url)
        soup = bs.BeautifulSoup(response.text, 'lxml')

        table = soup.find('table', {'class':'tablesorter'}) 
        if targets:
            data = []
            for t in targets:
                data.append([row.findAll('td')[t].text for row in table.findAll('tr')[1:]])

            return data
        else:
            return [row.findAll('td')[1].text for row in table.findAll('tr')[1:]]

    except AttributeError:
        raise AttributeError('Error in the scraping process.')
