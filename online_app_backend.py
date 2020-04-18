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

from crawl import collect_pubs#, collect_hosted_files
from get_bmark_corpus import process
from t_analysis import text_proc
# Put these results, in a data frame, then in Markdown, using RGerkin's code.
# https://gist.github.com/rgerkin/af5b27a0e30531c30f2bf628aa41a553
# !pip install --user tabulate # Install the tabulate package
from tabulate import tabulate
from t_analysis import text_proc, perplexity, unigram_zipf



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

    return [ tl for tl in the_list if 'standard' in tl.keys() ]


def take_url_from_gui(author_link_scholar_link_list):
    '''
    inputs a URL that's full of publication orientated links, preferably the
    authors scholar page.
    '''
    author_results = []
    follow_links = collect_pubs(author_link_scholar_link_list)[0:5]
    for r in follow_links:
       try:
           urlDat = process(r)

       except:
           follow_more_links = collect_pubs(r)
           for r in follow_more_links:
               urlDat = process(r)
       print(urlDat)
        
       if not isinstance(urlDat,type(None)):
           author_results.append(urlDat)

       # print(author_results[-1])
       #with open('new.p','wb') as f:
       #    pickle.dump(author_results,f)
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



def update_web_form(url):
    print(url)
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

def enter_name_here(scholar_page, name):
    df, datay, author_results = update_web_form(scholar_page)
    #author_results
    '''
    md = tabulate(df, headers='keys', tablefmt='pipe')
    # Fix the markdown string; it will not render with an empty first table cell,
    # so if the dataframe's index has no name, just place an 'x' there.
    md = md.replace('|    |','| %s |' % (df.index.name if df.index.name else 'x'))
    # Create the Markdown object
    result = d.Markdown(md)
    '''
    return df, datay, author_results

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

def ar_manipulation(ar):
    ar = [ tl for tl in ar if tl is not None ]
    ar = [ tl for tl in ar if type(tl) is not type(str('')) ]
    ar = [ tl for tl in ar if 'standard' in tl.keys() ]

    #with open(str('more_authors_results.p'),'wb') as f:
    #    pickle.dump([NAME,ar],f)

    with open('traingDats.p','rb') as f:
        trainingDats = pickle.load(f)
        
    trainingDats.extend(ar)
    return (ar, trainingDats)

def call_from_front_end(NAME,tour=None,NAME1=None,verbose=False):
    if type(tour) is type(None):
        scholar_link=str('https://scholar.google.com/scholar?hl=en&as_sdt=0%2C3&q=')+str(NAME)
        df, datay, ar  = enter_name_here(scholar_link,NAME)
        
        with open('_author_specific'+str(NAME)+'.p','wb') as f: pickle.dump([NAME,ar,df,datay,scholar_link],f)

        
        (ar, trainingDats) = ar_manipulation(ar)
        with open('traingDats.p','wb') as f:
            pickle.dump(trainingDats,f)
        import plotting_author_versus_distribution
        return ar

    else:
        scholar_link=str('https://scholar.google.com/scholar?hl=en&as_sdt=0%2C3&q=')+str(NAME)
        df, datay, ar  = enter_name_here(scholar_link,NAME)
        (ar0, trainingDats) = ar_manipulation(ar)
        scholar_link=str('https://scholar.google.com/scholar?hl=en&as_sdt=0%2C3&q=')+str(NAME1)
        df, datay, ar  = enter_name_here(scholar_link,NAME1)
        (ar1, trainingDats) = ar_manipulation(ar)
        import plotting_author_versus_distribution
        return [ar0,ar1]
