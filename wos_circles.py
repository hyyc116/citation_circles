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

    fig,axes = plt.subplots(4,1,figsize=(6,20))

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
    fig_data['title'] = 'Size of SCC'
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
    for scc in sccs:
        years = []
        for pid in scc:
            years.append(int(yearJson[pid]))

        yd = np.max(years)-np.min(years)


        my = np.min(years)

        yd_year_count[yd][my]+=1

        yds.append(yd)

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
    fig_data['xscale'] = 'log'
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
    # fig_data['yscale'] = 'log'
    # fig_data['marker'] = '-o'

    xlist = []
    ylist = []
    markers = []
    labels = []
    for i,yd in enumerate(sorted(yd_year_count.keys())):

        markers.append(_ALL_MARKERS[i])
        year_count = yd_year_count[yd]
        labels.append('N={:}'.format(yd))

        xs = []
        ys = []
        for year in sorted(year_count.keys()):
            xs.append(year)
            ys.append(year_count[year])

        xlist.append(xs)
        ylist.append(ys)

    fig_data['xses'] = xlist
    fig_data['yses'] = ylist
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
    fig_data['yscale'] = 'log'
    fig_data['marker'] = 'o'

    plot_line_from_data(fig_data,ax3)
    data.append(fig_data)

    plt.tight_layout()

    plt.savefig(pathObj._stats_fig,dpi=300)
    logging.info('fig saved to {:}.'.format(pathObj._stats_fig))


    open(pathObj._stats_fig_data,'w').write(json.dumps({'data':data}))
    logging.info('data of fig saved to {:}.'.format(pathObj._stats_fig_data))



if __name__ == '__main__':

    if int(sys.argv[1])==0:

        pathObj = PATHS('physics')

    else:

        pathObj = PATHS('computer science')

    # statistics_of_cc(pathObj)
    # scc_compare(pathObj)
    scc_stats(pathObj)






