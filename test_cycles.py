#coding:utf-8

'''
使用Tarjan’s algorithm with Nuutila’s modifications. Nonrecursive version of algorithm.

再次方法基础之上需要在将子图转换为无向图看是不是强链接图

'''

import networkx as nx


if __name__ == '__main__':
	
	G = nx.DiGraph()
	edges = [
		[317800,685521],
		[601153,685521],
		[603169,685521],
		[603172,685521],
		[603175,685521],
		[604255,685521],
		[852179,685521],
		[852184,685521]
	]

	G.add_edges_from(edges)

	for comp in nx.strongly_connected_components(G):
		print comp