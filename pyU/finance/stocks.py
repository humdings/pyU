# -*- coding: utf-8 -*-

import os
import webbrowser
from urllib2 import Request, urlopen
from urllib import urlencode, urlretrieve
import datetime


STATS = {
    'Price': 'price',
    'Volume': 'volume',
    'Last Update': 'timestamp',
    '200 Day SMA': 'two_hundred_day_moving_avg',
    '50 Day SMA': 'fifty_day_moving_avg',
    '52 Week High': 'fifty_two_week_high',
    '52 Week Low': 'fifty_two_week_low',
    'Ave Daily Volume': 'avg_daily_volume',
    'Book Value': 'book_value',
    'Change': 'change',
    'Dividend Per Share': 'dividend_per_share',
    'Dividend Yield': 'dividend_yield',
    'EBITDA': 'ebitda',
    'Earnings Per Share': 'earnings_per_share',
    'Market Cap': 'market_cap',
    'Price Book Ratio': 'price_book_ratio',
    'Price Earnings Growth Ratio': 'price_earnings_growth_ratio',
    'Price Earnings Ratio': 'price_earnings_ratio',
    'Price Sales Ratio': 'price_sales_ratio',
    'Short Ratio': 'short_ratio',
    'Stock Exchange': 'stock_exchange',
    
}
rSTATS = {STATS[i]: i for i in STATS}  # reversed version for convienience 


def get_historical_prices(sym, start_date, end_date, **kwargs):  
    """
    Date format must be 'YYYY-MM-DD' or a datetime object.

    keyword arg 'interval' is supported.
        'd' ==> days,
        'w' ==> weeks,
        'm' ==> monthts,
    There is an interval 'v' for dividends only but if a stock doesn't
    offer dividends a KeyError is raised.
    """
    
    start_date = str(start_date)
    end_date = str(end_date)
    url = 'http://ichart.yahoo.com/table.csv?'  
    url += 's={}&a={}&b={}&c={}&d={}&e={}&f={}&g={}'.format(  
        sym,  
        str(int(start_date[5:7]) - 1),  
        str(int(start_date[8:10])),  
        str(int(start_date[0:4])),  
        str(int(end_date[5:7]) - 1),  
        str(int(end_date[8:10])),
        str(int(end_date[0:4])),
        kwargs.get('interval', 'd'),
    )  
    url += '&ignore=.csv'  
    req = Request(url)
    resp = urlopen(req)
    content = str(resp.read().decode('utf-8').strip())
    daily_data = content.splitlines()
    hist_dict = dict()
    keys = daily_data[0].split(',')
    for day in daily_data[1:]:
        day_data = day.split(',')
        date = day_data[0]
        hist_dict[date] = {
            keys[i]: day_data[i] for i in range(1,len(keys))
        }
    return hist_dict    
    


class StockChart():
    """
    Gets a stock chart from Yahoo that can be opened in
    a browser or saved to a file for use elsewhere.
    
    url parameters:
    Stock symbol is the bare minimum unless called from a stock object,
    then no parameters are required. Optional keyword args are outlined
    below.

    keyword arguments:
        timespan: 1d, 5d, 3m, 6m, 1y, 2y, 5y, my (max years)
            eg: tspan = 3m 
        type: line=l, bar=b, candle=c
            eg: type = b   
        scale: on/off for logarithmic/linear
            eg: scale = on
        size: s, m, l
            eg: size=m
        avgs: moving average indicators.
            pass a list of day lengths as strings prepended
            with 'e' for exponential and 'm' for simple.
            eg: avgs=['m5','m20','e5','e20']
            
        """
    def __init__(self, symbol, **kwargs):
        self.symbol = symbol
        self.kwargs = kwargs
        self.url = self._url()
        
    def open_in_browser(self):
        webbrowser.open_new(self.url)
    
    def save(self, path):
        urlretrieve(self.url, path)
        self.abspath = os.path.abspath(path)
        
    def _url(self):
        kwargs = self.kwargs
        symbol = self.symbol
        url = "http://chart.finance.yahoo.com/z?"
        params = urlencode({
            's': symbol,
            't': kwargs.get('tspan','6m'),
            'q': kwargs.get('type', 'l'),
            'l': kwargs.get('scale', 'off'),
            'z': kwargs.get('size', 's'),
            'p': ','.join(kwargs.get('avgs',''))
        })
        url += "%s"%params
        return url


class Stock(object):
    
    def __init__(self, symbol):
        self.symbol = symbol
        self.all = self._all_quote_data()
        self.timestamp = datetime.datetime.now()
        self.all['timestamp'] = self.timestamp
        self.price = self.all['price']
        self.change = self.all['change']
        self.volume = self.all['volume']
        self.avg_daily_volume = self.all['avg_daily_volume']
        self.stock_exchange = self.all['stock_exchange']
        self.market_cap = self.all['market_cap']
        self.book_value = self.all['book_value']
        self.ebitda = self.all['ebitda']
        self.dividend_per_share = self.all['dividend_per_share']
        self.dividend_yield = self.all['dividend_yield']
        self.earnings_per_share = self.all['earnings_per_share']
        self.fifty_two_week_high = self.all['fifty_two_week_high']
        self.fifty_two_week_low = self.all['fifty_two_week_low']
        self.fifty_day_moving_avg = self.all['fifty_day_moving_avg']
        self.two_hundred_day_moving_avg = self.all['two_hundred_day_moving_avg']
        self.price_earnings_ratio = self.all['price_earnings_ratio']
        self.price_earnings_growth_ratio = self.all['price_earnings_growth_ratio']
        self.price_sales_ratio = self.all['price_sales_ratio']
        self.price_book_ratio = self.all['price_book_ratio']
        self.short_ratio = self.all['short_ratio']
        
    def __repr__(self):
        return "< %s: %s >"%(self.symbol, self.timestamp)
    
    def _quote_request(self, stat):
        url = "http://download.finance.yahoo.com/d/quotes.csv?s=%s&f=%s" %(
            self.symbol, 
            stat
        )
        req = Request(url)
        response = urlopen(req)
        return str(response.read().decode('utf-8').strip())
    
    def _all_quote_data(self):
        values = self._quote_request('l1c1va2xj1b4j4dyekjm3m4rr5p5p6s7').split(',')
        return dict(
            price = values[0],
            change = values[1],
            volume = values[2],
            avg_daily_volume = values[3],
            stock_exchange = values[4],
            market_cap = values[5],
            book_value = values[6],
            ebitda = values[7],
            dividend_per_share = values[8],
            dividend_yield = values[9],
            earnings_per_share = values[10],
            fifty_two_week_high = values[11],
            fifty_two_week_low = values[12],
            fifty_day_moving_avg = values[13],
            two_hundred_day_moving_avg = values[14],
            price_earnings_ratio = values[15],
            price_earnings_growth_ratio = values[16],
            price_sales_ratio = values[17],
            price_book_ratio = values[18],
            short_ratio = values[19],
        )
    def chart(self, **kwargs):
        return StockChart(self.symbol, **kwargs)
    
    def history(self, start_date, end_date, **kwargs):
        return get_historical_prices(
            self.symbol, start_date, end_date, **kwargs
        )
    def update(self):
        self.__init__(self.symbol)
        
    

