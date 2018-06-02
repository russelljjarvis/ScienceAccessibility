
import glob
import os
import dask.bag as db

from SComplexity.crawl import html_to_txt, convert_pdf_to_txt, print_best_text
from SComplexity.t_analysis import text_proc
#from SComplexity.utils import print_best_text#, convert_and_score

from natsort import natsorted, ns
import pprint
import pickle
import numpy as np
import os

#def proc_text(text):
#    text = text_proc(text,urlDat)
#    return text

def convert_and_score(fileName):
    b = os.path.getsize(fileName)
    text = None
    try: # this is just to prevent reading in of incomplete data.
        file = open(fileName)
        print(file)
        if str('.html') in fileName:
            text = html_to_txt(file)
        elif str('.pdf') in fileName:
            text = convert_pdf_to_txt(file)
        else:
            print('other')
        file.close()
        urlDat = {'link':fileName}
        urlDat = text_proc(text,urlDat)
        print(urlDat)
    except:
        urlDat = {'link':fileName}
    return urlDat

TOURNAMENT = False

try:
    assert os.path.isfile('../BenchmarkCorpus/benchmarks_ranked.p')
    benchmarks_ranked = pickle.load(open('../BenchmarkCorpus/benchmarks_ranked.p','rb'))

    benchmarks_unranked = pickle.load(open('../BenchmarkCorpus/benchmarks.p','rb'))# as f: pickle.dump(benchmarks,f)
    #import pdb; pdb.set_trace()
    benchmarks = [ b[1] for b in benchmarks ]
    urlDats = []
    urlDats.extend(benchmarks)
    print('benchmarks loaded')
except:
    pass
urlDats = []
# naturally sort a list of files, as machine sorted is not the desired file list hierarchy.
lo_query_html = natsorted(glob.glob(str(os.getcwd())+'/*.html'))
lo_query_pdf = natsorted(glob.glob(str(os.getcwd())+'/*.pdf'))


grid0 = db.from_sequence(lo_query_html[0:int(len(lo_query_html)/2)],npartitions=8)
grid1 = db.from_sequence(lo_query_html[int(len(lo_query_html)/2):-1],npartitions=8)
grid2 = db.from_sequence(lo_query_pdf,npartitions=8)


urlDats2 = list(db.map(convert_and_score,grid2).compute())
urlDats1 = list(db.map(convert_and_score,grid1).compute())
urlDats0 = list(db.map(convert_and_score,grid1).compute())

print('gets here')
urlDats.extend(urlDats0)
urlDats.extend(urlDats1)
urlDats.extend(urlDats2)

urlDats = list(filter(lambda url: len(list(url))>3, urlDats))
urlDats = list(filter(lambda url: len(list(url.keys()))>3, urlDats))
urlDats = list(filter(lambda url: str('penalty') in url.keys(), urlDats))
with open('unraveled_links.p','wb') as handle:
    pickle.dump(urlDats,handle)


winners = sorted(urlDats, key=lambda w: w['gf'])   # sort by age

text0 = print_best_text(winners[0]['link'])
text1 = print_best_text(winners[1]['link'])


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
