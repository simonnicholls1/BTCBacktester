import ccxt
import pandas as pd

class BinanceDAO():

    def __init__(self):
        self.binance_conn = ccxt.binance()

    def get_ticker_candles(self, ticker_name: str, freq='1m', limit=100):
        btc_usdt_candles = self.binance_conn.fetch_ohlcv(ticker_name, freq, limit)
        df = pd.DataFrame(btc_usdt_candles, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('datetime', inplace=True)
        return df