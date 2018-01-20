# Utility functions
from datetime import datetime as dt
from datetime import date
import time


def name_stock_ticker(ticker):

    parts = ticker.split(" ")
    if len(parts) > 1:
        ticker = "-".join(parts)
    else:
        ticker = ticker

    return ticker


def datestring_to_int(string_date):

    return int(time.mktime(dt.strptime(string_date, '%d.%m.%Y').timetuple()))

def convert_date(date):
    """
    Functio takes date in format '2017-01-24' and returns
    it in format '24.01.2017'
    """
    return dt.strptime(date,'%Y-%m-%d').strftime('%d.%m.%Y')

def get_today_datetime():

    return dt.combine(date.today(), dt.min.time())

def string_to_date(string_date):

    return dt.strptime(string_date, '%d.%m.%Y')

def convert_volume_format(string):
    """
    Converts volume
    """
    return int(string.replace(',','')) / 1000000
