import pickle
from collections import Counter

import numpy as np
import pandas as pd

from database import DataBase


class DataSet:

    def __init__(self, symbol, db):

        self.__raw = [list(x.values())[0] for x in db.get_stock(symbol, column='close')]

        print(self.__raw)

def process_naive(symbol, db, num_steps, input_size):

    X = []
    y = []
    DataSet(symbol, db)
    data = db.get_stock(symbol)

    for n, row in enumerate(data[1:len(data)-1]):
        X.append(row['close'])
        y.append(data[n+1]['close'])
    seq = [np.array(X[i * input_size: (i + 1) * input_size]) for i in range(len(X) // input_size)]
    #print(seq)
    return np.array(X), np.array(y)
