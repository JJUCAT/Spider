#!/usr/bin/python3
# -*- coding: UTF-8 -*-


import csv
import pandas as pd
import numpy as np
from mpl_toolkits.axisartist.axislines import SubplotZero
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
from datetime import datetime

# 东方财富
# 主力 = 超大单 + 大单
# 超大单 + 大单 + 中单 + 小单 = 0

def draw_graph(stock):
    step = 5
    dev = 1
    if step == 0:
        dev = 10000   
    load_path = "/home/lmr/ws/spider_ws/Spider/"+stock+".csv"
    with open(load_path,'r') as c:
        r = csv.reader(c)
        date,main,small,mid,big,huge,scale,total= [],[],[],[],[],[],[],[]
        index = 0
        for i in  r :
            if(index !=  0 ):
                date.append(i[0])
                main.append(float(i[1+step])/dev)
                small.append(float(i[2+step])/dev)
                mid.append(float(i[3+step])/dev)
                big.append(float(i[4+step])/dev)
                huge.append(float(i[5+step])/dev)
                scale.append(float(i[12]))
                total.append(main[-1]+small[-1]+mid[-1]+big[-1]+huge[-1])
            index =index+1
        list = ['date','main','small','mid','big','huge','scale','total']
        lists = {};
        lists["date"],lists["main"],lists["small"],lists["mid"],lists["big"],lists["huge"],lists["scale"],lists["total"]=\
        date,main,small,mid,big,huge,scale,total
    
    fig = plt.figure()
    ax1 = fig.add_subplot()
    ax2 = ax1.twinx()
    x = [datetime.strptime(d, '%Y-%m-%d').date() for d in date]

    # ax1 轴
    ax1.plot(x,main, label='main', color='m', linestyle='-', linewidth=1.0)
    # ax1.plot(x,small, label='small', color='b', linestyle='-', linewidth=1.0)
    # ax1.plot(x,mid, label='mid', color='c', linestyle='-', linewidth=1.0)
    # ax1.plot(x,big, label='big', color='g', linestyle='-', linewidth=1.0)
    # ax1.plot(x,huge, label='huge', color='k', linestyle='-', linewidth=1.0)
    # ax1.plot(x,total, label='total', color='b', linestyle='-', linewidth=1.8)
    ax1.legend(loc='upper left', prop = {'size':18})
    plt.grid(axis="y",linestyle='--')
    if step == 0:
        ax1.set_ylabel("sum(w)",fontsize=11) #设置纵轴单位
    elif step == 5:
        ax1.set_ylabel("scale(%)",fontsize=11) #设置纵轴单位
    ax1.set_ylim(-50,50)

    # ax2 轴
    # ax2.plot(x,scale, label='scale', color='r', linestyle='-', linewidth=1.8)
    ax2.bar(x,scale, label='scale', color='r', alpha=0.3)
    ax2.legend(loc='upper right', prop = {'size':18})
    ax2.set_ylabel("scale(%)",fontsize=11) #设置纵轴单位
    ax2.set_ylim(-20,20)

    plt.xlabel("date",fontsize=11)  #设置横轴单位
    ax1.axhline(y=0) #ax1轴画线
    plt.title(stock,fontsize=11)     #设置图片的头部
    save_path = '/home/lmr/ws/spider_ws/Spider/'+stock+'.png'
    plt.savefig(save_path, dpi=1200) #图片保存位置，图片像素
    plt.rcParams['figure.dpi'] =720 #分辨率
    plt.show()


if __name__ == "__main__":
    # draw_graph('002261') # 拓维
    # draw_graph('002594') # 比亚迪
    # draw_graph('000155') # 川能动力
    # draw_graph('600330') # 天通股份
    # draw_graph('600602') # 云赛智联
    # draw_graph('002236') # 大华股份 
    # draw_graph('002527') # 新时达 
    # draw_graph('002536') # 飞龙股份
