import os.path
import pdb
import pickle
from collections import OrderedDict

import IPython.display as d
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

from SComplexity.crawl import collect_pubs
from SComplexity.get_bmark_corpus import process
from SComplexity.t_analysis import text_proc
# Put these results, in a data frame, then in Markdown, using RGerkin's code.
# https://gist.github.com/rgerkin/af5b27a0e30531c30f2bf628aa41a553
# !pip install --user tabulate # Install the tabulate package
from tabulate import tabulate
from SComplexity.t_analysis import text_proc, perplexity, unigram

def metricss(rg):
    if isinstance(rg,list):
        pub_count = len(rg)
        standard = np.mean([ r['standard'] for r in rg ])
        return standard
    else:
        return None
def metricsp(rg):
    if isinstance(rg,list):
        pub_count = len(rg)
        penalty = np.mean([ r['penalty'] for r in rg ])
        penalty = np.mean([ r['perplexity'] for r in rg ])

        return penalty
    else:
        return None

def filter_empty(the_list):
    the_list = [ tl for tl in the_list if tl is not None ]
    return [ tl for tl in the_list if 'standard' in tl.keys() ]

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
EMARDER = str('https://scholar.google.com/citations?user=WUWmiBcAAAAJ&hl=en&oi=sra')
GRAYDEN = str('https://scholar.google.com/citations?user=X7aP2LIAAAAJ&hl=en')
SMBAER = str('https://scholar.google.com/scholar?hl=en&as_sdt=0%2C3&q=SM+baer+&btnG=')
RICK_FAVORED = str('https://elifesciences.org/articles/08127')
MARKRAM = str('https://scholar.google.com/citations?user=W3lyJF8AAAAJ&hl=en&oi=sra')
BHENDERSON = str('https://scholar.google.com/citations?user=o_aMfnoAAAAJ&hl=en&oi=ao')
PMCGURRIN = str('https://www.pmcgurrin.com/publications')

try:
    assert os.path.isfile('authors.p')
    authors = pickle.load(open('authors.p','rb'))
except:

    RGERKIN = collect_pubs(RGERKIN)
    SCROOK = collect_pubs(SCROOK)
    GRAYDEN = collect_pubs(GRAYDEN)
    MARKRAM = collect_pubs(MARKRAM)
    EMARDER = collect_pubs(EMARDER)
    BHENDERSON = collect_pubs(BHENDERSON)

    authors = {}
    authors['rgerkin'] = RGERKIN
    authors['scrook'] = SCROOK
    authors['grayden'] = GRAYDEN
    authors['smbaer'] = SMBAER
    authors['markram'] = MARKRAM
    authors['emarder'] = EMARDER
    authors['bhen'] = BHENDERSON


    with open('authors.p','wb') as f:
        pickle.dump(authors,f)

PMCGURRIN = collect_pubs(PMCGURRIN)
        
BHENDERSON = collect_pubs(BHENDERSON)

#authors['markram'] = MARKRAM
#authors['emarder'] = EMARDER
authors['bhen'] = BHENDERSON
authors['pg'] = PMCGURRIN


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


def get_ind_author(author_link_scholar_link_list):
    more = [author_results['markram'],author_results['emarder'],authors['bhen']]
    names = [str('bhen'),str('pg')]
    latest = []
    latest.extend(authors['bhen'])
    latest.extend(authors['pg'])
    for i,s in enumerate(latest):
        follow_links = collect_pubs(s)
        #names[i] = str('bhen')
        #import pdb; pdb.set_trace()
        for r in follow_links[0:10]:
           urlDat = process(r)
           if not isinstance(urlDat,type(None)):
               if str(r) not in author_results.keys():
                   author_results[names[i]] = {}
                   author_results[names[i]][str(r)] = urlDat
               else:
                   author_results[names[i]][str(r)] = urlDat
           print(author_results)
           with open('new.p','wb') as f:
               pickle.dump(author_results,f)
try:
    assert os.path.isfile('author_results.p')
    author_results = pickle.load(open('author_results.p','rb'))
    #import pdb
    #pdb.set_trace()
    #sb_results = pickle.load(open('sb_results.p','rb'))
    new = pickle.load(open('new.p','rb'))
    #author_results['sbaer'] = sb_results
    author_results['markram'] = new['markram']
    author_results['emarder'] = new['emarder']
    author_results['bhen'] = new['bhen']

except:
    author_results['bhen'] = authors['bhen']
    more = [author_results['markram'],author_results['emarder'],author_results['bhen']]
    names = [ str('bhen')]
    local = []
    
    local.extend(authors['bhen'][0:10])
    local.extend(authors['pg'][0:10])

    
    for i,s in enumerate(local):
        follow_links = collect_pubs(s)
        #names[i] = str('bhen')
        #import pdb; pdb.set_trace()
        for r in follow_links[0:15]:
           urlDat = process(r)
           if not isinstance(urlDat,type(None)):
               if str(r) not in author_results.keys():
                   author_results[str('bhen')] = {}
                   author_results[str('bhen')][str(r)] = urlDat
               else:
                   author_results[str('bhen')][str(r)] = urlDat
           print(author_results)
           with open('new.p','wb') as f:
               pickle.dump(author_results,f)
    # with open('new.p','wb') as f:
    #     pickle.dump(author_results,f)

    author_results = {'rgerkin':{}, 'scrook':{}, 'grayden':{}, 'emarder':{}, 'markram':{},'bhen':{}}
    for author,links in authors.items():
        for r in links:
            urlDat = process(r)

            if str(r) not in author_results.keys():
                author_results[author][str(r)] = urlDat
            else:
                author_results[author][str(r)] = urlDat
            print(author_results)
            with open('intermediate_author_results.p','wb') as f:
                pickle.dump(author_results,f)

    with open('author_results.p','wb') as f:
       pickle.dump(author_results,f)



try:

    assert 1==2
    big_model = pickle.load(open('big_model_science.p','rb'))
    author_results = OrderedDict(pickle.load(open('author_results_processed.p','rb')))

except:
    author_results_r = OrderedDict(author_results)
    terms = []
    for k,v in author_results.items():
        try:
            #author_results_r[k] = list(s for s in v.values()  )
            author_results[k]['files'] = list(s for s in v.values()  )

            words = [ ws['tokens'] for ws in author_results[k]['files'] if ws is not None ]
            author_results[k]['words'] = words
            terms.extend(words)# if isinstance(terms,dict) ]
        except:
            print(terms[-1])
    big_model = unigram(terms)


    with open('author_results_processed.p','wb') as file:
        pickle.dump(author_results,file)
    with open('big_model_science.p','wb') as file:
        pickle.dump(list(big_model),file)

compete_results = {}

for k,v in author_results.items():
    per_dpc = []
    try:
        for doc in author_results[k]['words']:
            per_doc.append(perplexity(doc, big_model))
    except:
        pass

    compete_results[k] = np.mean(per_doc)

    author_results['rgerkin']['perplexity'] = compete_results[k]




bh = list(author_results['bhen'].values())


rg = list(author_results['rgerkin'].values())
sc = list(author_results['scrook'].values())
gn = list(author_results['grayden'].values())
em = list(author_results['emarder'].values())
mk = list(author_results['markram'].values())

import pdb
pdb.set_trace()

bh = filter_empty(bh)

rg = filter_empty(rg)
sc = filter_empty(sc)
gn = filter_empty(gn)
#sb = filter_empty(sb)
mk = filter_empty(mk)
em = filter_empty(em)

all_authors = []
all_authors.extend(rg)
all_authors.extend(sc)
all_authors.extend(gn)
#all_authors.extend(sb)
all_authors.extend(em)
all_authors.extend(markram)
pickle.dump([rg,sc,gn,sb,all_authors],open('competition_data.p','wb'))
rick = metricss(rg)
scrook = metricss(sc)
grayden = metricss(gn)
bhenderson = metricss(bh)
emarder = metricss(em)
markram = metricss(mk)

rank = [(rick,str('rick')),(scrook,str('sharon')),(bhenderson,str('bryan henderson'))
(grayden,str('grayden')),(emarder,str('emarder')),(markram,str('markram'))]
print('the winner of the science clarity competition is: ', sorted(rank)[0])
pdb.set_trace()
print(rank)
print(rick,scrook,grayden,smbaer)
rick = metricsp(rg)
scrook = metricsp(sc)
scrook = metricsp(gn)
smbaer = metricsp(sb)
emarder = metricsp(em)
markram = metricsp(mk)
print('penalties: rick,scrook,grayden,bryan hen,emarder,markram')
print(rick,scrook,grayden,bhen,emarder,markram)

# Some random data
#data = np.random.rand(10,4)
# Columns A, B, C, D
#columns = [chr(x) for x in range(65,69)]
# Create the dataframe
data = [rick,scrook,scrook,smbaer,emarder,markram]

df = pd.DataFrame(data=data,
columns=columns)
# Optionally give the dataframe's index a name
#df.index.name = "my_index"
# Create the markdown string
md = tabulate(df, headers='keys', tablefmt='pipe')
# Fix the markdown string; it will not render with an empty first table cell,
# so if the dataframe's index has no name, just place an 'x' there.
md = md.replace('|    |','| %s |' % (df.index.name if df.index.name else 'x'))
# Create the Markdown object
result = d.Markdown(md)
# Display the markdown object (in a Jupyter code cell)
result
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
