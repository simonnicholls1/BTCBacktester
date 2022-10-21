import math
from services.portfolio.portfolio import Portfolio

class Backtester:

    def __init__(self, portfolio: Portfolio):
        self.portfolio = portfolio

    def backtest_portfolio(self, signal):
        self.portfolio.intialise_portfolio(signal)
        no_dates = len(self.portfolio.portfolio.index)
        curr_holdings = self.portfolio.portfolio.iloc[0]
        order = None

        # Loop through each date
        for i in range(1, no_dates):
            curr_date = self.portfolio.portfolio.index[i]
            prior_date = self.portfolio.portfolio.index[i-1]
            curr_signal = signal.loc[curr_date]
            prior_signal = signal.loc[prior_date]
            curr_price = prior_signal['close']
            curr_open_price = curr_signal['open']

            #Check for any orders and execute
            if order == 'SELL':
                #Sell at open price
                value = curr_holdings[self.portfolio.symbol] * curr_open_price
                cash = curr_holdings['cash'] + value
                holdings = [0, 0, 0, cash, cash, 0]
                order = None
            elif order == 'BUY':
                #Buy at open price
                #Get number of futures we can buy
                no_holdings = math.floor(curr_holdings['cash']/curr_open_price)
                value = no_holdings * curr_open_price
                cash = curr_holdings['cash'] - value

                #Recalc value for MTM close price
                value = no_holdings * curr_price
                holdings = [no_holdings, value, value, cash, cash + value, 0]
                order = None
            elif order is None:
                #Mark to market
                holding_value = curr_holdings[self.portfolio.symbol] * curr_price
                cash = curr_holdings['cash']
                port_val = holding_value + cash
                port_ret = (port_val-curr_holdings['portfolio_value'])/curr_holdings['portfolio_value']
                holdings = [curr_holdings[self.portfolio.symbol], holding_value, holding_value, cash, port_val, port_ret]

                #Check for signal change triggering trade
                if (prior_signal['signal'] == 1) and (curr_signal['signal'] == 0):
                    order = 'SELL'
                if (prior_signal['signal'] == 0) and (curr_signal['signal'] == 1):
                    order = 'BUY'

            self.portfolio.portfolio.loc[curr_date] = holdings
            curr_holdings = self.portfolio.portfolio.loc[curr_date]

        return self.portfolio.portfolio