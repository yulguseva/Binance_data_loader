# Binance_data_loader
Load historical and real live trading data from Binance.

The data used in code is retrieving historical Kline/Candlestick Data for USD-M Futures on all symbols (cryptocurrencies) listed in the universe.json file.

More information about Kline/Candlestick Data for USD-M Futures on Binance site: https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Kline-Candlestick-Data .


## Features

- **Historical Data**: Retrieve historical Kline/Candlestick data for USD-M Futures on all symbols listed in the `universe.json` file. Binance provides historical data for Kline/Candlestick for the entire available history.
- **Real-Time Data**: Fetch live trading data for the same symbols.
- **Data Storage**: Optionally store the fetched data in a format suitable for further analysis or processing.

