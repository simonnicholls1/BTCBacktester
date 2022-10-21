import matplotlib.pyplot as plt


class Plotter:

    def plot_strategy(self, signal):
        
        plt.figure(figsize=(20, 10))
        # plot buy signals
        plt.plot(signal[signal['positions'] == 1].index, signal['short_ewma'][signal['positions'] == 1].values, '^',
                 markersize=15, color='g', label='buy')
        # plot sell signals
        plt.plot(signal[signal['positions'] == -1].index, signal['long_ewma'][signal['positions'] == -1].values, 'v',
                 markersize=15, color='r', label='sell')

        # plot close price, short-term and long-term moving averages
        signal['close'].plot(color='k', label ='close')
        signal['short_ewma'].plot(color='b', label ='10 - EWMA')
        signal['long_ewma'].plot(color='g', label ='20 - EWMA')
        signal['signal_diff'] = signal['signal'].diff()

        plt.ylabel('Price', fontsize=15)
        plt.xlabel('Date', fontsize=15)
        plt.title('BTC-USDT EWMA Crossover Strategy', fontsize=20)
        plt.legend()
        plt.grid()
        plt.show()
