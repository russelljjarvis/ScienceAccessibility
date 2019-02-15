


try:
    summary_data = pickle.load(open('competition_data.p','rb'))   
    #assert os.path.isfile('results.p')
    #winners = pickle.load(open('results.p','rb'))
except:
    peter = str('https://academic.oup.com/beheco/article-abstract/29/1/264/4677340')
    xkcd_self_sufficient = str('http://splasho.com/upgoer5/library.php')
    high_standard = str('https://elifesciences.org/download/aHR0cHM6Ly9jZG4uZWxpZmVzY2llbmNlcy5vcmcvYXJ0aWNsZXMvMjc3MjUvZWxpZmUtMjc3MjUtdjIucGRm/elife-27725-v2.pdf?_hash=WA%2Fey48HnQ4FpVd6bc0xCTZPXjE5ralhFP2TaMBMp1c%3D')
rgerkin = str('https://scholar.google.com/citations?user=GzG5kRAAAAAJ&hl=en&oi=sra')
scrook = str('https://scholar.google.com/citations?user=xnsDhO4AAAAJ&hl=en&oe=ASCII&oi=sra')
dgrayden = str('https://scholar.google.com/citations?user=X7aP2LIAAAAJ&hl=en')

from bs4 import BeautifulSoup
from SComplexity.crawl import collect_pubs
import os.path
import pickle
import numpy as np


from SComplexity.get_bmark_corpus import process
from SComplexity.t_analysis import text_proc


try:
    assert os.path.isfile('authors.p')
    authors = pickle.load(open('authors.p','rb'))
except:

    rgerkin = collect_pubs(rgerkin)
    scrook = collect_pubs(scrook)
    authors = {}
    authors['rgerkin'] = rgerkin
    authors['scrook'] = scrook
    with open('authors.p','wb') as f:
        pickle.dump(authors,f)

hs = process(high_standard)
urlDat = {'link':high_standard}
hss = text_proc(hs,urlDat)

benchmark = process(xkcd_self_sufficient)
urlDat = {'link':xkcd_self_sufficient}
bench = text_proc(benchmark,urlDat)


try:
    assert os.path.isfile('author_results.p')
    author_results = pickle.load(open('author_results.p','rb'))
except:
    author_results = {'rgerkin':{}, 'scrook':{}}
    for author,links in authors.items():
        for r in links:
            urlDat = process(r)

            if str(r) not in author_results.keys():
                author_results[author][str(r)] = urlDat
            else:
                author_results[author][str(r)] = urlDat
        print(author_results)
    with open('author_results.p','wb') as f:
        pickle.dump(author_results,f)

rg = list(author_results['rgerkin'].values())
sc = list(author_results['scrook'].values())

def metrics(rg):
    if type(rg) is type([]):
        pub_count = len(rg)
        standard = np.mean([ r['standard'] for r in rg ])
        unique = np.mean([ r['uniqueness'] for r in rg ])
        density = np.mean([ r['info_density'] for r in rg ])
        wcount = np.mean([ r['wcount'] for r in rg ])
        scaled_density = density/wcount
        obj = np.mean([ r['sp'] for r in rg ])
        return standard
    else:
        return None

def filter_empty(the_list):
    return [ tl for tl in the_list if 'standard' in tl.keys() ]


rg = filter_empty(rg)
sc = filter_empty(sc)

both_authors = []
both_authors.extend(rg)
both_authors.extend(sc)
pickle.dump([rg,sc,both_authors],open('competition_data.p','wb'))
rick = metrics(rg)
scrook = metrics(sc)
rank = [(rick,str('rick')),(scrook,str('sharon'))]
print('the winner of the science clarity competition is: ', sorted(rank)[0])
#print('the scores are:',np.min(rick,sharon))
'''
bench = metrics(bench)
pm = metrics(pm)
hss = metrics(hss)
winners = [('rgerkin',rick),('scrook',scrook),('upgoer5_corpus',bench),('the readability of science decr over time', hss), ('peter',pm)]
with open('results.p','wb') as f:
    pickle.dump(winners,f)

winners = sorted([(w[1],w[0]) for w in winners])
print(winners)

try:
    win = pickle.load(open('winners.p','rb'))

    winners = sorted([(w['standard'],list(w.items())) for w in both_authors])
except:
    pass
'''
