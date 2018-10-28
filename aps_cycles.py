
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
		edges.append([citing_doi,cited_doi])


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

## cycle大小的分布
def cycle_size_distribution(aps_cycles_path):
	# cycles = []

	size_dis = defaultdict(int)
	for line in open(aps_cycles_path):

		cycle = line.split(',')

		size_dis[len(cycle)]+=1

	xs = []
	ys = []
	for size in sorted(size_dis.keys()):
		xs.append(size)
		ys.append(size_dis[size])

	plt.figure(figsize=(6,5))
	plt.plot(xs,ys,'-o')

	plt.xscale('log')
	plt.yscale('log')

	plt.xlabel('size of cycle')
	plt.ylabel('number of cycles')

	plt.tight_layout()

	plt.savefig('fig/aps_cycle_size_dis.jpg',dpi=200)

	logging.info('cycle size distribution fig saved to fig/aps_cycle_size_dis.jpg')

def cycle_year_difference_distribution(aps_cycles_path,aps_paper_year_path):

	year_differences = defaultdict(int)

	pid_year = json.loads(open(aps_paper_year_path).read())
	for line in open(aps_cycles_path):
		line = line.strip()
		years = []

		for p in line.split(','):
			year = pid_year.get(p,-1)
			if year==-1:
				print p
				continue

			years.append(year)
		if len(years) <2:
			continue

		yd = np.max(years)-np.min(years)

		year_differences[yd]+=1

	xs = []
	ys = []

	for yd in sorted(year_differences.keys()):
		xs.append(yd)
		ys.append(year_differences[yd])

	plt.figure(figsize=(6,5))
	plt.plot(xs,ys,'-o')

	# plt.xscale('log')
	plt.yscale('log')

	plt.xlabel('max time difference in cycle')
	plt.ylabel('number of cycles')

	plt.tight_layout()

	plt.savefig('fig/aps_cycle_year_difference_dis.jpg',dpi=200)

	logging.info('cycle year difference distribution fig saved to fig/aps_cycle_year_difference_dis.jpg')


if __name__ == '__main__':
	# APS_citation_cycles(APS_DATA_PATH)
	citation_cycles_path = 'data/aps_cycles.txt'
	paper_year_path = 'data/APS_paper_year.json'
	# cycle_size_distribution(citation_cycles_path)

	cycle_year_difference_distribution(citation_cycles_path,paper_year_path)










	