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
    follow_links = collect_pubs(author_link_scholar_link_list)
    for r in follow_links[0:14]:
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

BHENDERSON = str('https://scholar.google.com/citations?user=o_aMfnoAAAAJ&hl=en&oi=ao')
PMCGURRIN = str('https://www.pmcgurrin.com/publications')

def update_web_form(url):
    author_results = take_url_from_gui(url)
    data = {}
    for k,v in author_results.items():
        x = filter_empty(v)

        data[k] = metricss(x)
    df = pd.DataFrame(data=data, columns=columns)
    return df
# Optionally give the dataframe's index a name
#df.index.name = "my_index"
# Create the markdown string
try:
    test_values = [BHENDERSON,PMCGURRIN]
    for t in test_values:
        df = update_web_form(t)
    #author_results
        md = tabulate(df, headers='keys', tablefmt='pipe')
        # Fix the markdown string; it will not render with an empty first table cell,
        # so if the dataframe's index has no name, just place an 'x' there.
        md = md.replace('|    |','| %s |' % (df.index.name if df.index.name else 'x'))
        # Create the Markdown object
        result = d.Markdown(md)
except:
    print('tried and failed!')
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
