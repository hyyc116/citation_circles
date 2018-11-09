#coding:utf-8
'''
citation circle的实验，第二次重新实验，将所有的数据都记录下来

'''

from basic_config import *


'''

引用网络中的节点数量，边的数量输出

'''
def statistics_of_cc(pathObj):
    logging.info('stat dataset ...')

    _IDs = [_id.strip() for _id in open(pathObj._IDs)]
    logging.info('there are {:} articles in domain {:}.'.format(len(_IDs),pathObj._field))

    ## 加载年份数据
    yearJson = json.loads(open(pathObj._YearJson).read())
    logging.info('there are {:} articles has year tag.'.format(len(yearJson.keys())))

    ## 加载引用关系
    ## 引用的数量
    num_of_crs = 0
    ## 引用差大于三年的数量
    num_of_3_df_crs = []

    progress = 0
    for line in open(pathObj._CRs):
        cr = line.strip()

        progress+=1

        if progress%1000000==0:

            logging.info('progress {:} ...'.format(progress))

        citing_pid,cited_pid = cr.split(',')

        if citing_pid == cited_pid:
            continue

        citing_year = int(yearJson.get(citing_pid,-1))
        cited_year = int(yearJson.get(cited_pid,-1))

        if citing_year ==-1 or cited_year==-1:
            continue

        if cited_year - citing_year >=3:
            num_of_3_df_crs.append(cr)

        num_of_crs+=1


    logging.info('number of citation relations is {:}, in which {:} citation relations exist.'.format(num_of_crs,len(num_of_3_df_crs)))

    open(pathObj._3_yds,'w').write('\n'.join(num_of_3_df_crs))

    logging.info('citation relations with 3 year differences are saved to {:}.'.format(pathObj._3_yds))

## 直接抽取SCC之后SCC的Size以及年份差异，去掉三年YD的引用关系之后的结果
def scc_compare(pathObj):

    fig,axes = plt.subplots(1,2,figsize=(10,5))

    ax0 = axes[0]
    sccs_bak =[line.strip().split(',') for line in open(pathObj._sccs_bak)]

    sizes = [len(scc) for scc in sccs_bak]

    size_dict = Counter(sizes)

    size_xs = []
    size_ys = []
    for size in sorted(size_dict.keys()):
        size_xs.append(size)
        size_ys.append(size_dict[size])

    ax0.plot(size_xs,size_ys,'-o')
    ax0.set_xscale('log')
    ax0.set_yscale('log')
    ax0.set_xlabel('size of SCC\n(a)')
    ax0.set_ylabel('number of SCC')
    ax0.set_title('original ({:})'.format(pathObj._dataset))


    ax1 = axes[1]
    sccs =[line.strip().split(',') for line in open(pathObj._sccs)]

    sizes = [len(scc) for scc in sccs]

    size_dict = Counter(sizes)

    size_xs = []
    size_ys = []
    # total_num = 0
    for size in sorted(size_dict.keys()):
        size_xs.append(size)
        size_ys.append(size_dict[size])

    ax1.plot(size_xs,size_ys,'-o')
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    ax1.set_xlabel('size of SCC\n(b)')
    ax1.set_ylabel('number of SCC')
    ax1.set_title('processed ({:})'.format(pathObj._dataset))

    logging.info('total number of papers in SCC is {:}.'.format(np.sum(sizes)))


    plt.tight_layout()
    plt.savefig(pathObj._compare_size)


##所有的统计量画在一起
def scc_stats(pathObj):

    logging.info("start to draw stats fig ...")

    fig,axes = plt.subplots(4,1,figsize=(6,16))

    data = []
    logging.info('Distribution of SCC Size ...')
    ## SCC size的分布
    ax0 = axes[0]
    sccs = [line.strip().split(',') for line in open(pathObj._sccs)]

    sizes = [len(scc) for scc in sccs]


    size_dict = Counter(sizes)

    xs = []
    ys = []
    for size in sorted(size_dict.keys()):
        xs.append(size)
        ys.append(size_dict[size])

    fig_data = {}
    fig_data['x'] = xs
    fig_data['y'] = ys
    fig_data['title'] = '\n\nSize of SCC'
    fig_data['xlabel'] = 'Size of SCC\n(a)'
    fig_data['ylabel'] = 'Number of SCC'
    fig_data['xscale'] = 'log'
    fig_data['yscale'] = 'log'
    fig_data['marker'] = '-o'
    plot_line_from_data(fig_data,ax0)
    data.append(fig_data)


    logging.info('Year difference ....')
    ## year difference
    ax1 = axes[1]
    yearJson = json.loads(open(pathObj._years).read())

    yds = []
    yd_year_count = defaultdict(lambda:defaultdict(int))
    sizes=[]
    for scc in sccs:
        years = []
        for pid in scc:
            years.append(int(yearJson[pid]))

        yd = np.max(years)-np.min(years)


        my = np.min(years)

        yd_year_count[yd][my]+=1

        yds.append(yd)
        sizes.append(len(scc))

    yd_dict = Counter(yds)

    xs = []
    ys = []

    for yd in sorted(yd_dict.keys()):

        xs.append(yd)
        ys.append(yd_dict[yd])

    fig_data = {}
    fig_data['x'] = xs
    fig_data['y'] = ys
    fig_data['title'] = 'Year Difference'
    fig_data['xlabel'] = 'Year Differnece\n(b)'
    fig_data['ylabel'] = 'Number of SCC'
    # fig_data['xscale'] = 'log'
    fig_data['yscale'] = 'log'
    fig_data['marker'] = '-o'
    fig_data['xtick'] = True
    plot_line_from_data(fig_data,ax1)
    data.append(fig_data)


    logging.info('num dis over year ...')
    ## 不同yd随YEAR时间的变化
    ax2 = axes[2]
    fig_data = {}
    # fig_data['x'] = xs
    # fig_data['y'] = ys
    fig_data['title'] = 'Number distribution over year'
    fig_data['xlabel'] = 'year\n(c)'
    fig_data['ylabel'] = 'Number of SCC'
    # fig_data['xscale'] = 'log'
    fig_data['yscale'] = 'log'
    # fig_data['marker'] = '-o'

    xlist = []
    ylist = []
    markers = []
    labels = []
    for i,yd in enumerate(sorted(yd_year_count.keys())):

        markers.append(ALL_MARKERS[i])
        year_count = yd_year_count[yd]
        labels.append('N={:}'.format(yd))

        xs = []
        ys = []
        for year in sorted(year_count.keys()):
            xs.append(year)
            ys.append(year_count[year])

        xlist.append(xs)
        ylist.append(ys)

    fig_data['xs'] = xlist
    fig_data['ys'] = ylist
    fig_data['markers'] = markers
    fig_data['labels'] = labels
    plot_multi_lines_from_two_data(fig_data,ax2)
    data.append(fig_data)


    ##
    logging.info('scatter plot ...')
    ## SIZE和YD的散点图

    ax3 = axes[3]
    fig_data = {}
    fig_data['x'] = sizes
    fig_data['y'] = yds
    fig_data['title'] = 'Relations'
    fig_data['xlabel'] = 'Size of SCC\n(d)'
    fig_data['ylabel'] = 'Year Differnece'
    fig_data['xscale'] = 'log'
    # fig_data['yscale'] = 'log'
    fig_data['marker'] = 'o'
    # fig_data['xtick']=True

    plot_scatter_from_data(fig_data,ax3)
    data.append(fig_data)

    plt.suptitle(pathObj._dataset,fontsize=20,weight='bold')

    plt.tight_layout()

    plt.savefig(pathObj._stats_fig,dpi=300)
    logging.info('fig saved to {:}.'.format(pathObj._stats_fig))


    open(pathObj._stats_fig_data,'w').write(json.dumps({'data':data}))
    logging.info('data of fig saved to {:}.'.format(pathObj._stats_fig_data))


##iso_pattern
def iso(pattern_id,_id_pattern,graph):

    num_of_pattern = len(_id_pattern.keys())

    # size = len(graph.nodes())
    # pat_id  = pattern_id.get(size,{})
    is_iso = False
    for pattern in pattern_id.keys():
        if nx.is_isomorphic(graph,pattern):
            is_iso=True
            _id = pattern_id[pattern]
            break

    if not is_iso:
        _id = num_of_pattern
        pattern_id[graph] = _id
        _id_pattern[_id] = list(graph.edges())

    return pattern_id,_id_pattern,_id


## 对SCC的pattern进行分析
def scc_patterns(pathObj):

    yearJson = json.loads(open(pathObj._years).read())

    sccs = [line.strip().split(',') for line in open(pathObj._sccs)]

    edges = [line.strip().split(',') for line in open(pathObj._relations)]

    dig = nx.DiGraph()
    dig.add_edges_from(edges)

    pattern_id = defaultdict(int)
    _id_pattern = {}

    _id_attrs = defaultdict(list)
    progress = 0
    for scc in sccs:

        progress+=1

        if progress%10==0:

            logging.info('progress {:} ...'.format(progress))

        size = len(scc)

        if size >10:
            continue

        years = [int(yearJson[pid]) for pid in scc]
        yd = np.max(years)-np.min(years)

        subgraph = nx.DiGraph()
        subgraph.add_edges_from(list(dig.subgraph(scc).edges))

        ## simple circles
        circle_sizes = []
        for circle in nx.simple_cycles(subgraph):
            circle_sizes.append(len(circle))

        pattern_id,_id_pattern,_id = iso(pattern_id,_id_pattern,subgraph)

        _id_attrs[_id].append([size,yd,circle_sizes])

    open(pathObj._id_patterns,'w').write(json.dumps(_id_pattern))
    logging.info('{:} patterns saved to {:}.'.format(len(_id_pattern.keys()),pathObj._id_patterns))
    open(pathObj._id_attrs,'w').write(json.dumps(_id_attrs))
    logging.info('id attrs saved to {:}.'.format(pathObj._id_attrs))

### 把频次最高的20个pattern画出来
def top_pattern_plot(pathObj):

    _id_pattern = json.loads(open(pathObj._id_patterns).read())
    _id_attrs = json.loads(open(pathObj._id_attrs).read())

    ###出现频次最高的20个
    lines = ['|index|pattern_path|freq|size|year difference|circle size|','| ------: | :------: | ------: | ------: | :------: | :------: |']
    # html = '<table>'
    # html+='<tr> <td>index</td> <td>pattern</td> <td>Frequency</td> <td>Size</td> <td>YD Distribution</td> <td>Citation Circle</td></tr>'
    for i,_id in enumerate(sorted(_id_attrs.keys(),key=lambda x:len(_id_attrs[x]),reverse=True)[:20]):

        logging.info('plot {:}th pattern ...'.format(i))

        ## 出现的次数
        attrs = _id_attrs[_id]
        freq = len(attrs)
        _s,yds,cses = zip(*attrs)
        edges = _id_pattern[_id]

        plot_a_subcascade(edges,pathObj._top_patterns+str(i),shape='point',format='jpg')

        ##pattern的路径
        pattern_path = pathObj._top_patterns+str(i)+'.jpg'

        ## size
        dig = nx.DiGraph()
        dig.add_edges_from(edges)
        size = len(dig.nodes())

        ##year difference distribution
        yd_dict = Counter(yds)
        xs = []
        ys = []
        for yd in [0,1,2,3]:
            xs.append(yd)
            ys.append(yd_dict.get(yd,0))


        fig_data = {}
        fig_data['x'] = xs
        fig_data['y'] = ys
        fig_data['xlabel'] = 'year difference'
        fig_data['ylabel'] = 'number of SCCs'
        fig_data['yscale'] = 'log'
        plt.figure(figsize=(4,3))
        plot_bar_from_data(fig_data)
        # plt.tight_layout()
        yd_path = pathObj._top_yds+str(i)+".jpg"
        plt.savefig(yd_path,dpi=300)


        ## circle size distribution
        cs = cses[0]
        cs_dict = Counter(cs)

        xs = []
        ys = []
        for c in [2,3,4]:
            xs.append(c)
            ys.append(cs_dict.get(c,0))

        fig_data = {}
        fig_data['x'] = xs
        fig_data['y'] = ys
        fig_data['xlabel'] = 'circle size'
        fig_data['ylabel'] = 'number of circles'
        # fig_data['yscale'] = 'log'
        plt.figure(figsize=(4,3))
        plot_bar_from_data(fig_data)
        # plt.tight_layout()
        cs_path = pathObj._top_cs+str(i)+".jpg"
        plt.savefig(cs_path,dpi=300)


        line = '|{:}|![pattern]({:})|{:}|{:}|![yd]({:})|![cs]({:})|'.format(i,pattern_path,freq,size,yd_path,cs_path)

        lines.append(line)

        # html+='<tr> <td>{:}</td> <td><src="{:}" width=100 height=50 alt="pattern figure"/></td> <td>{:}</td> <td>{:}</td> <td><src="{:}" width=100 height=50 alt="YD figure"/></td> <td><src="{:}" width=100 height=50 alt="CS figure"/></td></tr>'.format(i,pattern_path,freq,size,yd_path,cs_path)


    # html+='</table>'
    open(pathObj._csv,'w').write('\n'.join(lines))
    logging.info('csv data saved to {:}.'.format(pathObj._csv))

    # open(pathObj._table,'w').write(html)
    # logging.info('table saved to {:}.'.format(pathObj._table))






if __name__ == '__main__':

    if int(sys.argv[1])==0:

        pathObj = PATHS('physics')

    else:

        pathObj = PATHS('computer science')

    # statistics_of_cc(pathObj)
    # scc_compare(pathObj)
    # scc_stats(pathObj)
    # scc_patterns(pathObj)
    top_pattern_plot(pathObj)






