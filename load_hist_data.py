import pandas as pd
import numpy as np

import sys, os, time
import requests

from datetime import datetime
from util import my_print
import traceback

def rest(universe, start_date, end_date):
    # add start date and end date
    # add python types
    s_time = int(start_date.timestamp()) * 1000
    e_time = int(end_date.timestamp()) * 1000

    global_data = pd.DataFrame()
    rest_columns = ['Open time', 'Open', 'High', 'Low',
                    'Close', 'Volume', 'Close time',
                    'Quote asset volume', 'Number of trades',
                    'Taker buy base asset volume',
                    'Taker buy quote asset volume', 'Ignore']

    for idx in range(len(universe[:3])):
        try:
            symbol = universe[idx]

            req = 'https://fapi.binance.com'
            req += '/fapi/v1/klines'
            params = {'symbol': symbol, 'interval': '1m', 'startTime': s_time}
            r = requests.get(req, params=params)
            # print(r.headers)
            j = r.json()

            assert type(j) == list, f'Error in symbol {symbol}'
            assert len(j) > 0, f'No data for symbol {symbol}'
            assert len(j[0]) == len(rest_columns), f'Error in number of features'


            df = pd.DataFrame(j, columns=rest_columns)

            df['Open time'] = pd.to_datetime(df['Open time'], unit='ms')
            df['Close time'] = pd.to_datetime(df['Close time'], unit='ms')
            df['symbol'] = symbol

            if global_data.shape[0] == 0:
                global_data = df
            else:
                global_data = pd.concat([global_data, df], axis=0, ignore_index=True)

        except Exception as e:
            traceback.print_exc()
            my_print(str(e))

    return global_data


def save_hist_data(df, start_date, end_date):
    root = 'data/rest/historical_data/'
    s_date = start_date.strftime('%Y%m%d')
    e_date = end_date.strftime('%Y%m%d')

    dirname = root + s_date + '_' + e_date + '/'
    print(dirname)

    if not os.path.exists(dirname):
        os.makedirs(dirname)
    path = dirname + 'data.csv'
    df.to_csv(path, index=False)

def get_universe(fname):
    with open(fname) as ifl:
        universe = eval(ifl.readline())
    return universe


if __name__ == '__main__':
    start_date = datetime(2024,8, 30)
    now = datetime.now()
    universe = get_universe('universe.json')

    df = rest(universe, start_date, now)
    save_hist_data(df, start_date, now)








