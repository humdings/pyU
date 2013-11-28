# -*- coding: utf-8 -*-

from pyU.finance.stocks import (
    rSTATS, STATS, Stock, get_historical_prices
)

def quotes(cell, stocks, **kwargs):
    """
        Optional keyword arguments:
            sheet='sheet name'
            wkbk='workbook name'
    """
    anchor = Cell(cell)
    wkbk = kwargs.get('wkbk')
    sheet = kwargs.get('sheet')    
    if wkbk:
        active_wkbk(wkbk)
    if sheet:
        active_sheet(sheet)
    row, col = anchor.row, anchor.col
    stocks = [Stock(i) for i in stocks]
    keys = sorted(stocks[0].all.keys())
    Cell(row, col).horizontal = ['Stock'] + [rSTATS[i] for i in keys]
    n_rows = len(Cell("A1").horizontal)    
    n_cols = len(stocks) + 1
    table = [[i.symbol]+[i.all[j] for j in keys] for i in stocks]    
    Cell(row+1, col).table = table
    
    anchor.vertical_range.font.bold = True
    anchor.horizontal_range.font.bold = True
    
    autofit()

def history(sym, start, end, **kwargs):
    wkbk = kwargs.get('wkbk')
    sheet = kwargs.get('sheet')    
    if wkbk:
        active_wkbk(wkbk)
    if sheet:
        active_sheet(sheet)
    
    data = get_historical_prices(sym, start, end, **kwargs)
    dates = sorted(data.keys())
    keys = data[dates[0]].keys()
    table = [[i]+[data[i][j] for j in keys] for i in dates]

    Cell("A1").horizontal = [sym] + keys
    Cell("A2").table = table
    CellRange("A1:G1").font.bold = True
    autofit()


def get_column_names():
    return [i for i in STATS]
    
def set_column_names(cell):
    Cell(cell).horizontal = get_column_names()


