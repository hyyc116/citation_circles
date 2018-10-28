#coding:utf-8

'''
使用Tarjan’s algorithm with Nuutila’s modifications. Nonrecursive version of algorithm.

再次方法基础之上需要在将子图转换为无向图看是不是强链接图

'''

import networkx as nx


if __name__ == '__main__':
	
	G = nx.DiGraph()
	edges = [
		['a','b'],
		['e','a'],
		['b','e'],
		['b','f'],
		['e','f'],
		['f','g'],
		['g','f'],
		['b','c'],
		['c','g'],
		['c','d'],
		['d','c'],
		['c','g'],
		['d','h'],
		['h','d'],
		['h','g']
	]

	G.add_edges_from(edges)

	for comp in nx.strongly_connected_components(G):
		print comp