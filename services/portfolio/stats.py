


class Stats():

    def sharpe(self, returns):
        return returns.mean()/returns.std()

    def trade_stats(self, portfolio_results, signal):
        trade_times = signal[(signal['positions'] == 1) | (signal['positions'] == -1)].index
        no_trades = len(trade_times)
        #Check we have even number of trade pairs - maybe we were still holding the last trade
        if no_trades % 2 !=0:
            no_trades = no_trades-1
        trades = portfolio_results.loc[trade_times]
        trade_returns = []
        #Get trade pairs and calculate the return
        #Big note: this is calculated using close prices so
        #not entirely accurate, i.e. we bought at open price
        #would need to change this therefore in real life
        for i in range(0, no_trades, 2):
            buy = portfolio_results.loc[trade_times[i]]
            sell = portfolio_results.loc[trade_times[i+1]]
            return_val = (sell['portfolio_value']-buy['portfolio_value'])/buy['portfolio_value']
            trade_returns.append(return_val)

        return trade_returns