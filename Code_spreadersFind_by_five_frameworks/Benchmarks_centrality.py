import networkx as nx
import json
import pickle
def Collective_Influence(G, l=2):
    Collective_Influence_Dic = {}
    node_set = G.nodes()
    for nid in node_set:
        CI = 0
        neighbor_set = []
        neighbor_hop_1 = list(G.neighbors(nid))
        neighbor_hop_2 = []
        for nnid in neighbor_hop_1:
            neighbor_hop_2  = list(set(neighbor_hop_2).union(set(G.neighbors(nnid))))
        # print("{}:{}".format(nid, neighbor_hop_1))
        # print("{}:{}".format(nid,neighbor_hop_2))

        center = [nid]
        neighbor_set = list(   set(neighbor_hop_2).difference(   set(neighbor_hop_1).union(set(center))  )    )
        # print("{}:{}".format(nid, neighbor_set))
        total_reduced_degree = 0
        for id in neighbor_set:
            total_reduced_degree = total_reduced_degree + (G.degree(id)-1.0)
        #end
        # print("{}:{}".format(nid, total_reduced_degree))
        CI = (G.degree(nid)-1.0) * total_reduced_degree
        Collective_Influence_Dic[nid] = CI
    #end for
    #print "Collective_Influence_Dic:",sorted(Collective_Influence_Dic.iteritems(), key=lambda d:d[1], reverse = True)
    return Collective_Influence_Dic

def Hindex(G):
    HindexDict = dict()
    # print("list(G.nodes())  ", len(list(G.nodes())), list(G.nodes()))
    for curnode in list(G.nodes()):  # ȫ���ڵ�
        # print(" curnode = %d  �ھ�����" % (curnode),G.degree(curnode))
        if G.degree(curnode) == 0:
            HindexDict[curnode] = 0
            continue
        neighborList = [[0 for col in range(2)] for row in range(G.degree(curnode))]
        index = 0
        for j in G.neighbors(curnode):
            neighborList[index][0] = j  # �ھӵ�����
            neighborList[index][1] = G.degree(j)  # �ھӵĶ�
            index += 1
        neighborList.sort(key=lambda d: d[1], reverse=True)
        for i in range(G.degree(curnode)):
            hin = i+1
            if i+1 < len(neighborList):
                if neighborList[i][1] >= hin and neighborList[i+1][1] < hin+1:
                    HindexDict[curnode] = hin
                    break
            else:
                HindexDict[curnode] = hin
    return HindexDict

def local_rank(G):
    N = {}
    Q = {}
    CL = {}
    for node in G.nodes():
        node_nei = list(G.neighbors(node))
        for n_i in node_nei:
            node_nei = node_nei + list(G.neighbors(n_i))
        node_nei = list(set(node_nei))
        N[node] = len(node_nei) - 1

    for node in G.nodes():
        node_nei = list(G.neighbors(node))
        t = 0
        for n_i in node_nei:
            t = t + N[n_i]
        Q[node] = t
    for node in G.nodes():
        node_nei = list(G.neighbors(node))
        t = 0
        for n_i in node_nei:
            t = t + Q[n_i]
        CL[node] = t
    return CL

if __name__ == '__main__':
    # 数据
    NetWorks = ['Celegans', 'Email', 'Ia-fb-messages', 'Lastfm_asia']
    for network in NetWorks:
        with open('../data/{}/Basic_info/{}.gpickle'.format(network, network), 'rb') as f:
            G = pickle.load(f)

        with open('../data/{}/Benchmarks/{}-nodes_CI.json'.format(network, network), 'w', encoding='UTF-8') as fp:
            fp.write(json.dumps(Collective_Influence(G), indent=2, ensure_ascii=False))
        with open('../data/{}/Benchmarks/{}-nodes_HI.json'.format(network, network), 'w', encoding='UTF-8') as fp:
            fp.write(json.dumps(Hindex(G), indent=2, ensure_ascii=False))
        with open('../data/{}/Benchmarks/{}-nodes_LC.json'.format(network, network), 'w', encoding='UTF-8') as fp:
            fp.write(json.dumps(local_rank(G), indent=2, ensure_ascii=False))
        with open('../data/{}/Benchmarks/{}-nodes_EC.json'.format(network, network), 'w', encoding='UTF-8') as fp:
            fp.write(json.dumps(nx.eigenvector_centrality(G,max_iter=1000), indent=2, ensure_ascii=False))
        with open('../data/{}/Benchmarks/{}-nodes_DC.json'.format(network, network), 'w', encoding='UTF-8') as fp:
            fp.write(json.dumps(nx.degree_centrality(G), indent=2, ensure_ascii=False))
        with open('../data/{}/Benchmarks/{}-nodes_CC.json'.format(network, network), 'w', encoding='UTF-8') as fp:
            fp.write(json.dumps(nx.closeness_centrality(G), indent=2, ensure_ascii=False))

        print('{}保存成功'.format(network))