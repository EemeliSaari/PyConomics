from datetime import date
import os
import sqlite3

import src.web_scraper as ws
import src.local as local
from src.utils import convert_date, string_to_date


class DataBase:

    def __init__(self, db='database.db'):

        self.__db = db

        if not os.path.exists(db):
            # Initialize the database connection, which creates the .db file as well
            self.__conn = sqlite3.connect(db)
            # Enable the foreign keys
            self.__c = self.__conn.execute('pragma foreign_keys=ON')
            print("Database not found\nStarting initialize process...\n")
            self.build()

        self.__conn = sqlite3.connect(db)
        self.__c = self.__conn.execute('pragma foreign_keys=ON')

    def __del__(self):
        
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
            self.__c.execute('''CREATE TABLE IF NOT EXISTS omx_nordic (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                                        name TEXT, 
                                                                        updated TEXT)''')
            today = convert_date(str(date.today()))
            for data in zip(markets, symbols_list):
                market = data[0]
                # New table for specific market
                self.__c.execute('''CREATE TABLE {:s} (company_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                        name TEXT, 
                                                        symbol TEXT,
                                                        sector TEXT,
                                                        ICB INT,
                                                        market_id INT REFERENCES omx_nordic(id))'''
                                                .format(market))

                market_id = self.insert_market(market, today)
                company_data = data[1]

                # Iterate through symbols data
                for i in range(len(company_data[0]) - 1):
                    cd = []
                    for p in range(len(company_data)):
                        cd.append(company_data[p][i])
                    # Insert symbols data to the market table
                    company_id = self.insert_company(market, (cd[0], cd[1], cd[2], int(cd[3]), market_id))
                    print(company_id)
                    self.new_stock_table(cd[1], market)
                    stock_data = ws.get_price_yahoo(cd[1], market, today)
                    #print(stock_data)

                    #self.insert_stock(cd[0], stock_data)
                    #self.insert_stock()
            # Commit & close connections
            self.__conn.commit()

            self.__c.close()
            self.__conn.close()
            print("...Ready")
            #os.remove(self.__db)

        except sqlite3.OperationalError as e:
            self.__c.close()
            self.__conn.close()
            os.remove(self.__db)
            print("Error creating the database\n{}".format(e))

    def new_stock_table(self, company_symbol, market):

        print(market)
        print(company_symbol)

        symbol = "stock_" + symbol
        self.__c.execute('''CREATE TABLE IF NOT EXISTS {:s} (date DATE, 
                                                            open FLOAT,
                                                            high FLOAT,
                                                            low FLOAT,
                                                            close FLOAT,
                                                            volume BIGINT)'''
                                .format(symbol))

    def insert_stock(self, company_symbol, data):

        self.__c.execute('''INSERT INTO {:s} VALUES(?, ?, ?, ?, ?, ?, ?)'''
                            .format(company_symbol), data)

    def insert_company(self, market, data):
        symbol = data[1]
        print(symbol)
        self.__c.execute('''INSERT INTO {:s} (name, symbol, sector, ICB, market_id) VALUES(?, ?, ?, ?, ?)'''
                        .format(market), data)

        return self.__c.execute("SELECT company_id FROM {:s} WHERE symbol=?".format(market), (symbol,)).fetchone()[0]

    def insert_market(self, market, today):
        # Insert the market name and day which insertion was made
        self.__c.execute('''INSERT INTO omx_nordic (name, updated) VALUES ('{:s}', '{:s}')'''
                            .format(market, today))
        # Query for the id
        return self.__c.execute("SELECT id FROM omx_nordic WHERE name='{:s}'".format(market)).fetchone()[0]
