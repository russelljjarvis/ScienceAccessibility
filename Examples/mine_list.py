
import glob
import os
import dask.bag as db
from crawl import html_to_txt, convert_pdf_to_txt
from t_analysis_csv import text_proc#, metrics
from natsort import natsorted, ns
# naturally sort a list of files, as machine sorted is not the desired file list hierarchy.
lo_query_html = natsorted(glob.glob(str(os.getcwd())+'/*.html'))
lo_query_pdf = natsorted(glob.glob(str(os.getcwd())+'/*.pdf'))

def local_opt(fileName):
    b = os.path.getsize(fileName)
    urlDat = {}
    if b>250: # this is just to prevent reading in of incomplete data.
        try:
            file = open(fileName)
            if str('.html') in fileName:
                text = html_to_txt(file)
            else:
                text = convert_pdf_to_txt(file)
            file.close()
            urlDat = {'link':fileName}
            urlDat = text_proc(text,urlDat)
            print(urlDat)
        except:
            pass
    return urlDat

urlDats = list(map(local_opt,lo_query_html[0:2]))

grid0 = db.from_sequence(lo_query_html)
grid1 = db.from_sequence(lo_query_pdf)
urlDats = list(db.map(local_opt,grid0).compute())
urlDats.extend(list(db.map(local_opt,grid1).compute()))

urlDats2 = list(filter(lambda url: len(list(url.keys()))>3, urlDats))

urlDats0 = list(filter(lambda url: str('penalty') in url.keys(), urlDats2))
#winners = sorted([ (w['penalty'],w['link']) for w in urlDats0])#winners = sorted([ (w['penalty'],w) for w in urlDats0])
#winners_len = sorted([ (w['wcount'],w['link']) for w in urlDats0])#winners = sorted([ (w['penalty'],w) for w in urlDats0])

winners = sorted(urlDats0, key=lambda w: w['penalty'])   # sort by age
#import pdb; pdb.set_trace()
#print(winners[0])
def print_best_text(fileName):
    file = open(fileName)
    if str('.html') in fileName:
        text = html_to_txt(file)
    else:
        text = convert_pdf_to_txt(file)
    file.close()
    return text

text0 = print_best_text(winners[0][1])
text1 = print_best_text(winners[1][1])

import pprint
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
import pickle
with open('unraveled_links.p','wb') as handle:
    pickle.dump(winners,handle)
