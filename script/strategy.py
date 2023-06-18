#!/usr/bin/python3
# -*- coding: UTF-8 -*-


from stock import *
import csv

# 获取热门排行中前 rank 位内，价格低于 high_price 的股票
def find_stock_from_hotrank(high_price, rank):
    print('find_stock_from_hotrank, high_price:%f' % high_price)
    path = "/home/lmr/ws/spider_ws/Spider/data/hotrank.csv"
    stocks=[]
    with open(path,'r') as c:
        r = csv.reader(c)
        index = 0
        for i in  r :
            if (index > rank):
                break            
            if (index !=  0 ):
                if (float(i[3]) <= high_price):
                    s=Stock(i[1][:2], i[1][2:], i[2])
                    stocks.append(s)
                    print('market:%s, code:%s, name:%s' % (s.market, s.code, s.name))
                    print('find suitable stock, code:%s, name:%s, price:%f' % \
                          (i[1], i[2], float(i[3])))
            index = index + 1
    print('stocks len:%d' % (len(stocks)))

    print('after filter')
    for s in stocks:
      print('stockls, market:%s, code:%s, name:%s' % (s.market, s.code, s.name))

    return stocks
            

# 获取 stockls 中 PE 低于 high_PE 的股票
def find_stock_within_PE(stockls, high_PE):
    print('find_stock_within_PE, high_price:%f' % high_PE)
    path = "/home/lmr/ws/spider_ws/Spider/data/realtime.csv"
    stocks=[]
    with open(path,'r') as c:
        r = csv.reader(c)
        index = 0
        for i in  r :
            if (len(stocks)==len(stockls)):
                break            
            if (index !=  0 ):
                for s in stockls:
                  # print('stockls, market:%s, code:%s, name:%s' % (s.market, s.code, s.name))
                  if (i[1]==s.code and i[2]==s.name):
                      print('股票 %s 的PE为 %f' % (s.name, high_PE))
                      if (float(i[15]) < high_PE):
                          print('PE 可以接收')
                          stocks.append(s)
                          break
            index = index + 1

    print('after filter')
    for s in stocks:
      print('stockls, market:%s, code:%s, name:%s' % (s.market, s.code, s.name))

    return stocks








