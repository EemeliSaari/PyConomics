from datetime import date
import os
import sqlite3

import src.web_scraper as ws
import src.local as local

def initialize():
    """Initialize routine"""

    db = 'database.db'
    if not os.path.exists(db):
        initialize_db(db)


def initialize_db(db_file):
    """
    Initialize the databse for omx nordic markets and companies.

    :param db_file: name of the database file
    """
    base = '.local/'
    if not os.path.exists(base):
        os.mkdir(base)

    markets, symbols_list = initialize_symbols(base)

    try:
        # Initialize the database connection, which creates the .db file as well
        conn = sqlite3.connect(db_file)
        # Enable the foreign keys
        c = conn.execute('pragma foreign_keys=ON')
        # Create the omx table containing all the market names
        c.execute('''CREATE TABLE omx (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                       name TEXT, 
                                       updated TEXT)''')

        for data in zip(markets, symbols_list):
            market = data[0]
            # Insert the market name and day which insertion was made
            c.execute("INSERT INTO omx (name, updated) VALUES ('{:s}', '{:s}')".format(market, str(date.today())))
            # Query for the id
            market_id = c.execute("SELECT id FROM omx WHERE name='{:s}'".format(market)).fetchone()[0]
            symbols_data = data[1]
            # New table for specific market
            c.execute('''CREATE TABLE {:s} (stock_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                            name TEXT, 
                                            symbol TEXT,
                                            sector TEXT,
                                            ICB INTEGER,
                                            market_id INTEGER REFERENCES omx(id))'''
                        .format(market))
            # Iterate through symbols data
            for i in range(len(symbols_data[0]) - 1):
                sym = []
                for p in range(len(symbols_data)):
                    sym.append(symbols_data[p][i])
                # Insert symbols data to the market table
                c.execute("INSERT INTO {:s} (name, symbol, sector, ICB, market_id)"
                            "VALUES('{:s}', '{:s}', '{:s}', {:s}, {:d})"
                                .format(market, sym[0], sym[1], sym[2], sym[3], market_id))
        # Commit & close connections
        conn.commit()
        c.close()
        conn.close()

    except sqlite3.OperationalError as e:
        c.close()
        conn.close()
        os.remove(db_file)
        print("Error creating the database\n{}".format(e))


def initialize_symbols(path):
    """
    Get the symbols for markets.

    :param path: path to local data
    """
    markets_data = ws.get_omx_markets()
    local.markets_to_pickle('OMX', markets_data, path)
    symbols = []
    for market in markets_data:
        symbols_data = ws.get_omx_data(market, 0, 1, 4, 5)

        symbols.append(symbols_data)
        local.symbols_to_pickle(symbols_data, market, path)

    return markets_data, symbols
