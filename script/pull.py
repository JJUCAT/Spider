#!/usr/bin/python3
# -*- coding: UTF-8 -*-


import akshare as ak
import numpy as np
import os
import pandas as pd
import requests
import datetime

def gen_secid(stock_code):
    '''
    生成东方财富专用的secid

    Parameters
    ----------
    stock_code: 6 位股票代码

    Return
    ------
    str : 东方财富给股票设定的一些东西
    '''
    # 沪市指数
    if stock_code[:3] == '000':
        print('沪市指数')
        return f'1.{stock_code}'
    # 深证指数
    if stock_code[:3] == '399':
        print('深证指数')
        return f'0.{stock_code}'
    # 沪市股票
    if stock_code[0] != '6':
        print('沪市股票')
        return f'0.{stock_code}'
    # 深市股票
    print('深市股票')
    return f'1.{stock_code}'


def gen_secid_new(stock_code, id):
    # 沪市股票
    if id == 'h':
        print('沪市股票')
        return f'0.{stock_code}'
    # 深市股票
    print('深市股票')
    return f'1.{stock_code}'


def get_history_bill(stock_code,id):
    '''
    获取多日单子数据
    -
    Parameters
    ----------
    stock_code: 6 位股票代码

    Return
    ------
    DataFrame : 包含指定股票的历史交易日单子数据（大单、超大单等）

    '''
    EastmoneyHeaders = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Referer': 'http://quote.eastmoney.com/center/gridlist.html',
    }
    EastmoneyBills = {
        'f51': '日期',
        'f52': '主力净流入',
        'f53': '小单净流入',
        'f54': '中单净流入',
        'f55': '大单净流入',
        'f56': '超大单净流入',
        'f57': '主力净流入占比',
        'f58': '小单流入净占比',
        'f59': '中单流入净占比',
        'f60': '大单流入净占比',
        'f61': '超大单流入净占比',
        'f62': '收盘价',
        'f63': '涨跌幅'

    }
    fields = list(EastmoneyBills.keys())
    columns = list(EastmoneyBills.values())
    fields2 = ",".join(fields)
    # secid = gen_secid(stock_code)
    secid = gen_secid_new(stock_code,id)
    params = (
        ('lmt', '100000'),
        ('klt', '101'),
        ('secid', secid),
        ('fields1', 'f1,f2,f3,f7'),
        ('fields2', fields2),

    )
    params = dict(params)
    url = 'http://push2his.eastmoney.com/api/qt/stock/fflow/daykline/get'
    json_response = requests.get(url,
                                 headers=EastmoneyHeaders, params=params).json()
    data = json_response.get('data')
    if data is None:
        if secid[0] == '0':
            secid = f'1.{stock_code}'
        else:
            secid = f'0.{stock_code}'
        params['secid'] = secid
        
        json_response: dict = requests.get(
            url, headers=EastmoneyHeaders,params=params).json()
        data = json_response.get('data')
    if data is None:
        print('股票代码:', stock_code, '可能有误')
        return pd.DataFrame(columns=columns)
    if json_response is None:
        return
    data = json_response['data']
    klines = data['klines']
    rows = []
    for _kline in klines:
        kline = _kline.split(',')
        rows.append(kline)
    df = pd.DataFrame(rows, columns=columns)

    return df

def pull_kline(stock,id):
    # 调用函数获取股票历史单子数据（有天数限制）
    df = get_history_bill(stock,id)
    # 保存数据到 csv 文件中
    df.to_csv(f'{stock}.csv', index=None, encoding='utf-8-sig')
    print(stock, f'的历史单子数据已保存到文件 {stock}.csv 中')

class Stock():
    def __init__(self, code, id):
        self.code = code
        self.id = id

# 更新股票名单
def pull_stocks():
    # a 股所有股票
    astockls = ak.stock_info_a_code_name()
    apath = '/home/lmr/ws/spider_ws/Spider/data/astockls.csv'
    astockls.to_csv(apath, index=None, encoding='utf-8-sig')
    print('A股股票列表已保存到 %s 中' % (apath))

    # 上证股票
    shstockls = ak.stock_info_sh_name_code()
    shpath = '/home/lmr/ws/spider_ws/Spider/data/shstockls.csv'
    shstockls.to_csv(shpath, index=None, encoding='utf-8-sig')
    print('上证股票列表已保存到 %s 中' % (shpath))

    # 深证股票
    szstockls = ak.stock_info_sz_name_code()
    szpath = '/home/lmr/ws/spider_ws/Spider/data/szstockls.csv'
    szstockls.to_csv(szpath, index=None, encoding='utf-8-sig')
    print('深证股票列表已保存到 %s 中' % (szpath))

# 获取热门股票，上升榜，热门关键词
def pull_hot_topic():
    hotrank = ak.stock_hot_rank_em()
    hrpath = '/home/lmr/ws/spider_ws/Spider/data/hotrank.csv'
    hotrank.to_csv(hrpath, index=None, encoding='utf-8-sig')
    print('热门股票列表已保存到 %s 中' % (hrpath))

    hotup = ak.stock_hot_up_em()
    hupath = '/home/lmr/ws/spider_ws/Spider/data/hotup.csv'
    hotup.to_csv(hupath, index=None, encoding='utf-8-sig')
    print('热门上升股票列表已保存到 %s 中' % (hupath))

    hotkeywork = ak.stock_hot_keyword_em()
    hkpath = '/home/lmr/ws/spider_ws/Spider/data/hotkeywork.csv'
    hotkeywork.to_csv(hkpath, index=None, encoding='utf-8-sig')
    print('热门关键词列表已保存到 %s 中' % (hkpath))

# 获取所有股票的实时信息
def pull_realtime():
    realtime = ak.stock_zh_a_spot_em()
    rtpath = '/home/lmr/ws/spider_ws/Spider/data/realtime.csv'
    realtime.to_csv(rtpath, index=None, encoding='utf-8-sig')
    print('A股实时信息已保存到 %s 中' % (rtpath))

# 获取指定股票最近 100 天的历史数据
def pull_history(code):
    today=datetime.datetime.now()
    end_date=today.strftime('%Y%m%d')
    start_date=(today-datetime.timedelta(days=100)).strftime('%Y%m%d') # 100 天前的时间
    print('start_date: %s, end_date: %s' % (start_date, end_date))
    history = ak.stock_zh_a_hist(symbol=code, period="daily", start_date=start_date, end_date=end_date, adjust="")
    hpath = '/home/lmr/ws/spider_ws/Spider/data/history/' + code + '.csv'
    history.to_csv(hpath, index=None, encoding='utf-8-sig')
    print('%s 股票的历史数据已保存到 %s 中' % (code, hpath))


# 获取股票年报，但有问题用不了
def pull_report():
    today=datetime.datetime.now().strftime('%Y%m%d')
    report = ak.stock_yjbb_em(date=today)
    rpath = '/home/lmr/ws/spider_ws/Spider/data/report.csv'
    report.to_csv(rpath, index=None, encoding='utf-8-sig')
    print('A股股票年报已保存到 %s 中' % (rpath))


# 获取高管持股情况
def pull_senior():
    senior = ak.stock_ggcg_em_df = ak.stock_ggcg_em(symbol="全部")
    spath = '/home/lmr/ws/spider_ws/Spider/data/senior.csv'
    senior.to_csv(spath, index=None, encoding='utf-8-sig')
    print('高管持股信息已保存到 %s 中' % (spath))

# 个股资金流向
def pull_flow_single(code, market):
    flow = ak.stock_individual_fund_flow(stock=code, market=market)
    fpath = '/home/lmr/ws/spider_ws/Spider/data/flow/' + code + '.csv'
    flow.to_csv(fpath, index=None, encoding='utf-8-sig')
    print('股票 %s 资金流向已保存到 %s 中' % (code, fpath))

# 资金流向排行
def pull_flow_rank(days=1):
    if days <= 1:
        ind = "今日"
    else:
        ind = str(days) + "日"
    flow = ak.stock_individual_fund_flow_rank(indicator=ind)
    today=datetime.datetime.now().strftime('%Y%m%d')
    fpath = '/home/lmr/ws/spider_ws/Spider/data/flowrank/flow_rank_' + str(days) + '日_from_' + today + '.csv'
    flow.to_csv(fpath, index=None, encoding='utf-8-sig')
    print('股票资金流向排行已保存到 %s 中' % (fpath))

# 行业资金流向排行
def pull_sector_flow_rank(days=1):
    if days <= 1:
        ind = "今日"
    else:
        ind = str(days) + "日"
    flow = ak.stock_sector_fund_flow_rank(indicator=ind, sector_type="行业资金流")
    today=datetime.datetime.now().strftime('%Y%m%d')
    fpath = '/home/lmr/ws/spider_ws/Spider/data/sectorflowrank/sector_flow_rank_' + str(days) + '日_from_' + today + '.csv'
    flow.to_csv(fpath, index=None, encoding='utf-8-sig')
    print('行业资金流向排行已保存到 %s 中' % (fpath))

# 行业个股资金流向排行
def pull_sector_stock_flow_rank(sector, days=1):
    if days <= 1:
        ind = "今日"
    else:
        ind = str(days) + "日"
    flow = ak.stock_sector_fund_flow_summary(symbol=sector, indicator=ind)
    today=datetime.datetime.now().strftime('%Y%m%d')
    fpath = '/home/lmr/ws/spider_ws/Spider/data/sectorflowrank/sector_stock_flow_rank_' + str(days) + '日_from_' + today + '.csv'
    flow.to_csv(fpath, index=None, encoding='utf-8-sig')
    print('行业个股资金流向排行已保存到 %s 中' % (fpath))



if __name__ == "__main__":
    # pull_stocks() # 更新股票列表
    # pull_hot_topic() # 更新热门信息
    # pull_realtime() # 更新实时指数
    # pull_history('000001') # 更新各个历史数据
    # pull_senior()
    # pull_flow_single('000001','sh')
    # pull_flow_rank()
    # pull_sector_flow_rank()
    pull_sector_stock_flow_rank('互联网服务')