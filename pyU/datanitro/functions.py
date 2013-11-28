from core import *

def stock_stat(ticker, stat):
    stock = Stock(ticker)
    try:
        return stock.all[STATS[stat]]
    except KeyError:
        return "ERR: FIX NAMES"
    else:
        return stock.all[stat]

def update_prices():
    pass
