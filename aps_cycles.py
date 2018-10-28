
#coding:utf-8

'''
使用cs aminer最简单的aminer进行测试，该数据在自己电脑上

/Users/huangyong/Workspaces/Study/datasets/APS/aps-dataset-citations-2016/aps-dataset-citations-2016.csv

citing_doi,cited_doi
10.1103/PhysRevSeriesI.11.215,10.1103/PhysRevSeriesI.1.1
10.1103/PhysRevSeriesI.17.267,10.1103/PhysRevSeriesI.1.1

'''
from basic_config import *


APS_DATA_PATH = '/Users/huangyong/Workspaces/Study/datasets/APS/aps-dataset-citations-2016/aps-dataset-citations-2016.csv'

### 统计每一篇文章被引的次数
def APS_citation_cycles(aps_citation_network_path):

	logging.info('loading APS citation relations ...')
	aps_references_file = open(aps_citation_network_path)
	aps_references_file.readline()

	edges=[]
	for line in aps_references_file:
		citing_doi,cited_doi = line.strip().split(',')
		edges.add([citing_doi,cited_doi])


	logging.info('{:} citation relations are loaded ...'.format(len(edges)))

	G = nx.DiGraph()
	G.add_edges_from(edges)

	logging.info('start to detect cycles from aps citation network ...')

	cycles = []
	for comp in nx.strongly_connected_components(G):
		if len(comp)==1:
			continue
		cycles.append(','.join(comp))



	open('data/aps_cycles.txt','w').write('\n'.join(cycles))
	logging.info('aminer cycles saved to data/aps_cycles.txt')


if __name__ == '__main__':
	APS_citation_cycles(APS_DATA_PATH)









	