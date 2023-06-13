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

def draw_graph():
    with open(r"/home/lmr/ws/spider_ws/Spider/002261.csv") as c:
        r = csv.reader(c)
        date,main,small,mid,big,huge,price= [],[],[],[],[],[],[]
        index = 0
        for i in  r :
            if(index !=  0 ):
                date.append(i[0])
                main.append(round(float(i[1])/10000))
                small.append(round(float(i[2])/10000))
                mid.append(round(float(i[3])/10000))
                big.append(round(float(i[4])/10000))
                huge.append(round(float(i[5])/10000))
                price.append(float(i[11]))
            index =index+1
        list = ['date','main','small','mid','big','huge','price']
        lists = {};
        lists["date"],lists["main"],lists["small"],lists["mid"],lists["big"],lists["huge"],lists["price"]=\
        date,main,small,mid,big,huge,price
    
    fig = plt.figure()
    ax1 = fig.add_subplot()
    ax2 = ax1.twinx()
    x = [datetime.strptime(d, '%Y-%m-%d').date() for d in date]
    ax1.plot(x,main, label='main', color='k', linestyle='-', linewidth=0.5)
    ax1.plot(x,small, label='small', color='b', linestyle='-', linewidth=0.5)
    ax1.plot(x,mid, label='mid', color='c', linestyle='-', linewidth=0.5)
    # ax1.plot(x,big, label='big', color='g', linestyle='-', linewidth=0.5)
    # ax1.plot(x,huge, label='huge', color='m', linestyle='-', linewidth=0.5)
    ax2.plot(x,price, label='price', color='r', linestyle='-', linewidth=1.8)
    ax1.legend(loc='upper left', prop = {'size':18})
    ax2.legend(loc='upper right', prop = {'size':18})
    plt.grid(axis="y",linestyle='--')
    plt.ylabel("price(w)",fontsize=11) #设置纵轴单位
    plt.xlabel("date",fontsize=11)  #设置横轴单位
    plt.title("002261",fontsize=11)     #设置图片的头部
    plt.savefig('/home/lmr/ws/spider_ws/Spider/002261.png',dpi=1200) #图片保存位置，图片像素
    plt.rcParams['figure.dpi'] =720 #分辨率
    plt.show()


if __name__ == "__main__":
    draw_graph()
