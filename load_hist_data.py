import pandas as pd

import os
import requests

from datetime import datetime, timedelta, timezone
from util import my_print
import traceback

def rest(universe, start_date, end_date):
    """
    Fetch historical Kline candlestick data for multiple symbols between the start and end dates.

    Parameters
    ----------
    universe : list
        A list of symbols (e.g., ['BTCUSDT', 'ETHUSDT']) to fetch candlestick data for.
    start_date : datetime
        The start date for fetching historical data.
    end_date : datetime
        The end date for fetching historical data.

    Returns
    -------
    pd.DataFrame
        A pandas DataFrame containing the candlestick data with appropriate column names.
    """

    global_data = pd.DataFrame()
    rest_columns = ['Open time', 'Open', 'High', 'Low',
                    'Close', 'Volume', 'Close time',
                    'Quote asset volume', 'Number of trades',
                    'Taker buy base asset volume',
                    'Taker buy quote asset volume', 'Ignore']

    current_date = start_date

    # iterate over day as Binance returns max 1500 candlesticks per request
    while current_date <= end_date:
        for idx in range(len(universe)):
            try:
                symbol = universe[idx]

                req = 'https://fapi.binance.com'
                req += '/fapi/v1/klines'

                # Define the request parameters
                params = {'symbol': symbol,
                          'interval': '1m',
                          'limit': 1440,      # number of minutes in 24 hours
                          'startTime': to_milliseconds(current_date)}
                r = requests.get(req, params=params)
                j = r.json()

                assert type(j) is list, f'Error in symbol {symbol}'
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

        current_date += timedelta(days=1)

    return global_data

def to_milliseconds(dt):
    """ convert datetime to milliseconds """
    dt = dt.astimezone(timezone.utc)
    return int(dt.timestamp() * 1000)

def save_hist_data(df, start_date, end_date):
    """
    Save the DataFrame as a CSV file in the 'data/rest/historical_data/' directory,
    with subdirectories named based on the date range.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame containing the historical data to be saved.
    start_date : datetime
    end_date : datetime
    """
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
    """ read universe from json """
    with open(fname) as ifl:
        universe = eval(ifl.readline())
    return universe


if __name__ == '__main__':
    start_date = datetime(2024,8, 30, tzinfo=timezone.utc)
    end_date = datetime(2024,9, 1, tzinfo=timezone.utc)
    universe = get_universe('universe.json')

    df = rest(universe, start_date, end_date)
    save_hist_data(df, start_date, end_date)
