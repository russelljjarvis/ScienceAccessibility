from bs4 import BeautifulSoup
from SComplexity.crawl import collect_pubs
import os.path
import pickle
import numpy as np

try:
    from SComplexity.get_bmark_corpus import process
    RICK_FAVORED = str('https://elifesciences.org/articles/08127')
    RICK_FAVORED = process(RICK_FAVORED)

except:
    pass
from SComplexity.t_analysis import text_proc



try:
    summary_data = pickle.load(open('competition_data.p','rb'))
except:
    pass
    # good standards:
xkcd_self_sufficient = str('http://splasho.com/upgoer5/library.php')
high_standard = str('https://elifesciences.org/download/aHR0cHM6Ly9jZG4uZWxpZmVzY2llbmNlcy5vcmcvYXJ0aWNsZXMvMjc3MjUvZWxpZmUtMjc3MjUtdjIucGRm/elife-27725-v2.pdf?_hash=WA%2Fey48HnQ4FpVd6bc0xCTZPXjE5ralhFP2TaMBMp1c%3D')
# competitors (3):
RGERKIN = str('https://scholar.google.com/citations?user=GzG5kRAAAAAJ&hl=en&oi=sra')
SCROOK = str('https://scholar.google.com/citations?user=xnsDhO4AAAAJ&hl=en&oe=ASCII&oi=sra')
GRAYDEN = str('https://scholar.google.com/citations?user=X7aP2LIAAAAJ&hl=en')
SMBAER = str('https://scholar.google.com/scholar?hl=en&as_sdt=0%2C3&q=SM+baer+&btnG=')
#ELI_JADE = str('Clones allow the consideration of algebras abstracted from signature. Despite the development of general algebra with the notion of type as a central concept, it is not the case that a variety uniquely determines the type; an equational class may be represented with different types. A classic example may be found in the variety of groups.')


try:
    assert os.path.isfile('authors.p')
    authors = pickle.load(open('authors.p','rb'))
except:

    RGERKIN = collect_pubs(RGERKIN)
    SCROOK = collect_pubs(SCROOK)
    GRAYDEN = collect_pubs(GRAYDEN)
    
    authors = {}
    authors['rgerkin'] = RGERKIN
    authors['scrook'] = SCROOK
    authors['grayden'] = GRAYDEN
    with open('authors.p','wb') as f:
        pickle.dump(authors,f)

#SMBAER = collect_pubs(SMBAER)
#authors['smbaer'] = SMBAER

with open('authors.p','wb') as f:
    pickle.dump(authors,f)

try:
    assert os.path.isfile('other_standards.p')
    other_s = pickle.load(open('other_standards.p','rb'))

except:
    hs = process(high_standard)
    urlDat = {'link':high_standard}
    hss = text_proc(hs,urlDat)


    benchmark = process(xkcd_self_sufficient)
    urlDat = {'link':xkcd_self_sufficient}
    bench = text_proc(benchmark,urlDat)
    other_s = pickle.dump([hss,benchmark,bench],open('other_standards.p','wb'))



try:
    #assert 1==2
    assert os.path.isfile('author_results.p')
    author_results = pickle.load(open('author_results.p','rb'))
except:
    author_results = {'rgerkin':{}, 'scrook':{}, 'grayden':{}, 'smbaer':{}}
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
gn = list(author_results['grayden'].values())
sb = list(author_results['smbaer'].values())
import pdb
pdb.set_trace()

def metricss(rg):
    if type(rg) is type([]):
        pub_count = len(rg)
        standard = np.mean([ r['standard'] for r in rg ])
        return standard
    else:
        return None
def metricsp(rg):
    if type(rg) is type([]):
        pub_count = len(rg)
        penalty = np.mean([ r['penalty'] for r in rg ])
        return penalty
    else:
        return None

def filter_empty(the_list):
    return [ tl for tl in the_list if 'standard' in tl.keys() ]


rg = filter_empty(rg)
sc = filter_empty(sc)
gn = filter_empty(gn)
sb = filter_empty(sb)

all_authors = []
all_authors.extend(rg)
all_authors.extend(sc)
all_authors.extend(gn)
all_authors.extend(sb)

pickle.dump([rg,sc,gn,sb,all_authors],open('competition_data.p','wb'))
rick = metricss(rg)
scrook = metricss(sc)
grayden = metricss(gn)
smbaer = metricss(sb)

rank = [(rick,str('rick')),(scrook,str('sharon')),(grayden,str('grayden')),(smbaer,str('smbaer'))]
print('the winner of the science clarity competition is: ', sorted(rank)[0])
import pdb
pdb.set_trace()
print(rank)
print(rick,scrook,grayden,smbaer)
rick = metricsp(rg)
scrook = metricsp(sc)
grayden = metricsp(gn)
smbaer = metricsp(sb)

print('penalties: rick,scrook,grayden,smbaer')
print(rick,scrook,grayden,smbaer)

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
