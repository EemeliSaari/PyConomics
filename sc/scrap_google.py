import pandas as pd
import requests
import bs4 as bs


def data_frame(symbol, startdate, enddate, market='HEL'):
    """
    Converts a scrapped list from Google's Finance history 
    page to a panda data set for further use.

    :param symbol: ticker of the stock company
    :param startdate: start date of the data frame
    :param enddate: end date for the data frame
    :param market: market that we're using available:HEL (default)
                                                     ---
    :return: .csv file of the given stock symbol in the following format: 
                                        header=date;open;high;low;close;volume
    """
    i = 0
    rows = 200
    data = []
    loop = True
    while loop:
        try:
            url = 'https://www.google.com/finance/historical?q={:s}%3A{:s}&startdate={:s}&enddate={:s}&start={:d}&num={:d}'.format(market, symbol, startdate, enddate, i, rows)
            response = requests.get(url)
            soup = bs.BeautifulSoup(response.text,'lxml')
            
            table = soup.find('table',{'class':'gf-table historical_price'})
            
            for head in table.findAll('tr')[1:]:
                date = [head.find('td', {'class':'lm'}).text.strip()]

                rest = []
                for p in head.findAll('td', {'class':'rgt'}): 
                    rest.append(p.text.strip())
                
                data.append(date + rest)

            i += 200

        except AttributeError:
            loop = False
            
    header = ['date', 'open', 'high', 'low', 'close', 'volume']

    return pd.DataFrame(data=data, columns=header)