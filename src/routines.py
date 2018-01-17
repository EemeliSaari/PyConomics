from datetime import date
import sqlite3


def check_date_routine(database='database.db', market='omx'):

    today = date.today()

    conn = sqlite3.connect(database)
    c = conn.cursor()

    for row in c.execute("SELECT updated FROM {:s}".format(market)):
        
        if row[0] != today:
            update_markets(c)


def update_markets(cursor):
    #TODO
    pass

def check_db_date(df, date):
    #TODO check the that the db is up to date.
    pass