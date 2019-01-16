
import glob
import os
import dask.bag as db

from SComplexity.utils import html_to_txt, convert_pdf_to_txt
from SComplexity.t_analysis import text_proc

from natsort import natsorted, ns
import pprint
import pickle
import numpy as np
import os


def print_best_text(f):
    link_tuple = pickle.load(open(f,'rb'))
    se_b, page_rank, link, category, buff_ = link_tuple
    return buff_



class Analysis(object):
    def __init__(self,files, min_word_length = 200, urlDats=None):
        self.files = files
        self.urlDats = urlDats
        self.mwl = min_word_length

    def convert_and_score(self,f):
        urlDat = {}
        b = os.path.getsize(f)
        link_tuple = pickle.load(open(f,'rb'))
        se_b, page_rank, link, category, buff_ = link_tuple
        if buff_ is not None:
            urlDat = { 'link':link,'page_rank':page_rank,'se':se_b,'query':category,'file':f }
            urlDat = text_proc(buff_,urlDat, WORD_LIM = self.mwl)
        return urlDat

    def cas(self):
        # Do in parallel as it is 2018
    
        pgrid = db.from_sequence(self.files,npartitions=8)
        urlDats = list(db.map(self.convert_and_score,pgrid).compute())
        # just kidding need to do a serial debug often times, regardless of parallel speed up.
        #urlDats = list(map(self.convert_and_score,self.files))
        urlDats = [ url for url in urlDats if type(url) is not type(None) ]
        #urlDats = list(filter(lambda url: type(url) != None, urlDats))
        urlDats = list(filter(lambda url: len(list(url))>3, urlDats))

        urlDats = list(filter(lambda url: len(list(url.keys()))>3, urlDats))
        # urlDats = list(filter(lambda url: str('penalty') in url.keys(), urlDats))
        if type(self.urlDats) is not type(None):
            urlDats.extend(self.urlDats)
        return urlDats

    def get_reference_web(self):
        from SComplexity.scrape import SW
        from SComplexity.get_bmark_corpus import get_bmarks
        return get_bmarks()

    #def get_reference_pickle(self):
    #    known_corpus = []
    #    from SComplexity.get_bmark_corpus import get_bmarks
    #    return get_bmarks()
