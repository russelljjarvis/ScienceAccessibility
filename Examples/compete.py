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
SMBAER = ['https://accounts.google.com/Login?hl=en&continue=https://scholar.google.com/scholar%3Fhl%3Den%26as_sdt%3D0%252C3%26q%3DSM%2Bbaer%2B%26btnG%3D', 'https://accounts.google.com/Login?hl=en&continue=https://scholar.google.com/scholar%3Fhl%3Den%26as_sdt%3D0%252C3%26q%3DSM%2Bbaer%2B%26btnG%3D', 'https://epubs.siam.org/doi/pdf/10.1137/0149003', \
'https://epubs.siam.org/doi/abs/10.1137/0149003', \
'http://gateway.webofknowledge.com/gateway/Gateway.cgi?GWVersion=2&SrcApp=GSSearch&SrcAuth=Scholar&DestApp=WOS_CPL&DestLinkType=CitingArticles&UT=A1989T025000003&SrcURL=https://scholar.google.com/&SrcDesc=Back+to+Google+Scholar&GSPage=TC', 'https://epubs.siam.org/doi/pdf/10.1137/0146047',\
'https://epubs.siam.org/doi/abs/10.1137/0146047',\
'http://gateway.webofknowledge.com/gateway/Gateway.cgi?GWVersion=2&SrcApp=GSSearch&SrcAuth=Scholar&DestApp=WOS_CPL&DestLinkType=CitingArticles&UT=A1986E294500001&SrcURL=https://scholar.google.com/&SrcDesc=Back+to+Google+Scholar&GSPage=TC', 'https://pdfs.semanticscholar.org/da88/b2a5d0a8d3d912e7222f2ae561e0c53bd33f.pdf',\
'https://www.physiology.org/doi/abs/10.1152/jn.1991.65.4.874', \
'http://gateway.webofknowledge.com/gateway/Gateway.cgi?GWVersion=2&SrcApp=GSSearch&SrcAuth=Scholar&DestApp=WOS_CPL&DestLinkType=CitingArticles&UT=A1991FF97300010&SrcURL=https://scholar.google.com/&SrcDesc=Back+to+Google+Scholar&GSPage=TC', 'http://gateway.webofknowledge.com/gateway/Gateway.cgi?GWVersion=2&SrcApp=GSSearch&SrcAuth=Scholar&DestApp=WOS_CPL&DestLinkType=CitingArticles&UT=000306193900009&SrcURL=https://scholar.google.com/&SrcDesc=Back+to+Google+Scholar&GSPage=TC', \
'https://epubs.siam.org/doi/pdf/10.1137/0152095', \
'https://epubs.siam.org/doi/abs/10.1137/0152095',\
'http://gateway.webofknowledge.com/gateway/Gateway.cgi?GWVersion=2&SrcApp=GSSearch&SrcAuth=Scholar&DestApp=WOS_CPL&DestLinkType=CitingArticles&UT=A1992KA76600009&SrcURL=https://scholar.google.com/&SrcDesc=Back+to+Google+Scholar&GSPage=TC',\
'https://link.aps.org/pdf/10.1103/PhysRevA.35.1165', \
'https://journals.aps.org/pra/abstract/10.1103/PhysRevA.35.1165',\
'http://gateway.webofknowledge.com/gateway/Gateway.cgi?GWVersion=2&SrcApp=GSSearch&SrcAuth=Scholar&DestApp=WOS_CPL&DestLinkType=CitingArticles&UT=A1987F987200026&SrcURL=https://scholar.google.com/&SrcDesc=Back+to+Google+Scholar&GSPage=TC',\
'https://www.sciencedirect.com/science/article/pii/S0006349588829886/pdf?md5=e6618131f15a16225a4099d17db76d4a&pid=1-s2.0-S0006349588829886-main.pdf&_valck=1', 'https://www.sciencedirect.com/science/article/pii/S0006349588829886', \
'http://gateway.webofknowledge.com/gateway/Gateway.cgi?GWVersion=2&SrcApp=GSSearch&SrcAuth=Scholar&DestApp=WOS_CPL&DestLinkType=CitingArticles&UT=A1988P969000019&SrcURL=https://scholar.google.com/&SrcDesc=Back+to+Google+Scholar&GSPage=TC',\
'https://link.aps.org/pdf/10.1103/PhysRevE.78.036205', \
'https://journals.aps.org/pre/abstract/10.1103/PhysRevE.78.036205', 'http://gateway.webofknowledge.com/gateway/Gateway.cgi?GWVersion=2&SrcApp=GSSearch&SrcAuth=Scholar&DestApp=WOS_CPL&DestLinkType=CitingArticles&UT=000259683100028&SrcURL=https://scholar.google.com/&SrcDesc=Back+to+Google+Scholar&GSPage=TC', 'https://epubs.siam.org/doi/pdf/10.1137/050627757', \
'https://epubs.siam.org/doi/abs/10.1137/050627757', 'http://gateway.webofknowledge.com/gateway/Gateway.cgi?GWVersion=2&SrcApp=GSSearch&SrcAuth=Scholar&DestApp=WOS_CPL&DestLinkType=CitingArticles&UT=000238324300012&SrcURL=https://scholar.google.com/&SrcDesc=Back+to+Google+Scholar&GSPage=TC', 'https://www.physiology.org/doi/abs/10.1152/jn.1990.64.2.326', \
'http://gateway.webofknowledge.com/gateway/Gateway.cgi?GWVersion=2&SrcApp=GSSearch&SrcAuth=Scholar&DestApp=WOS_CPL&DestLinkType=CitingArticles&UT=A1990DV59900002&SrcURL=https://scholar.google.com/&SrcDesc=Back+to+Google+Scholar&GSPage=TC'
]


try:
    assert os.path.isfile('authors.p')
    authors = pickle.load(open('authors.p','rb'))
except:

    RGERKIN = collect_pubs(RGERKIN)
    SCROOK = collect_pubs(SCROOK)
    GRAYDEN = collect_pubs(GRAYDEN)
    MARKRAM = collect_pubs(MARKRAM)
    EMARDER = collect_pubs(EMARDER)
    authors = {}
    authors['rgerkin'] = RGERKIN
    authors['scrook'] = SCROOK
    authors['grayden'] = GRAYDEN
    authors['smbaer'] = SMBAER
    authors['markram'] = MARKRAM
    authors['emarder'] = EMARDER


    with open('authors.p','wb') as f:
        pickle.dump(authors,f)


authors['markram'] = MARKRAM
authors['emarder'] = EMARDER


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
    assert os.path.isfile('author_results.p')
    author_results = pickle.load(open('author_results.p','rb'))
    #import pdb
    #pdb.set_trace()
    sb_results = pickle.load(open('sb_results.p','rb'))
    new = pickle.load(open('new.p','rb'))
    author_results['sbaer'] = sb_results
    author_results['markram'] = new['markram']
    author_results['emarder'] = new['emarder']

except:
    more = [author_results['markram'],author_results['emarder']]
    names = [str('markram'),str('emarder')]

    for i,s in enumerate(more):
        follow_links = collect_pubs(s)
        #import pdb; pdb.set_trace()
        for r in follow_links:
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
    # with open('new.p','wb') as f:
    #     pickle.dump(author_results,f)

    author_results = {'rgerkin':{}, 'scrook':{}, 'grayden':{}, 'smbaer':{}}
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

    compete_results[k] = np.mean(per_author)

    author_results['rgerkin']['perplexity'] = compete_results[k]






rg = list(author_results['rgerkin'].values())
sc = list(author_results['scrook'].values())
gn = list(author_results['grayden'].values())
sb = list(author_results['smbaer'].values())
em = list(author_results['emarder'].values())
mk = list(author_results['markram'].values())

sb = sb[0:12]
import pdb
pdb.set_trace()


rg = filter_empty(rg)
sc = filter_empty(sc)
gn = filter_empty(gn)
sb = filter_empty(sb)
mk = filter_empty(mk)
em = filter_empty(em)

all_authors = []
all_authors.extend(rg)
all_authors.extend(sc)
all_authors.extend(gn)
all_authors.extend(sb)
all_authors.extend(em)
all_authors.extend(markram)
pickle.dump([rg,sc,gn,sb,all_authors],open('competition_data.p','wb'))
rick = metricss(rg)
scrook = metricss(sc)
grayden = metricss(gn)
smbaer = metricss(sb)
emarder = metricss(em)
markram = metricss(mk)

rank = [(rick,str('rick')),(scrook,str('sharon')),
(grayden,str('grayden')),(smbaer,str('smbaer')),
(emarder,str('emarder')),(markram,str('markram'))]
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
print('penalties: rick,scrook,grayden,smbaer,emarder,markram')
print(rick,scrook,grayden,smbaer,emarder,markram)

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
