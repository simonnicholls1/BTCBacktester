from services.strategy.ewma_crossover import EWMACrossover
from data.binance_dao import BinanceDAO
from services.portfolio.portfolio import Portfolio
from services.backtester.backtester import Backtester
from services.presentation.plotter import Plotter
from services.portfolio.stats import Stats

ticker = 'BTC/USDT'
short_window = 10
long_window = 20


#Generate signal
data_service = BinanceDAO()
strat = EWMACrossover(ticker, data_service, short_window, long_window)
signal = strat.gen_signal('1m', 5000, 'close')

#Setup portfolio
initial_capital = 10000.0
portfolio = Portfolio(ticker, initial_capital)

#Run backtester
backtester = Backtester(portfolio)
portfolio_results = backtester.backtest_portfolio(signal)

#Plot
plotter = Plotter()
plotter.plot_strategy(signal)
plotter.plot_portfolio(portfolio_results)

#Stats
stats = Stats()
final_acc_balance = portfolio_results['portfolio_value'][-1]
final_return = (portfolio_results['portfolio_value'][-1] - portfolio_results['portfolio_value'][0])/portfolio_results['portfolio_value'][0]
sharpe = stats.sharpe(portfolio_results['return'])
trades = stats.trade_stats(portfolio_results, signal)

#Output
print('Portfolio initial balance {0}'.format(initial_capital))
print('Portfolio final balance {0}'.format(final_acc_balance))
print('Portfolio return {:.2%}'.format(final_return))
print('Portfolio sharp {:.0}'.format(sharpe))
print('No Trades {0}'.format(len(trades)))
print('Trade Returns {0}'.format(trades))
print('Number profitable {0}'.format(sum(i > 0 for i in trades)))
print('Number not profitable {0}'.format(sum(i < 0 for i in trades)))

