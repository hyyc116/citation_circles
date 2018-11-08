#coding:utf-8
import os
import sys
import json
from collections import defaultdict
from collections import Counter
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import math
import numpy as np
import random
import logging
import networkx as nx
import pylab
from networkx.algorithms import isomorphism
from collections import Counter
import matplotlib as mpl
import matplotlib.colors as colors
from cycler import cycler

'''
==================
## logging的设置，INFO
==================
'''
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',level=logging.INFO)

'''
==================
### 示意图的画图方法
==================
'''
# from viz_graph import *



'''
==================
### 数据库
==================
'''
from database import *



'''
==================
### 路径
==================
'''
from paths import *


'''
==================
## pyplot的设置
==================
'''
## 最大的chunksize
mpl.rcParams['agg.path.chunksize'] = 10000

## 颜色循环，取代默认的颜色
color_sequence = ['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c','#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5',
                '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f',
                '#c7c7c7', '#bcbd22', '#dbdb8d', '#17becf', '#9edae5']

mpl.rcParams['axes.prop_cycle'] = cycler('color', color_sequence)

### 用特定的color theme进行画图
# color = plt.cm.viridis(np.linspace(0.01,0.99,6)) # This returns RGBA; convert:
# hexcolor = map(lambda rgb:'#%02x%02x%02x' % (rgb[0]*255,rgb[1]*255,rgb[2]*255),
#                tuple(color[:,0:-1]))

# mpl.rcParams['axes.prop_cycle'] = cycler('color', hexcolor)

## 画图各种参数的大小
params = {'legend.fontsize': 10,
        'axes.labelsize': 15,
        'axes.titlesize':20,
        'xtick.labelsize':15,
        'ytick.labelsize':15}

pylab.rcParams.update(params)

'''
==================
## 画柱状图时进行自动标签
==================
'''
def autolabel(rects,ax,total_count=None,step=1,):
    """
    Attach a text label above each bar displaying its height
    """
    for index in np.arange(len(rects),step=step):
        rect = rects[index]
        height = rect.get_height()
        # print height
        if not total_count is None:
            ax.text(rect.get_x() + rect.get_width()/2., 1.005*height,
                '{:}\n({:.6f})'.format(int(height),height/float(total_count)),
                ha='center', va='bottom')
        else:
            ax.text(rect.get_x() + rect.get_width()/2., 1.005*height,
                '{:}'.format(int(height)),
                ha='center', va='bottom')







