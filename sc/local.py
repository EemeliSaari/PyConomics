import os
from scrap_google import data_frame
from datetime import datetime as dt
import pandas as pd
import web_scraper 
import pickle


# Saves the mined data into a .pickle dumps for further use


def get_symbols(location, dpath):
    """
    Gets symbol list and saves it to pickle dump

    :param location: market location, helsinki, iceland, stockholm etc.
    :param dpath: directory path that pickle dump is saved into.
    """
    target = 'OMX_{:s}_symbols.pickle'.format(location)
    
    if not os.path.exists(dpath + target):    
        with open((dpath + target),'wb') as f:
            pickle.dump(web_scraper.get_omx(location),f)

def get_df(location, target_path, symbol_path, startdate, enddate):
    """
    Saves the panda dataframe acquired from Googles Finance history search
    into a pickle dump for local usage so we don't have to do heavy processing
    power required work everytime.

    :param location: markets location, helsinki, iceland, stockholm etc.
    :param target_path: saving location
    :param symbol_path: path for symbol dump
    :param startdate: list history from startdate
    :param enddate: list history to enddate
    """
    m = {'helsinki':'HEL'}
    symbols = 'OMX_{:s}_symbols.pickle'.format(location)
    
    with open((symbol_path + symbols),'rb') as symbol_file:
        symbols_list = pickle.load(symbol_file)
    
    for symbol in symbols_list: 

        if not os.path.exists(target_path+symbol+'.pickle'):
            df = data_frame(symbol, startdate, enddate, market=m[location])

            with open(target_path+symbol+'.pickle','wb') as f:
                pickle.dump(df,f)
        else:
            print('Already have it')


def convert_date(date):

    return dt.strptime(date,'%b %d, %Y').strftime('%Y-%m-%d')


def compile_data(market,column,symbols_path,df_path,target_path=None):
    """

    :param market: to specify saved file
    :param column: [date,open,high,low,close,volume]
    :param symbols_path: path for symbols
    :param df_path: path for stock data frames
    :param target_path: path to save compiled data into
    """

    symbols_file = symbols_path + 'OMX_{:s}_symbols.pickle'.format(market)

    with open(symbols_file,'rb') as f:
        symbols_list = pickle.load(f)

    if not os.path.exists('./.local/df_compiled'):
        os.mkdir('./.local/df_compiled')

    new_df = pd.DataFrame()

    for count, symbol in enumerate(symbols_list):
        with open(df_path + symbol + '.pickle', 'rb') as f:
            df = pickle.load(f)
        
        df['date'] = df['date'].apply(convert_date)
        df.set_index('date',inplace=True)
        
        df.drop(['open','high','low','volume'], 1, inplace=True)
        df.rename(columns = {column: symbol}, inplace=True)
        
        if new_df.empty:
            new_df = df
        else:
            new_df =  new_df.join(df,how='outer')

        if count % 10 == 0:
            print(count)

    print(new_df.head())
    new_df.to_csv('./.local/df_compiled/OMX_{:s}_joined_{:s}.csv'.format(market,column))