# -*- coding: utf-8 -*-

from datanitro.nitro_stocks import *


IMG_DIR = '..\\img\\'         

today = datetime.date.today()
yesterday = datetime.date.today() - datetime.timedelta(days=1)
_3months_ago = yesterday - datetime.timedelta(days=90)


rename_sheet('Sheet1','Quotes' + str(today))

stocks = ['GOOG', 'SPY','AA','DD','AMZN']
avgs = ['e5','e20']

#quotes(stocks)   

for stock in stocks:
    new_sheet(stock)
    img_file = IMG_DIR + '%s.png'%stock
    img = StockChart(stock, size='m', tspan='3m', avgs=avgs)
    img.save(img_file)
    history(stock, _3months_ago, yesterday, sheet=stock)
    picture = Image(img.abspath)
    picture.x += 350
    picture.y +=20
    

