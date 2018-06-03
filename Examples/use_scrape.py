# Scientific readability project
# authors: other authors,
# ...,
# Russell Jarvis
# https://github.com/russelljjarvis/
# rjjarvis@asu.edu
import selenium
from pyvirtualdisplay import Display
from selenium import webdriver
from fake_useragent import UserAgent
from numpy import random
import os
from delver import Crawler
from GoogleScraper import scrape_with_config, GoogleSearchError

from natsort import natsorted, ns
import pprint
import numpy as np
import os
import glob


import pickle
from SComplexity.scrape import SW
from SComplexity.analysis import Analysis

LINKSTOGET= 10 #number of links to pull from each search engine (this can be any value, but more processing with higher number)


def engine_dict_list():
    se = {0:"google",1:"yahoo",2:"duckduckgo",3:"wikipedia",4:"scholar",5:"bing"}
    return se, list(se.values())

def search_params():
    SEARCHLIST = ["evolution","cancer", "photosysnthesis",'climate change','Vaccines','Transgenic','GMO','Genetically Modified Organism','reality TV', 'unicorn versus brumby', 'football soccer', 'prancercise philosophy', 'play dough delicious deserts']
    return SEARCHLIST, se, LINKSTOGET
# Use this variable to later reconcile file names with urls
# As there was no, quick and dirty way to bind the two togethor here, without complicating things later.
se, _ = engine_dict_list()

SEARCHLIST, se, LINKSTOGET = search_params()
flat_iter = [ (se[b],category) for category in SEARCHLIST for b in range(0,4) ]

# traverse this list randomly as hierarchial traversal may be a bot give away.
random.shuffle(flat_iter)

sw = SW(flat_iter,nlinks=10)
sw.run()


#
# naturally sort a list of files, as machine sorted is not the desired file list hierarchy.
# Note this mess could be avoided if I simply stored the mined content somewhere else.
files = natsorted(glob.glob(str(os.getcwd())+'/*.p'))
files = [ f for f in files if not str('unraveled_links.p') in str(f) ]
files = [ f for f in files if not str('winners.p') in str(f) ]
files = [ f for f in files if not str('benchmarks.p') in str(f) ]
files = [ f for f in files if not str('benchmarks_ranked.p') in str(f) ]


A = Analysis(files)
A.get_bench()
urlDats = A.cas()
with open('unraveled_links.p','wb') as handle:
    pickle.dump(urlDats,handle)

winners = sorted(urlDats, key=lambda w: w['penalty'])   # sort by age


def print_best_text(f):
    link_tuple = pickle.load(open(f,'rb'))
    se_b, page_rank, link, category, buffer = link_tuple
    return buffer


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
