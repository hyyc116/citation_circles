
#coding:utf-8

'''
使用cs aminer最简单的aminer进行测试，该数据在自己电脑上

/Users/huangyong/Workspaces/Study/datasets/APS/aps-dataset-citations-2016/aps-dataset-citations-2016.csv

citing_doi,cited_doi
10.1103/PhysRevSeriesI.11.215,10.1103/PhysRevSeriesI.1.1
10.1103/PhysRevSeriesI.17.267,10.1103/PhysRevSeriesI.1.1


#### 问题 有些图很大，但是应该不是cycle，所以为了区分 需要将这个子图转化为无向图 然后判断是不是cycle


'''
from basic_config import *


APS_DATA_PATH = '/Users/huangyong/Workspaces/Study/datasets/APS/aps-dataset-citations-2016/aps-dataset-citations-2016.csv'

### 统计每一篇文章被引的次数
def APS_citation_cycles(aps_citation_network_path,paper_year_path):

	logging.info('loading paper year path ...')

	paper_year = json.loads(open(paper_year_path).read())

	for line in open('data/aps_all_ny_dois_year.txt'):
		line = line.strip()

		ss = line.split()

		paper_year[ss[0]] = int(ss[1])

	logging.info('{:} papers has year attr ...'.format(len(paper_year.keys())))

	logging.info('loading APS citation relations ...')
	aps_references_file = open(aps_citation_network_path)
	aps_references_file.readline()

	edges=[]
	lines = []
	ny_dois = []
	for line in aps_references_file:
		citing_doi,cited_doi = line.strip().split(',')
		if citing_doi == cited_doi:
			continue


		if paper_year.get(citing_doi,-1)==-1:
			ny_dois.append(citing_doi)
			# continue

		if paper_year.get(cited_doi,-1)==-1:
			ny_dois.append(cited_doi)
			# continue

		if paper_year.get(citing_doi,-1)!=-1 and paper_year.get(cited_doi,-1) != -1 and paper_year.get(citing_doi) - paper_year.get(cited_doi) < -3:

			print 'error relation:',citing_doi,paper_year.get(citing_doi),cited_doi,paper_year.get(cited_doi)
			continue

		edges.append([citing_doi,cited_doi])

	logging.info('{:} citation relations are loaded ...'.format(len(edges)))

	G = nx.DiGraph()
	G.add_edges_from(edges)

	logging.info('{:} nodes in citation network, and {:} nodes do not has year attr..'.format(len(G.nodes()),len(set(ny_dois))))

	logging.info('start to detect cycles from aps citation network ...')

	cycles = []
	for comp in nx.strongly_connected_components(G):
		if len(comp)==1:
			continue
		cycles.append(','.join(comp))

	open('data/aps_cycles.txt','w').write('\n'.join(cycles))
	open('data/ny_dois.txt','w').write('\n'.join(list(set(ny_dois))))
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
	num=[]

	pid_year = json.loads(open(aps_paper_year_path).read())

	logging.info('{:} papers year are loaded.'.format(len(pid_year.keys())))

	for line in open(aps_cycles_path):
		line = line.strip()
		years = []
		cycle = line.split(',')
		for p in cycle: 
			year = int(pid_year.get(p,-1))
			if year==-1:
				# print p
				num.append(p)
				continue

			years.append(year)



		if len(years) <2:
			continue

		yd = np.max(years)-np.min(years)
		if len(cycle)>100:
			print len(cycle),yd

		year_differences[yd]+=1
	
	logging.info('{:} of papers are not found.'.format(len(num)))

	open('data/aps_all_ny_dois.txt','w').write('\n'.join(num))

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



def plot_size_10_cycle(aps_citation_network_path,citation_cycles_path):
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

	for line in open(citation_cycles_path):
		line = line.strip()
		cycle = line.split(',')

		# if len(cycle)>5 and len(cycle)<20:
		# 	print cycle
		# 	sg = G.subgraph(cycle)
		# 	subedges = sg.edges
		# 	print subedges
		# 	plot_a_subcascade(subedges,'fig/aps_10/aps10')
		# 	sgraph = nx.DiGraph()
		# 	sgraph.add_edges_from(subedges)
		# 	for i,c in enumerate(nx.simple_cycles(sgraph)):

		# 		plot_a_subcascade(sgraph.subgraph(c).edges,'fig/aps_10/aps10_{:}'.format(i))

		# 	break

	logging.info('Done')


def plot_bigest_scc(citation_cycles_path,paper_year_path,aps_citation_network_path):
	biggest_scc = None
	for line in open(citation_cycles_path):
		line = line.strip()
		cycle = line.split(',')
		if len(cycle)>20:
			biggest_scc = cycle
			break

	logging.info('the size of biggest scc is {:}.'.format(len(biggest_scc)))
	paper_year = json.loads(open(paper_year_path).read())


	for line in open('data/aps_all_ny_dois_year.txt'):
		line = line.strip()

		ss = line.split()

		paper_year[ss[0]] = int(ss[1])

	# biggest_scc = [p for p in biggest_scc if paper_year.get(p,-1)!=-1]

	## plot year distribution of this scc
	logging.info('year distribution ...')
	year_dis = defaultdict(int)
	nys=[]
	for paper in biggest_scc:

		year = int(paper_year.get(paper,-1))

		if year==-1:
			nys.append(paper)
			continue

		year_dis[year]+=1


	logging.info('there are {:} papers without year ...'.format(len(nys)))

	open('data/aps_biggest_ny_dois.txt','w').write('\n'.join(nys))

	xs = []
	ys = []
	for year in sorted(year_dis.keys()):

		xs.append(year)
		ys.append(year_dis[year])

	print xs,ys

	plt.figure(figsize=(6,5))
	plt.plot(xs,ys)

	plt.yscale('log')
	plt.xlabel('year')
	plt.ylabel('number of papers')

	plt.savefig('fig/aps_biggest_year_dis.jpg',dpi=300)

	### plot top 20 subgraph
	logging.info('earliest 20 subgraph ...')
	early_20_papers = sorted(biggest_scc,key=lambda x:paper_year.get(x,-1))

	print early_20_papers

	logging.info('loading APS citation relations ...')
	aps_references_file = open(aps_citation_network_path)
	aps_references_file.readline()

	edges=[]
	for line in aps_references_file:
		citing_doi,cited_doi = line.strip().split(',')

		if citing_doi==cited_doi:
			continue

		if paper_year.get(citing_doi,-1)!=-1 and paper_year.get(cited_doi,-1) != -1 and paper_year.get(citing_doi) - paper_year.get(cited_doi) < -3:

			# print 'error relation:',citing_doi,paper_year.get(citing_doi),cited_doi,paper_year.get(cited_doi)
			continue

		edges.append([citing_doi,cited_doi])


	logging.info('{:} citation relations are loaded ...'.format(len(edges)))

	G = nx.DiGraph()
	G.add_edges_from(edges)

	logging.info('number of papers:{:} ..'.format(len(G.nodes())))

	logging.info("plot edges ...")
	edges = G.subgraph(early_20_papers).edges
	plot_a_subcascade(edges,'fig/biggest_scc/aps_biggest',format='pdf')

	subgraph = nx.DiGraph()
	subgraph.add_edges_from(edges)

	for i,c in enumerate(nx.simple_cycles(subgraph)):

		plot_a_subcascade(subgraph.subgraph(c).edges,'fig/biggest_scc/aps_biggest_{:}'.format(i))

	logging.info('Done')




if __name__ == '__main__':
	citation_cycles_path = 'data/aps_cycles.txt'
	paper_year_path = 'data/APS_paper_year.json'

	# APS_citation_cycles(APS_DATA_PATH,paper_year_path)

	# cycle_size_distribution(citation_cycles_path)

	# cycle_year_difference_distribution(citation_cycles_path,paper_year_path)


	# plot_size_10_cycle(APS_DATA_PATH,citation_cycles_path)
	plot_bigest_scc(citation_cycles_path,paper_year_path,APS_DATA_PATH)






	