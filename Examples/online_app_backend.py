import copy
import matplotlib.pyplot as plt
import seaborn as sns
#plt.backend("")
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
from SComplexity.t_analysis import text_proc, perplexity, unigram_zipf

def metricss(rg):
    if isinstance(rg,list):
        pub_count = len(rg)
        mean_standard = np.mean([ r['standard'] for r in rg if 'standard' in r.keys()])
        return mean_standard
    else:
        return None
def metricsp(rg):
    if isinstance(rg,list):
        pub_count = len(rg)
        penalty = np.mean([ r['penalty'] for r in rg if 'penalty' in r.keys()])
        penalty = np.mean([ r['perplexity'] for r in rg if 'perplexity' in r.keys() ])

        return penalty
    else:
        return None

def filter_empty(the_list):
    the_list = [ tl for tl in the_list if tl is not None ]
    the_list = [ tl for tl in the_list if type(tl) is not type(str('')) ]

    #simport pdb
    #pdb.set_trace()
    return [ tl for tl in the_list if 'standard' in tl.keys() ]


'''
PMCGURRIN = collect_pubs(PMCGURRIN)
BHENDERSON = collect_pubs(BHENDERSON)
'''

#def take_url_from_gui(url):


def take_url_from_gui(author_link_scholar_link_list):
    '''
    inputs a URL that's full of publication orientated links, preferably the
    authors scholar page.
    '''
    author_results = []
    follow_links = collect_pubs(author_link_scholar_link_list)
    for r in follow_links:
       urlDat = process(r)
       if not isinstance(urlDat,type(None)):
           author_results.append(urlDat)

       print(author_results[-1])
       with open('new.p','wb') as f:
           pickle.dump(author_results,f)
    return author_results

def unigram_model(author_results):
    '''
    takes author results.
    '''
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

    return big_model

def info_models(author_results):
    big_model = unigram_model(author_results)
    compete_results = {}
    for k,v in author_results.items():
        per_dpc = []
        try:
            for doc in author_results[k]['words']:
                per_doc.append(perplexity(doc, big_model))
        except:
            pass
        compete_results[k] = np.mean(per_doc)
        author_results[k]['perplexity'] = compete_results[k]
    return author_results, compete_results



def update_web_form(url,name):
    #data = author_results = {}
    author_results = take_url_from_gui(url)
    ar =  copy.copy(author_results)
    #data[name] = author_results
    #for k,v in author_results.items():
    datax = filter_empty(ar)
    datay = metricss(ar)
    print(datay)
    df = pd.DataFrame(datax)
    print(df)
    return df, datay, author_results
# Optionally give the dataframe's index a name
#df.index.name = "my_index"
# Create the markdown string

BHENDERSON = str('https://scholar.google.com/citations?user=o_aMfnoAAAAJ&hl=en&oi=ao')
PMCGURRIN = str('https://www.pmcgurrin.com/publications')
RGERKIN = str('https://scholar.google.com/citations?user=GzG5kRAAAAAJ&hl=en&oi=ao')
#try:
test_values = [PMCGURRIN,BHENDERSON]
names = [str('PMCGURRIN'),str('BHENDERSON')]

#for t,name in zip(test_values,names):
def enter_name_here(scholar_page,name):
    df, datay, author_results = update_web_form(scholar_page,name)
#author_results
    md = tabulate(df, headers='keys', tablefmt='pipe')
    # Fix the markdown string; it will not render with an empty first table cell,
    # so if the dataframe's index has no name, just place an 'x' there.
    md = md.replace('|    |','| %s |' % (df.index.name if df.index.name else 'x'))
    # Create the Markdown object
    result = d.Markdown(md)

    return df, datay, author_results

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

df, datay, ar  = enter_name_here(BHENDERSON,'ben')

ar = [ tl for tl in ar if tl is not None ]
ar = [ tl for tl in ar if type(tl) is not type(str('')) ]
ar = [ tl for tl in ar if 'standard' in tl.keys() ]

with open(str('more_authors_results.p'),'wb') as f:
    pickle.dump(ar,f)

with open('traingDats.p','rb') as f:
    trainingDats = pickle.load(f)

#For the bars, information is stored in:
standard_sci = [ t['standard'] for t in trainingDats ]
temp = [ t['standard'] for t in ar ]
standard_sci.extend(temp)

sns.distplot(standard_sci).patches
#You can access the bar's height via the function patches.get_height():

[ h.get_height() for h in sns.distplot(standard_sci).patches ]
xys = [ (h.get_x(),h.get_height()) for h in sns.distplot(standard_sci).patches ]


sns.distplot(standard_sci)
index = find_nearest([x[0] for x in xys], author_results)
plt.scatter(x=author_results, y=xys[index][1], color='b')
plt.show()
#'all_before.png'

#except:
#    print('tried and failed!')
# Display the markdown object (in a Jupyter code cell)
#result
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
