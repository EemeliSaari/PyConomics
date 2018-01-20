import re
from time import time

import bs4 as bs
import requests as req

from src.utils import datestring_to_int


class YahooQuery:

    def __init__(self, symbol, market):

        self.__MARKETS = {
            "Helsinki" : "HE",
            "Stockholm" : "ST",
            "Baltic" : "TL",
            "Copenhagen" : "CO",
            "Iceland" : "L"
        } # TODO add rest of the markets

        self.__symbol = symbol
        self.__market = market

    def get_crumb(self, base):

        res = req.get(base)
        cookies = res.cookies['B']
        # Fetch the crump from cookies with regex
        pattern = re.compile('.*"CrumbStore":\{"crumb":"(?P<crumb>[^"]+)"\}')
        return [pattern.match(x).groupdict()['crumb'] for x in res.text.splitlines() if pattern.match(x)][0], cookies

    def get_historic(self, start, end, interval):

        symbol = ".".join([self.__symbol, self.__MARKETS[self.__market]])

        URL = 'https://query1.finance.yahoo.com/v7/finance/download/{:s}'.format(self.__symbol)

        crumb, cookies = self.get_crumb("https://finance.yahoo.com/quote/{:s}/history".format(symbol))
        if start:
            start = datestring_to_int(start)
        else:
            start = 0

        params = {
            'symbol' : symbol,
            'period1' : start,
            'period2' : datestring_to_int(end),
            'interval' : interval,
            'crumb' : crumb
        }
        cookies = {
            'B' : cookies
        }

        resp = req.get(URL, params=params, cookies=cookies)
        self.parse_errors(resp)

        return resp.text

    def parse_errors(response):
        #TODO check for errors
        print(response.splitlines()[0])
        pass
