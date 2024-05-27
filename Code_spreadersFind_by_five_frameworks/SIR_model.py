import networkx as nx
import numpy as np
import random

# 临界感染率
def infected_beta(graph):
    degree = nx.degree(graph)
    degree_list = []
    degree_sq_list = []
    for i in degree:
        degree_list.append(i[1])
        degree_sq_list.append(i[1] * i[1])
    degree_avg = np.mean(degree_list)
    degree_avg_sq = np.mean(degree_sq_list)
    infected = degree_avg / (degree_avg_sq - degree_avg)
    return infected
def SIR_update_node_status(G,node, beta, gamma):
    if G.nodes[node]["status"] == "I": #感染者
        p = random.random() # 生成一个0到1的随机数
        if p < gamma:   # gamma的概率恢复
            G.nodes[node]["status"] = "R" #将节点状态设置成“R”
    elif G.nodes[node]["status"] == "S": #易感者
        p = random.random() # 生成一个0到1的随机数
        k = 0  # 计算邻居中的感染者数量
        for neibor in G.adj[node]: # 查看所有邻居状态，遍历邻居用 G.adj[node]
            if G.nodes[neibor]["status"] == "I": #如果这个邻居是感染者，则k加1
                k = k + 1
        if p < 1 - (1 - beta)**k:  # 易感者被感染
            G.nodes[node]["status"] = "I"
def count_node(G):
    """
    计算当前图内各个状态节点的数目
    :param G: 输入图
    :return: 各个状态（S、I、R）的节点数目
    """
    s_num, i_num, r_num = 0, 0, 0
    for node in G:
        if G.nodes[node]['status'] == 'S':
            s_num += 1
        elif G.nodes[node]['status'] == 'I':
            i_num += 1
        else:
            r_num += 1
    return s_num, i_num, r_num
def SIR_network(graph, source, beta, gamma, step):
    """
    获得感染源的节点序列的SIR感染情况
    :param graph: networkx创建的网络
    :param source: 需要被设置为感染源的节点序列
    :param beta: 感染率
    :param gamma: 免疫率
    :param step: 迭代次数
    """
    nodes_list = graph.nodes()  # 网络节点个数
    n = len(nodes_list)
    sir_values = []  # 存储每一次的感染节点数
    # 初始化节点状态
    for i in nodes_list:
        graph.nodes[i]['status'] = 'S'  # 将所有节点的状态设置为 易感者（S）
    # 若生成图G中的node编号（从0开始）与节点Id编号（从1开始）不一致，需要减1
    for j in source:
        graph.nodes[j]['status'] = 'I'  # 将感染源序列中的节点设置为感染源，状态设置为 感染者（I）
    # 记录初始状态
    sir_values.append(len(source)/n)
    for t in range(step):
        # 针对对每个节点进行状态更新以完成本次迭代
        for node in nodes_list:
            SIR_update_node_status(graph, node, beta, gamma)  # 针对node号节点进行SIR过程
        s, i, r = count_node(graph)  # 得到本次迭代结束后各个状态（S、I、R）的节点数目
        sir = (r +i) / n  # 本次sir值为迭代结束后 (免疫节点数r+感染节点数)/总节点数n
        sir_values.append(sir)  # 将本次迭代的sir值加入数组
    return sir_values




