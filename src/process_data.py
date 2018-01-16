from collections import Counter
import pickle
import numpy as np
import pandas as pd


def determination(*args):

    cols = [x for x in args]
    req = 0.02

    for col in cols:
        if col > req:
            return 1
        if col < -req:
            return -1
    return 0


def process_labels(symbol,location,dt):

    days = 5
    df = pd.read_csv('./.local/df_compiled/OMX_{:s}_joined_{:s}.csv'
                    .format(location,dt), index_col = 0)

    symbols = df.columns.values.tolist()
    df.fillna(0,inplace=True)

    for i in range(1, days+1):

        dr = df[symbol]
        df['{}_{}d'.format(symbol,i)] = (dr.shift(-i) - dr) / dr

    df.fillna(0,inplace=True)
    
    df['{:s}_target'.format(symbol)] = df.apply(lambda x: determination(x['{:s}_1d'.format(symbol)],
                                               x['{:s}_2d'.format(symbol)], 
                                               x['{:s}_3d'.format(symbol)],
                                               x['{:s}_4d'.format(symbol)],
                                               x['{:s}_5d'.format(symbol)]),axis=1)
    
    str_vals = [str(i) for i in df['{:s}_target'.format(symbol)].values.tolist()]
    print('Data spread:', Counter(str_vals))

    df.fillna(0, inplace=True)
    df = df.replace([np.inf, -np.inf], np.nan)
    df.dropna(inplace=True)

    df_vals = df[[s for s in symbols]].pct_change()
    df_vals = df_vals.replace([np.inf, -np.inf], 0)
    df_vals.fillna(0, inplace=True)

    X, y = df_vals.values, df['{:s}_target'.format(symbol)].values

    return X, y, df

#process_labels('YLEPS','helsinki','close')
