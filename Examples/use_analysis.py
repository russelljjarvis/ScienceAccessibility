
import glob
from natsort import natsorted, ns
import pprint
import numpy as np
import os


import pickle
from SComplexity.scrape import SW
from SComplexity.analysis import Analysis

#
# naturally sort a list of files, as machine sorted is not the desired file list hierarchy.
# Note this mess could be avoided if I simply stored the mined content somewhere else.
files = natsorted(glob.glob(str(os.getcwd())+'/results_dir/*.p'))
#files = [ f for f in files if not str('unraveled_links.p') in str(f) ]
#files = [ f for f in files if not str('winners.p') in str(f) ]
#files = [ f for f in files if not str('benchmarks.p') in str(f) ]
#files = [ f for f in files if not str('benchmarks_ranked.p') in str(f) ]


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


pp = pprint.PrettyPrinter(indent=4)
print('best')
pp.pprint(winners[0])
print('worst')

pp.pprint(winners[-1])

frames = False
if frames ==True:
    unravel = process_dics(urlDats)
else:
    unravel = urlDats
with open('winners.p','wb') as handle:
    pickle.dump(urlDats,handle)
