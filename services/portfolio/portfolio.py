import pandas as pd

class Portfolio:

    def __init__(self, symbol, initial_capital=10000.0):
        self.symbol = symbol
        self.initial_capital = float(initial_capital)
        self.portfolio = pd.DataFrame(columns=[symbol, symbol + '_total_val', 'holdings_val', 'cash', 'portfolio_value', 'return'])

    def intialise_portfolio(self, signal):
        self.portfolio = self.portfolio.reindex(signal.index)
        self.portfolio.iloc[0] = [0, 0, 0, self.initial_capital, self.initial_capital, 0]