import codecs
import json
import re
from time import time

import bs4 as bs
import requests as req

from src.utils import datestring_to_int, name_stock_symbol


class YahooQuery:

    def __init__(self, symbol, market):

        self.__MARKETS = {
            "Helsinki" : ["HE"],
            "Stockholm" : ["ST"],
            "Baltic" : ["TL", 'RG', 'VS'],
            "Copenhagen" : ["CO"],
            "Iceland" : ["L", "IC"]
        }

        self.__symbol = name_stock_symbol(symbol)
        self.__market = market

    def get_crumb(self):
        """
        Parses the http request for crumb and cookies

        :return: crumb, cookies, working stock symbol
        """
        for padding in self.__MARKETS[self.__market]:
            
            symbol = ".".join([self.__symbol, padding])
            URL = "https://finance.yahoo.com/quote/{:s}/history".format(symbol)
            try:
                res = req.get(URL)
                cookies = res.cookies['B']
                # Fetch the crump from cookies with regex
                pattern = re.compile('.*"user":\{"crumb":"(?P<crumb>[^"]+)"\,')
                crumb = self.parse_crumb([pattern.match(x).groupdict()['crumb'] for x in res.text.splitlines() if pattern.match(x)][0])
                return crumb, cookies, symbol

            except KeyError:
                pass

    def parse_crumb(self, raw_crumb):
        """
        Decode the raw_crumb
        """
        return str(codecs.decode(raw_crumb, 'unicode-escape'))

    def get_historic(self, end, interval, start=None):
        """
        Yahoo query for historic stock price

        :param start: starting date as string format('%d.%m.%Y'),
                      default(None), will return the max
        :param end: end date as string format('%d.%m.%Y')
        :param interval: interval for search, available: [1d, 1wk, 1mo]
        """
        try:
            URL = 'https://query1.finance.yahoo.com/v7/finance/download/{:s}'.format(self.__symbol)

            crumb, cookies, symbol = self.get_crumb()

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
            if self.check_errors(resp.text):
                return resp.text

        except TypeError:
            pass

        except req.exceptions.ContentDecodingError:
            pass
        
        return None

    def check_errors(self, response):
        """
        Check the response for any errors
        """
        # Errors are represented in JSON fromat
        try:
            js = json.loads(response)
            print(js)
            return False
        # In case of failure we know that there was no error
        except json.decoder.JSONDecodeError:
            return True
