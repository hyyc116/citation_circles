#coding:utf-8
'''
文章的作者，期刊，机构之间的关系图

'''

from basic_config import *


##首先需要获得

def get_social_attrs(pathObj):

    sccs = [line.strip().split(',') for line in open(pathObj._sccs)]

    pids = set([_id for _ids in sccs for _id in _ids ])

    logging.info('there are {:} unique papers in scc.'.format(len(pids)))

    ### 在数据库中遍历找到作者、期刊、机构
    query_op = dbop()
    sql = 'select id,title where title_id=6'
    pid_journal = {}
    progress = 0
    for pid,journal in query_op.query_database(sql):
        progress+=1

        if progress%10000000==0:
            logging.info('journal progress  {:} ...'.format(progress))


        if pid in pids:
            pid_journal[pid] = journal

    logging.info('{:} papers has journal info ...'.format(len(pid_journal.keys())))

    open(pathObj._journals,'w').write(json.dumps(pid_journal))
    logging.info('journal info  saved to {:}...'.format(pathObj._journals))



    sql = 'select id,full_name,seq_no from wos_summary_names where role=\'author\''

    pid_seq_author=defaultdict(dict)
    progress = 0
    for pid,author,seq_no in query_op.query_database(sql):

        progress+=1

        if progress%10000000==0:
            logging.info('author progress  {:} ...'.format(progress))

        if pid in pids:
            pid_seq_author[pid][seq_no] = author

    logging.info('{:} papers has author info ...'.format(len(pid_seq_author.keys())))

    open(pathObj._authors,'w').write(json.dumps(pid_seq_author))
    logging.info('authors info  saved to {:}...'.format(pathObj._authors))

    sql = 'select id,organization from wos_address_organizations'
    pid_orgs = defaultdict(list)
    progress = 0
    for pid,org in query_op.query_database(sql):
        progress+=1

        if progress%10000000==0:
            logging.info('org progress  {:} ...'.format(progress))

        if pid in pids:
            pid_orgs[pid].append(org)

    logging.info('{:} papers has org info ...'.format(len(pid_orgs.keys())))

    open(pathObj._orgs,'w').write(json.dumps(pid_orgs))
    logging.info('Organizations info  saved to {:}...'.format(pathObj._orgs))

    query_op.close_db()


if __name__ == '__main__':

    data = int(sys.argv[1])

    if data==0:
        pathObj = PATHS('physics')
    else:
        pathObj = PATHS('computer science')


    get_social_attrs(pathObj)



