'''
输入：网络图邻接矩阵，需要被设置为感染源的节点序列，感染率，免疫率，迭代次数step
输出：所有时间步  SIR模型迭代的  感染数量比例（包含免疫）  以及  std 文件
'''

import random
import networkx as nx
import numpy as np
import pandas as pd
import math
import pickle
# 获得所需的top-k节点
def TopK(methods, k):
    print('Top-' + str(k) + '节点生成中...')
    # 循环每一个方法
    source_all = []
    methods_name = np.array(methods.columns)[1: len(methods.columns)]
    for i in range(len(methods_name)):
        nodes_ID = methods.iloc[:, 0]
        method = methods.iloc[:, i + 1]  # 方法列
        index_top_K = method.argsort()[::-1][0:k]
        source = []
        for j in index_top_K:
            source.append(nodes_ID[j])
        source_all.append(source)
    return source_all