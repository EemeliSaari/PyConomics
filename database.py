from datetime import date
import os
import sqlite3

import src.web_scraper as ws
import src.local as local
from src.utils import convert_date, string_to_date, name_stock_symbol


class DataBase:

    def __init__(self, db='database.db'):
        """
        Constructor for the class.

        :param db: database file name
        """
        self.__db = db

        if not os.path.exists(db):
            # Initialize the database connection, which creates the .db file as well
            self.__conn = sqlite3.connect(db, check_same_thread=False)
            self.__conn.row_factory = dict_factory
            # Enable the foreign keys
            self.__c = self.__conn.execute('pragma foreign_keys=ON')
            print("Database not found\nStarting initialize process...\n")
            self.build()

        self.__conn = sqlite3.connect(db, check_same_thread=False)
        self.__conn.row_factory = dict_factory
        self.__c = self.__conn.execute('pragma foreign_keys=ON')

        self.get_stock('ELISA')

    def __del__(self):
        """
        Deconstruct method for class. 
        Closes the connection to the database.
        """
        self.__c.close()
        self.__conn.close()

    def build(self):
        """
        Initialize the databse for omx nordic markets and companies.

        :param db_file: name of the database file
        """
        local_files = '.local/'

        markets, symbols_list = local.initialize_symbols(local_files)
        try:
            # Create the omx table containing all the market names
            self.__c.execute('''CREATE TABLE IF NOT EXISTS omx_nordic (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT, 
                updated TEXT)''')

            today = convert_date(str(date.today()))
            for data in zip(markets, symbols_list):
                market = data[0].lower()
                print(market)

                # New table for specific market
                self.__c.execute('''CREATE TABLE {:s} (
                    company_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT, 
                    symbol TEXT,
                    sector TEXT,
                    ICB INT,
                    market_id INT REFERENCES omx_nordic(id))'''.format(market))

                market_id = self.insert_market(market, today)
                company_data = data[1]

                # Iterate through symbols data
                for i in range(len(company_data[0]) - 1):
                    cd = []
                    for p in range(len(company_data)):
                        cd.append(company_data[p][i])
                    # Insert symbols data to the market table

                    stock_data = ws.get_price_yahoo(cd[1], market, today)
                    # will only insert a company if any data was available
                    if stock_data:
                        company_id = self.insert_company(market, (cd[0], cd[1], cd[2], int(cd[3]), market_id))
                        company_symbol = self.new_stock_table(cd[1], market)
                        self.insert_stock(company_symbol, stock_data)
                    else:
                        self.insert_unprocessed(cd[1], today)
            # Commit & close connections
            self.__conn.commit()

            print("...Ready")

        except sqlite3.OperationalError as e:
            self.__c.close()
            self.__conn.close()
            os.remove(self.__db)
            print("Error creating the database\n{}".format(e))

    def get_stock(self, symbol):
        """Queries the database for a given stock symbol"""
        symbol = "stock_" + name_stock_symbol(symbol, sep='_')

        return self.__c.execute('SELECT * FROM {:s}'.format(symbol)).fetchall()

    def new_stock_table(self, company_symbol, market):
        """
        Adds a new stock table to the database

        Table naming: 'stock_company_symbol' spaces separated with case "_".

        :param company_symbol:
        :param market:
        :return: company symbol in a table name format
        """
        symbol = "stock_" + name_stock_symbol(company_symbol, sep='_')
        print(symbol)
        self.__c.execute('''CREATE TABLE IF NOT EXISTS {:s} (
            date DATE, 
            open FLOAT,
            high FLOAT,
            low FLOAT,
            close FLOAT,
            adj_close FLOAT,
            volume BIGINT)'''.format(symbol))
        return symbol

    def insert_unprocessed(self, company_symbol, date):
        """
        Store unprocessed companies to specific table for further use.

        :param company_symbol:
        :param date: date of the attempted process
        """
        self.__c.execute('''CREATE TABLE IF NOT EXISTS unprocessed_companies (
            symbol TEXT,
            date DATE)''')
        self.__c.execute('''INSERT INTO unprocessed_companies VALUES (?, ?)''', (company_symbol, date))

    def insert_stock(self, company_symbol, data):
        """
        Insert a new stock entry

        :param company_symbol:
        :param data:
        """
        print(len(data))
        self.__c.executemany('''INSERT INTO {:s} VALUES(?, ?, ?, ?, ?, ?, ?)'''
                                .format(company_symbol), data)

    def insert_company(self, market, data):
        """
        Insert new company

        :param market:
        :param data:
        """
        symbol = data[1]
        self.__c.execute('''INSERT INTO {:s} (name, symbol, sector, ICB, market_id) VALUES(?, ?, ?, ?, ?)'''
                            .format(market), data)

        return self.__c.execute("SELECT company_id FROM {:s} WHERE symbol=?".format(market), (symbol,)).fetchone()[0]

    def insert_market(self, market, today):
        """
        Insert new market to omx_nordic

        :param market:
        :param today:
        """
        # Insert the market name and day which insertion was made
        self.__c.execute('''INSERT INTO omx_nordic (name, updated) VALUES ('{:s}', '{:s}')'''
                            .format(market, today))
        # Query for the id
        return self.__c.execute("SELECT id FROM omx_nordic WHERE name='{:s}'".format(market)).fetchone()[0]

def dict_factory(cursor, row):
    """Returns database rows in dict format instead of tuple"""

    data = {}
    for i, col in enumerate(cursor.description):
        data[col[0]] = row[i]
    return data
