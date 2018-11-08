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
def scc_stats(pathObj):

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
    ax0.set_xlabel('size of SCC')
    ax0.set_ylabel('number of SCC')
    ax0.set_title('before removing')


    ax1 = axes[1]
    sccs =[line.strip().split(',') for line in open(pathObj._sccs)]

    sizes = [len(scc) for scc in sccs]

    size_dict = Counter(sizes)

    size_xs = []
    size_ys = []
    for size in sorted(size_dict.keys()):
        size_xs.append(size)
        size_ys.append(size_dict[size])

    ax1.plot(size_xs,size_ys,'-o')
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    ax1.set_xlabel('size of SCC')
    ax1.set_ylabel('number of SCC')
    ax1.set_title('before removing')

    plt.tight_layout()
    plt.savefig(pathObj._compare_size)


if __name__ == '__main__':

    if int(sys.argv[1])==0:

        pathObj = PATHS('physics')

    else:

        pathObj = PATHS('computer science')

    # statistics_of_cc(pathObj)
    scc_stats(pathObj)







