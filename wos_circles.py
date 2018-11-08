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

    for line in open(pathObj._CRs):
        cr = line.strip()
        citing_pid,cited_pid = cr.split(',')
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


if __name__ == '__main__':

    if int(sys.argv[1])==0:

        pathObj = PATHS('physics')

        statistics_of_cc(pathObj)

    else:

        pathObj = PATHS('computer science')

        statistics_of_cc(pathObj)







