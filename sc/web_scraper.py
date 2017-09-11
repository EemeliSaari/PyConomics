import bs4 as bs
import requests


def get_omx(location,target=1):
    """
    Scrapes a Nasdq Nordic website based on markets location and searched attribute.

    :param location: Markets based on the Nasdaq nordic. Example: helsinki or iceland
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
        url = 'http://www.nasdaqomxnordic.com/shares/listed-companies/'
        response = requests.get(url + location)
        soup = bs.BeautifulSoup(response.text,'lxml')

        table = soup.find('table', {'class':'tablesorter'}) 

        return [row.findAll('td')[target].text for row in table.findAll('tr')[1:]]
    
    except AttributeError:
        return False