#coding:utf-8
'''
画一个大小为10的SCC

'''

from basic_config import *


def plot_cc_size_10(pathObj):

    ### 加载scc所有边的关系
    scc_relations = [line.strip().split(',') for line in open(pathObj._relations)]

    ### 加载scc的时间
    scc_years = json.loads(open(pathObj._years).read())

    ## 选择一个长度为10的scc
    scc = [line.strip().split(',') for line in open(pathObj._sccs) if len(line.strip().split(','))==10][0]

    dig = nx.DiGraph()

    dig.add_edges_from(scc_relations)

    ## scc的样子
    scc_edges = dig.subgraph(scc).edges

    ##保存一个图
    plot_a_subcascade(scc_edges,pathObj._10_size_scc_fig,format='pdf')

if __name__ == '__main__':
    if int(sys.argv[1])==0:

        pathObj = PATHS('physics')

    else:

        pathObj = PATHS('computer science')

    plot_cc_size_10(pathObj)



