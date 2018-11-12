import os
from bs4 import BeautifulSoup
import os.path
import pickle
import numpy as np

from SComplexity.t_analysis import text_proc
from SComplexity.utils import black_string
from SComplexity.crawl import collect_pubs
from SComplexity.scrape import convert
from SComplexity.crawl import convert_pdf_to_txt


from delver import Crawler
C = Crawler()
import requests
import dask.bag as db




def process(link):
    urlDat = {}
    urlDat['link'] = link
    urlDat['page_rank'] = 'benchmark'
    if str('pdf') not in link:
        content = C.open(link).content
        buffer = convert(content,urlDat['link'])
    else:
        pdf_file = requests.get(link, stream=True)
        buffer = convert_pdf_to_txt(pdf_file)

    urlDat = text_proc(buffer,urlDat)
    return urlDat

#try:
#    assert os.path.isfile('../BenchmarkCorpus/benchmarks.p')
#    with open('../BenchmarkCorpus/benchmarks.p','rb') as f:
#        urlDats = pickle.load(f)
#except:
def get_bmarks():

    xkcd_self_sufficient = str('http://splasho.com/upgoer5/library.php')
    high_standard = str('https://elifesciences.org/download/aHR0cHM6Ly9jZG4uZWxpZmVzY2llbmNlcy5vcmcvYXJ0aWNsZXMvMjc3MjUvZWxpZmUtMjc3MjUtdjIucGRm/elife-27725-v2.pdf?_hash=WA%2Fey48HnQ4FpVd6bc0xCTZPXjE5ralhFP2TaMBMp1c%3D')
    the_science_of_writing = str('https://cseweb.ucsd.edu/~swanson/papers/science-of-writing.pdf')
    pmeg = str('http://www.elsewhere.org/pomo/') # Note this is so obfuscated, even the english language classifier rejects it.
    links = [xkcd_self_sufficient,high_standard,the_science_of_writing,pmeg ]
    royal = '../BenchmarkCorpus/royal.txt'
    klpd = '../BenchmarkCorpus/planning_document.txt'
    klpdf = open(klpd)
    strText = klpdf.read()
    urlDat = {'link':'local_resource'}

    klpdfp = text_proc(strText,urlDat, WORD_LIM = 100)
    grid = db.from_sequence(links,npartitions=8)
    urlDats = list(db.map(process,grid).compute())
    urlDats.append(klpdfp)
    print(urlDats)

    klpdr = open(royal)
    strText = klpdr.read()
    urlDat = {'link':'local_resource_royal'}

    klpdfr = text_proc(strText,urlDat, WORD_LIM = 100)
    print(klpdfr)
    grid = db.from_sequence(links,npartitions=8)
    urlDats = list(db.map(process,grid).compute())
    urlDats.append(klpdfp)


    with open('benchmarks.p','wb') as f:
        pickle.dump(urlDats,f)
    return urlDats


def check_self_contained(file_name):
    royal = '../BenchmarkCorpus/' +str(file_name)
    klpdr = open(royal)
    strText = klpdr.read()
    urlDat = {'link':'local_resource_royal'}
    klpdfr = text_proc(strText,urlDat, WORD_LIM = 100)
    return klpdfr

#urlDats = check_self_contained('royal.txt')
#urlDats = get_bmarks()
#import docx

def getText(filename):
    # convert docx files.
    # https://stackoverflow.com/questions/44741226/converting-docx-to-pure-text
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        txt = para.text.encode('ascii', 'ignore')
        fullText.append(txt)
    return '\n'.join(fullText)


#import comtypes.client

def PPTtoPDF(inputFileName, outputFileName, formatType = 32):
    powerpoint = comtypes.client.CreateObject("Powerpoint.Application")
    powerpoint.Visible = 1

    if outputFileName[-3:] != 'pdf':
        outputFileName = outputFileName + ".pdf"
        deck = powerpoint.Presentations.Open(inputFileName)
        deck.SaveAs(outputFileName, formatType) # formatType = 32 for ppt to pdf
        deck.Close()
        powerpoint.Quit()

        
