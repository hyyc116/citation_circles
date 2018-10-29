#coding:utf-8

'''
使用Tarjan’s algorithm with Nuutila’s modifications. Nonrecursive version of algorithm.

再次方法基础之上需要在将子图转换为无向图看是不是强链接图

'''

from basic_config import *


if __name__ == '__main__':
	
	G = nx.DiGraph()
	edges = [
		['a','b'],
		['b','c'],
		['c','d'],
		['d','a'],
		['c','a'],
		['d','e'],
		['e','d'],
		['e','h'],
		['h','e']
	]

	plot_a_subcascade(edges,'fig/test')

	G.add_edges_from(edges)

	for comp in nx.strongly_connected_components(G):
		print comp



	G = nx.DiGraph()
	edges = [
		['a','b'],
		['b','c'],
		['c','d'],
		['d','e'],
		['e','f']
	]

	plot_a_subcascade(edges,'fig/test2')

	G.add_edges_from(edges)

	for comp in nx.strongly_connected_components(G):
		print comp


