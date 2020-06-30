import copy
import matplotlib.pyplot as plt
import seaborn as sns
import os.path
import pdb
import pickle
from collections import OrderedDict

import IPython.display as d
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

from .crawl import collect_pubs
from .get_bmark_corpus import process
from .t_analysis import text_proc
from .t_analysis import text_proc, perplexity, unigram_zipf

import streamlit as st

if 'DYNO' in os.environ:
    heroku = True
else:
    heroku = False
from time import sleep
import numpy as np


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

from tqdm import tqdm
import streamlit as st


class tqdm:
    def __init__(self, iterable, title=None):
        if title:
            st.write(title)
        self.prog_bar = st.progress(0)
        self.iterable = iterable
        self.length = len(iterable)
        self.i = 0

    def __iter__(self):
        for obj in self.iterable:
            yield obj
            self.i += 1
            current_prog = self.i / self.length
            self.prog_bar.progress(current_prog)


def take_url_from_gui(author_link_scholar_link_list):
    '''
    inputs a URL that's full of publication orientated links, preferably the
    authors scholar page.
    '''
    author_results = []
    if heroku:
        follow_links = collect_pubs(author_link_scholar_link_list)[3:25]
    else:
        follow_links = collect_pubs(author_link_scholar_link_list)[0:15]

    for r in tqdm(follow_links,title='Progess of scraping'):
  
        try:
            urlDat = process(r)
        except:
            follow_more_links = collect_pubs(r)
            for r in tqdm(follow_more_links,title='Progess of scraping'):
                if heroku:
                    sleep(np.random.uniform(1,3))
                urlDat = process(r)        
        if not isinstance(urlDat,type(None)):
            author_results.append(urlDat)
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
    author_results = take_url_from_gui(url)
    ar =  copy.copy(author_results)
    datax = filter_empty(ar)
    datay = metricss(ar)
    df = pd.DataFrame(datax)
    return df, datay, author_results

def enter_name_here(scholar_page, name):
    df, datay, author_results = update_web_form(scholar_page)
    return df, datay, author_results

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

def ar_manipulation(ar):
    ar = [ tl for tl in ar if tl is not None ]
    ar = [ tl for tl in ar if type(tl) is not type(str('')) ]
    ar = [ tl for tl in ar if 'standard' in tl.keys() ]

    with open('data/traingDats.p','rb') as f:
        trainingDats = pickle.load(f)
        
    trainingDats.extend(ar)
    return (ar, trainingDats)

import os
from crossref_commons.iteration import iterate_publications_as_json
import requests
def call_from_front_end(NAME):
    if not heroku:
        scholar_link=str('https://scholar.google.com/scholar?hl=en&as_sdt=0%2C3&q=')+str(NAME)
        #for link in scholar_link:
        #    st.text(link) 

        _, _, ar  = enter_name_here(scholar_link,NAME)


    if heroku:
        filter_ = {'type': 'journal-article'}
        queries = {'query.author': NAME}
        ar = []
        bi =[p for p in iterate_publications_as_json(max_results=50, filter=filter_, queries=queries)]   
        for p in bi[0:9]:    
            res = str('https://api.unpaywall.org/v2/')+str(p['DOI'])+str('?email=YOUR_EMAIL')
            response = requests.get(res)
            temp = response['best_oa_location']['url_for_pdf']

            #temp=str('https://unpaywall.org/'+str(p['DOI'])) 
            #st.text(temp) 
            urlDat = process(temp)        
            if not isinstance(urlDat,type(None)):
                ar.append(urlDat)
                #st.text(urlDat) 


    (ar, trainingDats) = ar_manipulation(ar)
    '''
    with open('data/traingDats.p','rb') as f:            
        trainingDats_old = pickle.load(f)
    trainingDats.extend(trainingDats_old)    
    with open('data/traingDats.p','wb') as f:            
        pickle.dump(trainingDats,f)        
    '''
    return ar
