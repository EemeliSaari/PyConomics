from datetime import datetime as dt
import pickle

# Utility functions


def convert_date(date):
    """
    Functio takes date in format 'Feb 1, 2017' and returns
    it in format '2017-1-1'
    """
    return dt.strptime(date,'%b %d, %Y').strftime('%Y-%m-%d')


def conver_volume_format(string):
    """
    Converts volume
    """
    return int(string.replace(',','')) / 1000000
