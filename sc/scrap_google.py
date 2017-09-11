import pandas as pd
import requests
import bs4 as bs


def scrapper(symbol,startdate,enddate,loc='HEL',rows=200):
    """
    Scrapes Google's finance history page.

    :param symbol: ticker of the stock company
    :param startdate: list history from startdate
    :param enddate: list history to enddate
    :param loc: markets ticker
    :param rows: the amount of rows to be pulled at the same time

    :return: list rows containing [date,open,high,low,close,volume]
    """
    i = 0
    data = []
    state = True
    while state:
        try:
            url = 'https://www.google.com/finance/historical?q={:s}%3A{:s}&startdate={:s}&enddate={:s}&start={:d}&num={:d}'.format(loc,symbol,startdate,enddate,i,rows)
            response = requests.get(url)
            soup = bs.BeautifulSoup(response.text,'lxml')
            
            table = soup.find('table',{'class':'gf-table historical_price'})
            
            for head in table.findAll('tr')[1:]:
                date = [head.find('td',{'class':'lm'}).text.strip()]

                rest = []
                for p in head.findAll('td',{'class':'rgt'}): 
                    rest.append(p.text.strip())
                
                data.append(date+rest)

            i += 200

        except AttributeError:
            state = False
            return data


def data_frame(symbol,startdate,enddate):
    """

    :param symbol:
    :param startdate:
    :param enddate:
    
    :return: .csv file of of the given stock symbol with 
                    header=date;open;high;low;close;volume
    """
    header = ['date','open','high','low','close','volume']
    data = scrapper(symbol,startdate,enddate)

    return pd.DataFrame(data=data,columns=header)