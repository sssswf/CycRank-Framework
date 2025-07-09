
import random
import networkx as nx
import numpy as np
import pandas as pd
import math
import pickle
import json
from SIR_model import infected_beta,SIR_network,run_SIR_experiment
def cycle_number(network):
    with open('../data/{}/{}-nodes_CN.json'.format(network, network), "r") as f:
        CN_dict = json.load(f)
    return CN_dict
def cycle_number_avg(network,cycle):
    sum_number = []
    CN_dict = cycle_number(network)
    # 用 max_value进行归一化
    max_value = max(CN_dict.values())
    for i in cycle:
        sum_number.append(CN_dict[str(i)] / max_value)
    return np.mean(sum_number)
# 按照社区划分方式对基本圈进行排序并输出圈id
def cycle_edgCen_avg(G,basic_cycle):
    edge_cen = nx.edge_current_flow_betweenness_centrality(G)
    edge_llist_all = []
    for i in basic_cycle:
        edge_llist = []
        for j in range(len(i)):
            if j == len(i) - 1:
                edge_llist.append([i[j], i[0]])
            else:
                edge_llist.append([i[j], i[j + 1]])
        edge_llist_all.append(edge_llist)
    edge_all = {}
    for i in range(len(edge_llist_all)):
        edge_i = []
        for j in edge_llist_all[i]:
            if (j[0], j[1]) in edge_cen.keys():
                edge_i.append(edge_cen[(j[0], j[1])])
            else:
                edge_i.append(edge_cen[(j[1], j[0])])
        edge_all[i] = np.mean(edge_i)
    return edge_all
def cycle_edgeAvgCen(network):
    with open('../data/{}/{}-edges_cen.json'.format(network, network), "r") as f:
        edge_dict = json.load(f)
    return edge_dict
def key_cycle_in_neiCom(G,network):
    basic_cycle = nx.cycle_basis(G)
    community = nx.community.louvain_communities(G, seed=123)
    cycle_community_ratio_dict = {}
    for i in range(len(basic_cycle)):
        count_1 = 0
        count_2 = 0
        neighbor_set = set().union(*(G.neighbors(n) for n in basic_cycle[i]))
        for com in community:
            if len(set(basic_cycle[i]) & com) != 0:
                count_1 += 1
            if len(neighbor_set & com) != 0:
                count_2 += 1
        cycle_community_ratio_dict[i] = (count_1 / len(basic_cycle[i])) * (count_2 / len(neighbor_set)) * cycle_number_avg(network,basic_cycle[i]) * cycle_edgeAvgCen(network)[str(i)]

    cycle_community_ratio_dict_sort = sorted(cycle_community_ratio_dict.items(), key=lambda x: x[1], reverse=True)
    cycle_rank_id = []
    for i in range(len(cycle_community_ratio_dict_sort)):
        cycle_rank_id.append(cycle_community_ratio_dict_sort[i][0])
    return cycle_rank_id
#判断节点i和节点集A的所有节点的距离是否都大于d
def distance_judge(G,node,node_list,d):
    z = 1
    for i in node_list:
        distance = nx.shortest_path_length(G, source=node, target=i)
        if distance >= d:
            z = 1
            continue
        else:
            z = -1
            break
    return z

# 从重要圈中按照中心性和距离的约束筛选重要节点
def find_vital_nodes_by_vitalCycle(G,p,index_dict,network):
    k = p * len(G.nodes())
    basic_cycle = nx.cycle_basis(G)
    cycle_id = key_cycle_in_neiCom(G,network)
    seed_node = []
    for i in cycle_id:
        if len(seed_node) < k:
            tempt_index = {}
            cycle_new = set(basic_cycle[i]).difference(set(seed_node))
            for j in cycle_new:
                tempt_index[j] = index_dict[str(j)]
            seed_reday = max(tempt_index, key=tempt_index.get)
            if distance_judge(G,seed_reday,seed_node,2) == 1:
                seed_node.append(seed_reday)
        else:
            break
    return seed_node
