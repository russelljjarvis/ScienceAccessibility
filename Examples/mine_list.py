
import glob
import os
import dask.bag as db
from crawl import html_to_txt, convert_pdf_to_txt
from t_analysis_csv import text_proc
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
            urlDat = {'link':fileName}
            urlDat = text_proc(text,urlDat)
            print(urlDat)
        except:
            pass
    return urlDat

grid0 = db.from_sequence(lo_query_html)
grid1 = db.from_sequence(lo_query_pdf)
urlDats = list(db.map(local_opt,grid0).compute())
urlDats.extend(list(db.map(local_opt,grid1).compute()))
frames = False

if frames ==True:
    unravel = process_dics(urlDats)
else:
    unravel = urlDats
import pickle
with open('unraveled_links.p','wb') as handle:
    pickle.dump(unravel,handle)
