from services.strategy.ewma_crossover import EWMACrossover
from data.binance_dao import BinanceDAO
from services.portfolio.portfolio import Portfolio
from services.backtester.backtester import Backtester
from services.presentation.plotter import Plotter

ticker = 'BTC/USDT'
short_window = 10
long_window = 20
data_service = BinanceDAO()
strat = EWMACrossover(ticker, data_service, short_window, long_window)
signal = strat.gen_signal('1m', 5000, 'close')
initial_capital = 10000.0
portfolio = Portfolio(ticker, initial_capital)
backtester = Backtester(portfolio)
portfolio_results = backtester.backtest_portfolio(signal)

plotter = Plotter()
plotter.plot_strategy(signal)

print('here')

