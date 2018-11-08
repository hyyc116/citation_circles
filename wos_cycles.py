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


    open('data/sccs_{:}.txt_bak'.format(field),'w').write('\n'.join(sccs))

    logging.info('Sccs saved to data/sccs_{:}.txt_bak.'.format(field))


## cycle大小的分布
def cycle_size_distribution(pathObj):
    # cycles = []
    cycles_path = pathObj._sccs

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

    plt.savefig('fig/{:}_cycle_size_dis.jpg'.format(pathObj._name),dpi=200)

    logging.info('cycle size distribution fig saved to fig/{:}_cycle_size_dis.jpg'.format(pathObj._name))


def cycle_year_difference_distribution(pathObj):

    # field = '_'.join(field.split())
    cycles_path = pathObj._sccs
    paper_year_path = pathObj._years

    year_differences = defaultdict(int)
    num=[]

    pid_year = json.loads(open(paper_year_path).read())

    logging.info('{:} papers year are loaded.'.format(len(pid_year.keys())))

    yd_years = defaultdict(int)
    for line in open(cycles_path):
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
        
        if yd > 0:
            logging.info('yd:{:},size:{:}'.format(yd,len(years)))

        else:
            yd_years[years[0]]+=1


        year_differences[yd]+=1
    
    logging.info('{:} of papers are not found.'.format(len(num)))

    # open('data/aps_all_ny_dois.txt','w').write('\n'.join(num))

    xs = []
    ys = []

    for yd in sorted(year_differences.keys()):
        xs.append(yd)
        ys.append(year_differences[yd])

    plt.figure(figsize=(7,5))
    plt.plot(xs,ys,'-o')

    # plt.xscale('log')
    plt.yscale('log')

    plt.xlabel('max time difference in cycle')
    plt.ylabel('number of cycles')

    plt.tight_layout()

    plt.savefig('fig/{:}_cycle_year_difference_dis.jpg'.format(pathObj._name),dpi=200)

    logging.info('cycle year difference distribution fig saved to fig/{:}_cycle_year_difference_dis.jpg'.format(pathObj._name))


    xs = []
    ys = []

    for year in sorted(yd_years.keys()):
        xs.append(year)
        ys.append(yd_years[year])

    plt.figure(figsize=(7,5))
    plt.plot(xs,ys,'-o')

    # plt.xscale('log')
    plt.yscale('log')

    plt.xlabel('year')
    plt.ylabel('number of cycles')

    plt.tight_layout()

    plt.savefig('fig/{:}_cycle_year_dis.jpg'.format(pathObj._name),dpi=200)

    logging.info('cycle year distribution fig saved to fig/{:}_cycle_year_dis.jpg'.format(pathObj._name))


### 根据citation network, 年份, scc生成SCC的citation network的数据和对应节点的年份
def scc_network(field):

    field = '_'.join(field.split())
    cycles_path = 'data/sccs_{:}.txt'.format(field)
    paper_year_path = 'data/year_{:}.json'.format(field)
    citation_network_path = 'data/citation_network_{:}.txt'.format(field)

    paper_year = json.loads(open(paper_year_path).read())

    ## 首先得到所有在scc中的文章节点
    pids = []

    for line in open(cycles_path):
        line = line.strip()
        pids.extend(line.split(','))

    pids = set(pids)
    logging.info('there are {:} papers in sccs'.format(len(pids)))


    ### 或者所有文章相关的citation relations
    scc_relations = []

    ##SCC中本学科的年份
    scc_node_year = {}
    for line in open(citation_network_path):

        line = line.strip()

        citing_pid,cited_pid = line.split(',')


        if citing_pid in pids and cited_pid in pids:

            if citing_pid == cited_pid:
                continue

            ## 把所有没有年份的，就是本学科之外的删除，所有本学科的都有年份
            if paper_year.get(citing_pid,-1)==-1:
                continue

            if paper_year.get(cited_pid,-1)==-1:
                continue

            ## 本学科的年份
            scc_node_year[citing_pid] = paper_year[citing_pid]
            scc_node_year[cited_pid] = paper_year[cited_pid]


            scc_relations.append(line)

    open('data/scc_relations_{:}.txt'.format(field),'w').write('\n'.join(scc_relations))

    logging.info('scc relations saved to data/scc_relations_{:}.txt'.format(field))

    open('data/scc_year_{:}.txt'.format(field),'w').write(json.dumps(scc_node_year))

    logging.info('scc node year saved to data/scc_year_{:}.txt'.format(field))

## 根据scc network以及年份， 去掉被引-引证年份<-3的论文

def new_from_scc_network(field):
    field = '_'.join(field.split())

    scc_relations_path = 'data/scc_relations_{:}.txt'.format(field)
    scc_year_path = 'data/scc_year_{:}.txt'.format(field)

    scc_year = json.loads(open(scc_year_path).read())

    edges = []
    for line in open(scc_relations_path):
        line = line.strip()

        citing_pid,cited_pid = line.split(',')

        ## 如果被引文献比引证文献晚3年以上
        if int(scc_year[cited_pid]) - int(scc_year[citing_pid]) >= 3:
            continue

        edges.append([citing_pid,cited_pid])

    logging.info('{:} filtered edges...'.format(len(edges)))
    ## 根据过滤之后的node进行构建network

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



###随机选择100个SCC查证准确率
def check_accuracy_of_scc(pathObj):

    edges = []

    for line in open(pathObj._relations):

        line = line.strip()

        citing_pid,cited_pid = line.split(',')

        edges.append([citing_pid,cited_pid])

    ## 创建graph

    dig = nx.DiGraph()
    dig.add_edges_from(edges)

    logging.info('total directed graph created success.')

    ## 根据scc进行subgraph的可视化
    lines = [line.strip() for line in open(pathObj._sccs)]

    _100_sccs = np.random.choice(lines,100)

    open(pathObj._random_100,'w').write('\n'.join(_100_sccs))

    ## 可视化100个子图
    for i,scc in enumerate(_100_sccs):

        scc = scc.split(',')

        logging.info('plot subgraph {:} ...'.format(i))
        ## 子图
        subgraph = dig.subgraph(scc)

        # print subgraph.edges
        ## 对每个subgraph进行可视化
        plot_a_subcascade(subgraph.edges,pathObj._subgraph+str(i),format='pdf')

    logging.info('finished')



### 构建特定领域的引文网络
def generate_cc_of_field(field):
    filter_ids_of_field(field)
    _ids_path = 'data/selected_IDs_from_{:}.txt'.format('_'.join(field.split()))
    fetch_citation_network(_ids_path,field)


if __name__ == '__main__':



    if int(sys.argv[1])==0:

        ## 构建citation network
        # generate_cc_of_field('physics')

        ## 第一轮生成scc
        # find_scc_from_citation_network('physics')

        ## 获得该领域论文的published year
        # fecth_pubyear_of_com_ids('physics')

        # ## 根据 scc获得network的子集,以及published year的子集以便于下载
        # scc_network('physics')

        # ## 根据子集过滤掉中其领域的文章以及cited_paper比citing paper晚三年的关系，生成新的scc
        # new_from_scc_network('physics')

        pathObj = PATHS('physics')

        check_accuracy_of_scc(pathObj)

        ## SCC的size 分布
        cycle_size_distribution(pathObj)

        ## SCC的最大年份差分布，以及0年的时间分布
        cycle_year_difference_distribution(pathObj)


    else:

        ## 构建citation network
        # generate_cc_of_field('computer science')

        ## 第一轮生成scc
        # find_scc_from_citation_network('computer science')

        ## 获得该领域论文的published year
        # fecth_pubyear_of_com_ids('computer science')


        # ## 根据 scc获得network的子集,以及published year的子集以便于下载
        # scc_network('computer science')

        # ## 根据子集过滤掉中其领域的文章以及cited_paper比citing paper晚三年的关系，生成新的scc
        # new_from_scc_network('computer science')


        pathObj = PATHS('computer science')

        check_accuracy_of_scc(pathObj)

        ## SCC的size 分布
        cycle_size_distribution(pathObj)

        ## SCC的最大年份差分布，以及0年的时间分布
        cycle_year_difference_distribution(pathObj)













  
