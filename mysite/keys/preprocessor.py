import collections as coll
import itertools
import os

DATA_DIR = '..\combine'

FILE_LS = next(os.walk(DATA_DIR))[-1]
INNER_GT = 10

def load_data(ng_len=2, lat_lb=20, lat_ub=500):
    '''
    optional args
    ngraph length, defaults to 2
    lower bound on latency, defaults to 20
    upper bound on latency, defaults to 500

    returns dict (user str -> [(ngraph, latency)])
    '''
    data_dict = {}
    d = {}

    for f in FILE_LS:
        #if f.startswith('A'): continue
        data = file(DATA_DIR+'/'+f).read()
        pairs = [x.rsplit(':',1) for x in data.replace('\n','\t').split('\t')]
        pairs = [(x[0], int(x[1])) for x in pairs if len(x) == 2]
        ngraphs = []
        for i in range(len(pairs)-ng_len+1):
            ng_t =  pairs[i+ng_len-1][1] - pairs[i][1]
            if lat_lb <= ng_t <= lat_ub: ngraphs.append([''.join([x[0] for x in pairs[i:i+ng_len]]), ng_t])
        if len(ngraphs)>3000:  d[f.split('.')[0]] = ngraphs    #the file name without extension (e.g. ".txt")
    return d

def chunkify(ls, sz):
    '''
    takes list of elements
    returns list of lists of size sz, drops last if size less than sz
    '''
    #s= [ls[x:x+sz] for x in range(0, len(ls), sz) if len(ls[x:x+sz]) == sz][:2]
    #print [len(i) for i in s ]
    #exit()
    return [ls[x:x+sz] for x in range(0, len(ls), sz) if len(ls[x:x+sz]) == sz]

def ngraph_ls2dict(ls):
    '''
    takes [(ngraph, latency)]
    returns dict (ngraph -> [latency])
    '''
    d = coll.defaultdict(list)
    for ng_t in ls:
        d[ng_t[0]].append(float(ng_t[1]))
    return d

def split_samples(data_dict, sample_size=1000):
    '''
    takes dict (user str -> [(ngraph, latency)])
    optional args
    sample size, defaults to 1000 (keystrokes)
    returns dict (user str -> [(ngraph -> [latency])])
    '''
    return {k:map(ngraph_ls2dict,chunkify(v,sample_size)) for k,v in data_dict.items()}

def filter_users_val(sample_dict):
    '''
    takes dict (user str -> [(ngraph -> [latency])])
    returns a dict of the same type so that
    only users who can supply the necessary amount of
    inner/outer genuine validation tests are kept.
    also returns dict containing values of p for each user
    (i.e. leave-p-out per outer validation split)
    and dict containing values of k for each users
    (i.e. leave-k-out per inner validation split)

    could reduce N loop to ceil(N/2), cache comb approximations
    '''
    pk_combs_d = {}
    for u in sample_dict.keys():
        N = len(sample_dict[u])
        pk_combs_d[u] = (1, 1, N, N-1)
    return sample_dict, pk_combs_d

if __name__=='__main__':
    d = split_samples(load_data())
    su = []
    for u in d:
        for s in d[u]:
            aa = len([i for i in s if len(s[i])>=10])
            su.append(aa)
            if aa>30: print 'aa', s
    print [len(d[i]) for i in d]
    print su
    print sum(su)*1.0/len(su)
    f, pkd = filter_users_val(d)

    user_list = []
    for k,x in pkd.items():
        user_list.append(k)
        print k, ',', x[0], ',', x[1], ',', int(x[2]/x[0]), ',', int(x[3]/x[1])
    data = f
    p = {u:int(pkd[u][0]) for u in [user_list[1], user_list[2]]}
    k = {u:int(pkd[u][1]) for u in [user_list[1], user_list[2]]}

    lli1 = len(list(i1))


