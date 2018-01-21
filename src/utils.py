# Utility functions
from datetime import datetime as dt
from datetime import date
import time


def name_stock_symbol(symbol, sep='-'):
    """
    Function takes stock symbol, separates spaces and replaces with separator
    """
    parts = symbol.split(" ")
    if len(parts) > 1:
        symbol = sep.join(parts)

    return symbol

def parse_null(str_list):
    """
    Parse string list for null entries
    """
    return [row for row in str_list if 'null' not in row.split(',')[0:len(row.split(','))]]


def datestring_to_int(string_date):
    """
    Converts datestring to int
    """
    return int(time.mktime(dt.strptime(string_date, '%d.%m.%Y').timetuple()))

def convert_date(date):
    """
    Functio takes date in format '2017-01-24' and returns
    it in format '24.01.2017'
    """
    return dt.strptime(date,'%Y-%m-%d').strftime('%d.%m.%Y')

def get_today_datetime():
    """
    Function returns today as a datetime object
    """
    return dt.combine(date.today(), dt.min.time())

def string_to_date(string_date):
    """
    Convert string to datetime object
    """
    return dt.strptime(string_date, '%d.%m.%Y')

def convert_volume(string):
    """
    Converts volume
    """
    if string != 'null':
        return int(string.replace(',',''))
    else:
        return 0