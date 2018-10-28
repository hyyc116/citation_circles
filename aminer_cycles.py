#coding:utf-8

'''
使用cs aminer最简单的aminer进行测试，该数据在53服务器上有

/public/data/Aminer_MAG/Aminer/aminer_reference.json 

{
"RECORDS":[
{
"id":1,
"cpid":10, citing paper id
"pid":289259, cited paper id
"pid_vid":131641,
"pid_year":1980,
"cpid_year":1984
},
...
}

'''
from basic_config import *

## 生成引文网络
## 存到文件里，每一行是一对引用关系 citing_pid -> cited_pid
def generate_citation_network(aminer_ref_json_file):

	ref_json = json.loads(open(aminer_ref_json_file).read())
	lines = []
	## 文章发表年
	pid_year = {}
	progress = 0
	for obj in ref_json['RECORDS']:

		progress+=1

		if progress%10000==0:
			logging.info('progress {:} ...'.format(progress))


		line= '{:},{:}'.format(obj['cpid'],obj['pid'])
		lines.append(line)

		pid_year[obj['cpid']] = obj['cpid_year']
		pid_year[obj['pid']] = obj['pid_year']


	open('data/aminer_citation_network.txt','w').write('\n'.join(lines))
	logging.info('citation network saved to data/aminer_citation_network.txt.')
	# pass

	open('data/aminer_paper_year.json','w').write(json.dumps(pid_year))

	logging.info('paper year json saved to data/aminer_paper_year.json.')



def detect_cycle_from_aminer(aminer_citation_network_path):
	edges = []

	for line in open(aminer_citation_network_path):
		line = line.strip()

		citing_pid,cited_pid = line.split(',')

		edges.append([citing_pid,cited_pid])

	G = nx.DiGraph()
	G.add_edges_from(edges)

	cycles = []
	for comp in nx.strongly_connected_components(G):
		cycles.append(','.join(comp))


	open('data/aminer_cycles.txt','w').write('\n'.join(cycles))
	logging.info('aminer cycles saved to data/aminer_cycles.txt')

if __name__ == '__main__':
	
	# generate_citation_network('/public/data/Aminer_MAG/Aminer/aminer_reference.json')

	detect_cycle_from_aminer('data/aminer_citation_network.txt')



