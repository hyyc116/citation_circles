#coding:utf-8

'''
定义程序中所有可能用到的路径信息

'''

### 定义所有的
class PATHS:

    def __init__(self,field):

        ## 领域名
        self._field = field

        ## 保存的名
        self._name = '_'.join(field.split())

        if field=='physics':
            self._dataset = 'WOS-P'
        else:
            self._dataset = 'WOS-CS'

        ## 各个领域所属文章的ID列表文件
        self._IDs = 'data/selected_IDs_from_{:}.txt'.format(self._name)

        ## 领域内引用关系的列表文件
        self._CRs = 'data/citation_network_{:}.txt'.format(self._name)

        ## 被引论文比引证文献晚发表三年的列表
        self._3_yds = 'data/three_yd_{:}.txt'.format(self._name)

        ## 领域内所有文章的JSON文件
        self._YearJson = 'data/year_{:}.json'.format(self._name)

        ##强联通量的存放文件,去掉三年以后的结果
        self._sccs = 'data/sccs_{:}.txt'.format(self._name)
        ## 没有去掉三年的结果
        self._sccs_bak = 'data/sccs_{:}.txt_bak'.format(self._name)
        ## 对比的Size图
        self._compare_size = 'fig/scc_size_compare_{:}.jpg'.format(self._name)


        ## 强连通量中节点相关的文件
        self._relations = 'data/scc_relations_{:}.txt'.format(self._name)

        ##强联通量的年份
        self._years = 'data/scc_year_{:}.txt'.format(self._name)


        ### 四个统计量的图形位置
        self._stats_fig = 'fig/scc_stats_{:}.jpg'.format(self._name)
        self._stats_fig_data = 'fig/data/scc_stats_data_{:}.json'.format(self._name)

        ## pattern的统计量
        self._id_patterns = 'data/scc_id_patterns_{:}.json'.format(self._name)
        self._id_attrs = 'data/scc_id_attr_{:}.json'.format(self._name)
        self._top_patterns = 'fig/patterns/scc_pattern_{:}_'.format(self._name)
        self._top_yds = 'fig/yds/scc_yd_{:}_'.format(self._name)
        self._top_cs = 'fig/cs/scc_cs_{:}_'.format(self._name)
        self._csv = 'data/scc_csv_{:}.csv'.format(self._name)
        self._table = 'scc_table_{:}.html'.format(self._name)


        ## 强联通量的子图存放地址
        self._subgraph = 'fig/subgraph/scc_subgraph_{:}_'.format(self._name)

        ## 随机100个SCC的地址
        self._random_100 = 'data/scc_rn100_{:}.txt'.format(self._name)


        ### author,期刊，机构的对应关系数据
        self._authors = 'data/scc_authors_{:}.json'.format(self._name)
        self._journals = 'data/scc_journals_{:}.json'.format(self._name)
        self._orgs = 'data/scc_orgs_{:}.json'.format(self._name)
        self._social = 'data/scc_social_{:}.txt'.format(self._name)







