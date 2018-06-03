
import glob
import os
import dask.bag as db

from SComplexity.crawl import html_to_txt, convert_pdf_to_txt#, print_best_text
from SComplexity.t_analysis import text_proc
#from SComplexity.utils import print_best_text#, convert_and_score

from natsort import natsorted, ns
import pprint
import pickle
import numpy as np
import os

def print_best_text(f):
    link_tuple = pickle.load(open(f,'rb'))
    se_b, page_rank, link, category, buffer = link_tuple
    return buffer

def convert_and_score(f):
    urlDat = {}
    b = os.path.getsize(f)
    link_tuple = pickle.load(open(f,'rb'))
    se_b, page_rank, link, category, buffer = link_tuple
    if type(buffer) is not type(None):
        urlDat = { 'link':link,'page_rank':page_rank,'se':se_b,'query':category,'file':f }
        urlDat = text_proc(buffer,urlDat)
        print(urlDat)

    return urlDat

known_corpus = []
try:
    assert os.path.isfile('../BenchmarkCorpus/benchmarks_ranked.p')
    benchmarks_ranked = pickle.load(open('../BenchmarkCorpus/benchmarks_ranked.p','rb'))

    benchmarks_unranked = pickle.load(open('../BenchmarkCorpus/benchmarks.p','rb'))# as f: pickle.dump(benchmarks,f)
    #import pdb; pdb.set_trace()
    benchmarks = [ b[1] for b in benchmarks_ranked ]
    known_corpus.extend(benchmarks)
    print('benchmarks loaded')
except:
    import get_bmark_corpus

# naturally sort a list of files, as machine sorted is not the desired file list hierarchy.
files = natsorted(glob.glob(str(os.getcwd())+'/*.p'))
files = [ f for f in files if not str('unraveled_links.p') in str(f) ]
files = [ f for f in files if not str('winners.p') in str(f) ]
files = [ f for f in files if not str('benchmarks.p') in str(f) ]
files = [ f for f in files if not str('benchmarks_ranked.p') in str(f) ]

grid = db.from_sequence(files,npartitions=8)
urlDats = list(db.map(convert_and_score,grid).compute())
urlDats = list(filter(lambda url: len(list(url))>3, urlDats))
urlDats = list(filter(lambda url: len(list(url.keys()))>3, urlDats))
urlDats = list(filter(lambda url: str('penalty') in url.keys(), urlDats))
with open('unraveled_links.p','wb') as handle:
    pickle.dump(urlDats,handle)

urlDats.extend(known_corpus)
winners = sorted(urlDats, key=lambda w: w['gf'])   # sort by age
import pdb; pdb.set_trace()

text0 = print_best_text(winners[0]['file'])
text1 = print_best_text(winners[1]['file'])


pp = pprint.PrettyPrinter(indent=4)
pp.pprint(winners[0])
pp.pprint(text0)
pp.pprint(winners[1])
pp.pprint(text1)

frames = False
if frames ==True:
    unravel = process_dics(urlDats)
else:
    unravel = urlDats
with open('winners.p','wb') as handle:
    pickle.dump(urlDats,handle)
