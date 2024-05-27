import networkx as nx
import numpy as np
def similarity_nodes(G,node_list):
    su_all = []
    for i in node_list:
        for j in node_list:
            if i != j:
                jiaoji = len(set(nx.neighbors(G,i)) & set(nx.neighbors(G,j)))
                bingji = len(set(nx.neighbors(G,i)) | set(nx.neighbors(G,j)))
                su = jiaoji / bingji
                su_all.append(su)
    su_avg = np.mean(su_all)
    return su_avg
def similarity_judge(G,node,node_list):
    or_sim = similarity_nodes(G, node_list)
    new_node_list = []
    for i in node_list:
        new_node_list.append(i)
    new_node_list.append(node)
    now_sim = similarity_nodes(G, new_node_list)
    if now_sim <= or_sim:
        z = True
    else:
        z = False
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

def DecSim(G,k,methods):
    seed_node = k * len(G.nodes())
    index_original = get_index_original(methods=methods)
    methods_name = np.array(methods.columns)[1: len(methods.columns)]
    seed_node_all = []
    for j in range(0, len(methods_name)):
        count_seed = 2
        seed_node_list = []
        seed_node_list.append(index_original[j][0])
        seed_node_list.append(index_original[j][1])
        for i in range(2, len(index_original[j])):
            if count_seed <= seed_node:
                if similarity_judge(G, index_original[j][i], seed_node_list):
                    seed_node_list.append(index_original[j][i])
                    count_seed = count_seed + 1
                else:
                    continue
            else:
                break
        seed_node_all.append(seed_node_list)
    return seed_node_all



