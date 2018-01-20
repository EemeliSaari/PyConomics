from datetime import date
import sqlite3

from src.utils import string_to_date, get_today_datetime

def check_date_routine(database='database.db', market='omx'):

    today = get_today_datetime()

    conn = sqlite3.connect(database)
    c = conn.cursor()

    for row in c.execute("SELECT * FROM {:s}".format(market)):

        print(row)
        if string_to_date(row[2]) < today:
            print('ha')
            update_markets(c)


def update_markets(cursor):
    #TODO
    pass

def check_db_date(df, date):
    #TODO check the that the db is up to date.
    pass