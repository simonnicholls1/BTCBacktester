import pandas as pd
import numpy as np
import pandas_ta as ta


class EWMACrossover:

    def __init__(self, ticker, data_service,  short_window: int, long_window: int):
        self.short_window = short_window
        self.long_window = long_window
        self.ticker = ticker
        self.data_service = data_service

    def gen_signal(self, time_series_freq: str, time_limit: int, data_column='close'):
        """Returns the DataFrame of symbols containing the signals
        to go long, short or hold (1, -1 or 0)."""
        time_series_df = self.data_service.get_ticker_candles(self.ticker, time_series_freq, time_limit)
        signal = pd.DataFrame(index=time_series_df.index)
        signal['signal'] = 0.0
        signal['close'] = time_series_df['close']
        signal['open'] = time_series_df['open']

        # Create the set of short and long simple moving averages over the
        # respective periods
        signal['short_ewma'] = ta.ema(time_series_df[data_column], length=self.short_window, min_periods=1)
        signal['long_ewma'] = ta.ema(time_series_df[data_column], length=self.long_window, min_periods=1)

        # Create a 'signal' (invested or not invested) when the short moving average crosses the long
        # moving average, but only for the period greater than the shortest moving average window
        signal['signal'][self.short_window:] = np.where(signal['short_ewma'][self.short_window:]
                                                         > signal['long_ewma'][self.short_window:], 1.0, 0.0)

        # Take the difference of the signals in order to generate actual trading orders
        signal['positions'] = signal['signal'].diff()

        return signal
