import matplotlib.pyplot as plt
from matplotlib import style

import numpy as np
import pandas as pd

style.use('ggplot')


def simple_graph(symbol, path):
    """
    One line graph for stock closed prices.

    :param symbol: stocks symbol
    :param path: 
    """

    df = pd.read_csv(path)
    data = df[['date', symbol]]
    print(data.head())
    plt.plot_date(df['date'], df[symbol], '-', label='Price')

    plt.xlabel('Date')
    plt.ylabel('Price')

    plt.tight_layout()
    plt.show()


def decent_graph(symbol):
    """
    Graph of closed prices - 100ma - volume.

    :param symbol: symbol for stock.
    """
    
    # path for the .csv file of the company
    path = './.local/df_stock_csv/' + symbol + ".csv"
    
    df = pd.read_csv(path, parse_dates=True, index_col=0)

    #creating a new column 100days moving average
    df['100ma'] = df['close'].rolling(window=100, min_periods=0).mean()

    ax1 = plt.subplot2grid((6, 1), (0, 0), rowspan=5, colspan=1)
    ax2 = plt.subplot2grid((6, 1), (5, 0), rowspan=5, colspan=1, sharex=ax1)

    ax1.plot(df.index, df['close'], '-', label='Closed')
    ax1.plot(df.index, df['100ma'], '-', label='100ma')
    ax2.bar(df.index, df['volume'])
    
    start = df.index[len(df.index) - 1]
    end = df.index[0]
    
    ax1.set_xlim(xmin=start, xmax=end)
    
    plt.tight_layout()

    plt.show()


def correlation_table(market, column):
    """
    Correlation heatmap table plotted from the compiled data set.

    :param market: market location for example: helsinki
    :param column: column that the data was compiled with: high, close, etc.
    """
    path = './.local/df_compiled/OMX_{}_joined_{}.csv'.format(market, column)
    
    df = pd.read_csv(path)

    df_corr = df.corr()

    data = df_corr.values
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    heathmap = ax.pcolor(data, cmap=plt.cm.RdYlGn)
    fig.colorbar(heathmap)

    ax.set_xticks(np.arange(data.shape[0]) + 0.5, minor=False)
    ax.set_yticks(np.arange(data.shape[1]) + 0.5, minor=False)

    ax.invert_yaxis()
    ax.xaxis.tick_top()

    column_labels = df_corr.columns
    row_labels = df_corr.index

    ax.set_xticklabels(column_labels)
    ax.set_yticklabels(row_labels)

    plt.xticks(rotation=90)
    heathmap.set_clim(-1, 1)

    plt.tight_layout()
    plt.show()

#correlation_table('helsinki','close')
#simple_graph('ELISA','./.local/df_compiled/OMX_helsinki_joined_close.csv')
#decent_graph('PIZZA')
