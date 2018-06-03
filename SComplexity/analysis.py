
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


class Analysis(object):
    def __init__(self,files, urlDats=None):
        self.files = files
        self.urlDats = urlDats

    def cas(self):
        grid = db.from_sequence(self.files,npartitions=8)
        urlDats = list(db.map(convert_and_score,grid).compute())
        urlDats = list(filter(lambda url: len(list(url))>3, urlDats))
        urlDats = list(filter(lambda url: len(list(url.keys()))>3, urlDats))
        urlDats = list(filter(lambda url: str('penalty') in url.keys(), urlDats))
        if type(self.urlDats) is not type(None):
            urlDats.extend(self.urlDats)
        return urlDats

    def get_bench(self):
        try:
            assert os.path.isfile('../BenchmarkCorpus/benchmarks_ranked.p')
            benchmarks_ranked = pickle.load(open('../BenchmarkCorpus/benchmarks_ranked.p','rb'))
            benchmarks = [ b[1] for b in benchmarks_ranked ]
            known_corpus.extend(benchmarks)
        except:
            import get_bmark_corpus
            assert os.path.isfile('../BenchmarkCorpus/benchmarks_ranked.p')
            benchmarks_ranked = pickle.load(open('../BenchmarkCorpus/benchmarks_ranked.p','rb'))
            benchmarks = [ b[1] for b in benchmarks_ranked ]
            known_corpus.extend(benchmarks)
        self.urlDats = known_corpus
        return

    
