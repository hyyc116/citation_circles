#coding:utf-8

from basic_config import *

'''
在WOS的数据集上进行操作

1. 首先得到不同领域文章的ID

2. 根据ID得到他们之间的citation network

3. 探测 citation network的强连通分量


'''

#### 根据关键词过滤领域中的论文
def filter_ids_of_field(field):
    logging.info('filter out paper ids from wos_subjects of field:[{:}].'.format('_'.join(field.split())))
    selected_IDs = []
    
    ## query database 
    query_op = dbop()

    sql = 'select id,subject from wos_subjects'

    progress = 0
    subjects = []
    for fid,subject in query_op.query_database(sql):
        progress+=1
        if progress%10000000==0:
            logging.info('progress {:} .... ' .format(progress))

            
        if field in subject.lower():
            selected_IDs.append(str(fid))
            subjects.append(subject.lower())

    query_op.close_db()
    selected_IDs = list(set(selected_IDs))
    saved_path = 'data/selected_IDs_from_{:}.txt'.format('_'.join(field.split()))
    open(saved_path,'w').write('\n'.join(selected_IDs))
    logging.info('number of papers belong to field [{:}] is [{:}] out of total {:} papers, and saved to {:}.'.format(field,len(selected_IDs),progress,saved_path))


    open('data/{:}_subjects.txt'.format('_'.join(field.split())),'w').write('\n'.join(sorted(list(set(subjects)))))

    logging.info('subjects used saved to {:}_subjects.txt.'.format('_'.join(field.split())))
    logging.info('ID filter done.')

## 根据过滤得到的领域文章，构建citation network
def fetch_citation_network(selected_IDs_path,field):
    logging.info('fetch citing papers of selected IDs ...')


    selected_IDs = set([line.strip() for line in open(selected_IDs_path)])

    logging.info('{:} selected IDs from {:}.'.format(len(selected_IDs),selected_IDs_path))


    total = len(selected_IDs)

    query_op = dbop()
    sql = 'select id,ref_id from wos_references'
    progress=0
    # sub_progress = 0
    # citing_IDs = []

    # has_citations = []

    lines = []
    f = open('data/citation_network_{:}.txt'.format('_'.join(field.split())),'w+')
    num_of_relations = 0
    for pid,ref_id in query_op.query_database(sql):
        progress+=1
        if progress%10000000==0:
            logging.info('total progress {:} ...'.format(progress))
        
        if ref_id in selected_IDs or pid in selected_IDs:
            lines.append('{:},{:}'.format(pid,ref_id))

            num_of_relations+=1
            # has_citations.append(ref_id)
            # citing_IDs.append(pid)

            if len(lines)%10000==0:
                # logging.info(' {:} ...'.format(progress))
                f.write('\n'.join(lines)+'\n')
                lines = []

    if len(lines)!=0:
        f.write('\n'.join(lines))

    f.close()

    logging.info('{:} citation relations in citation network saved to data/citation_network_{:}.txt.'.format(num_of_relations,field))

    query_op.close_db()

def fecth_pubyear_of_com_ids(field):
    field = '_'.join(field.split())
    com_IDs_path = 'data/selected_IDs_from_{:}.txt'.format(field)
    com_IDs = set([line.strip() for line in open(com_IDs_path)])
    logging.info('fetch published year of {:} combine ids'.format(len(com_IDs)))
    com_ids_year = {}

    ## query database wos_summary
    query_op = dbop()
    sql = 'select id,pubyear from wos_summary'
    progress=0
    for pid,pubyear in query_op.query_database(sql):
        progress+=1
        if progress%1000000==0:
            logging.info('progress {:} ...'.format(progress))
        if pid in com_IDs:
            com_ids_year[pid] = pubyear

    query_op.close_db()
    logging.info('{:} cited ids have year.'.format(len(com_ids_year.keys())))
    open('data/year_{:}.json'.format(field),'w').write(json.dumps(com_ids_year))
    # return com_ids_year

def find_scc_from_citation_network(field):

    logging.info('start to load citation relations ...')
    field = '_'.join(field.split())
    citation_network_path = 'data/citation_network_{:}.txt'.format(field)

    edges = []
    progress = 0
    for line in open(citation_network_path):
        line = line.strip()

        progress+=1

        if progress%1000000==0:
            logging.info('progress {:} ...'.format(progress))

        citing_pid,cited_pid = line.split(',')

        if citing_pid==cited_pid:
            continue

        edges.append([citing_pid,cited_pid])


    logging.info('{:} citation relations are loaded ...'.format(len(edges)))


    logging.info('start to generate directed graph ...')
    cc = nx.DiGraph()
    cc.add_edges_from(edges)

    logging.info('directed graph created ...')

    logging.info('start to detect strongly connected components ...')

    sccs = []
    for c in nx.strongly_connected_components(cc):
        if len(c)==1:
            continue
        sccs.append(','.join(c))

    logging.info('Scc detection complete, {:} sccs are detected.'.format(len(sccs)))


    open('data/sccs_{:}.txt'.format(field),'w').write('\n'.join(sccs))

    logging.info('Sccs saved to data/sccs_{:}.txt.'.format(field))


## cycle大小的分布
def cycle_size_distribution(field):
    # cycles = []
    field = '_'.join(field.split())
    cycles_path = 'data/sccs_{:}.txt'.format(field)
    size_dis = defaultdict(int)
    for line in open(cycles_path):

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

    plt.savefig('fig/{:}_cycle_size_dis.jpg'.format(field),dpi=200)

    logging.info('cycle size distribution fig saved to fig/{:}_cycle_size_dis.jpg'.format(field))


### 构建特定领域的引文网络
def generate_cc_of_field(field):
    filter_ids_of_field(field)
    _ids_path = 'data/selected_IDs_from_{:}.txt'.format('_'.join(field.split()))
    fetch_citation_network(_ids_path,field)


if __name__ == '__main__':

    # generate_cc_of_field('physics')

    # generate_cc_of_field('computer science')

    if int(sys.argv[1])==0:

        # find_scc_from_citation_network('physics')

        fecth_pubyear_of_com_ids('physics')

        cycle_size_distribution('physics')

    else:

        # find_scc_from_citation_network('computer science')

        # fecth_pubyear_of_com_ids('computer science')

        cycle_size_distribution('computer science')



    













  
