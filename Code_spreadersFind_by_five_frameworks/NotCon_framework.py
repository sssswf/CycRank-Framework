import networkx as nx
import numpy as np
def distance_judge(G,node,node_list,d):
    for i in node_list:
        distance = nx.shortest_path_length(G, source=node, target=i)
        if distance >= d:
            z = True
            continue
        else:
            z = False
            break
    return z
def get_index_original(methods):
    # 循环每一个方法
    source_all = []
    methods_name = np.array(methods.columns)[1: len(methods.columns)]
    for i in range(len(methods_name)):
        nodes_ID = methods.iloc[:, 0]
        method = methods.iloc[:, i + 1]  # 方法列
        index_top_K = method.argsort()[::-1]
        source = []
        for j in index_top_K:
            source.append(nodes_ID[j])
        source_all.append(source)
    return source_all

def NotCon(G,k,methods):
    seed_node = k * len(G.nodes())
    index_original = get_index_original(methods=methods)
    seed_node_all = []
    methods_name = np.array(methods.columns)[1: len(methods.columns)]
    for j in range(0, len(methods_name)):
        count_seed = 1
        seed_node_list = []
        seed_node_list.append(index_original[j][0])
        for i in range(1, len(index_original[j])):
            if count_seed <= seed_node:
                if distance_judge(G, index_original[j][i], seed_node_list, 2):
                    seed_node_list.append(index_original[j][i])
                    count_seed = count_seed + 1
                else:
                    continue
            else:
                break
        seed_node_all.append(seed_node_list)
    return seed_node_all
