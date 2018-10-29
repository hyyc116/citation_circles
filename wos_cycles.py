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
    logging.info('filter out paper ids from wos_subjects of field:[{:}].'.format(field))
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
    saved_path = 'data/selected_IDs_from_{:}.txt'.format(field)
    open(saved_path,'w').write('\n'.join(selected_IDs))
    logging.info('number of papers belong to field [{:}] is [{:}] out of total {:} papers, and saved to {:}.'.format(field,len(selected_IDs),progress,saved_path))


    open('data/{:}_subjects.txt'.format(field),'w').write('\n'.join(sorted(list(set(subjects)))))

    logging.info('subjects used saved to {:}_subjects.txt.'.format(field))
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
    f = open('data/citation_network_{:}.txt'.format(field),'w+')
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

### 构建特定领域的引文网络
def generate_cc_of_field(field):
    filter_ids_of_field(field)
    _ids_path = 'data/selected_IDs_from_{:}.txt'.format(field)
    fetch_citation_network(_ids_path,field)

if __name__ == '__main__':

    generate_cc_of_field('physics')

    generate_cc_of_field('computer science')


    













  
