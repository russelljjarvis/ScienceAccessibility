import os
import os.path
import pickle

import dask.bag as db
import numpy as np
import requests
from bs4 import BeautifulSoup

from crawl import collect_pubs, convert_pdf_to_txt#,process
from scrape import get_driver
from t_analysis import text_proc
from utils import black_string

def process(link):
    urlDat = {}
    urlDat['link'] = link
    urlDat['page_rank'] = 'benchmark'
    if str('pdf') not in link:
        
        driver = get_driver()

        driver.get(link)
        crude_html = driver.page_source

        soup = BeautifulSoup(crude_html, 'html.parser')
        for script in soup(["script", "style"]):
            script.extract()    # rip it out
        text = soup.get_text()
        #wt = copy.copy(text)
        #organize text
        lines = (line.strip() for line in text.splitlines())  # break into lines and remove leading and trailing space on each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  ")) # break multi-headlines into a line each
        text = '\n'.join(chunk for chunk in chunks if chunk) # drop blank lines
        buffered = str(text)
    else:
        pdf_file = requests.get(link, stream=True)
        buffered = convert_pdf_to_txt(pdf_file)
    urlDat = text_proc(buffered,urlDat)
    return urlDat

#try:
#    assert os.path.isfile('../BenchmarkCorpus/benchmarks.p')
#    with open('../BenchmarkCorpus/benchmarks.p','rb') as f:
#        urlDats = pickle.load(f)
#except:

def mess_length(word_length,bcm):
    with open('bcm.p','rb') as f:
        big_complex_mess = pickle.load(big_complex_mess,f)
    reduced = big_complex_mess[0:word_length]
    urlDat = {}
    pmegmess = text_proc(reduced,urlDat)
    return mess_length, pmegmess
"""
def get_greg_nicholas():
    urlDat = {}
    urlDat['link'] = "nicholas"
    urlDat['page_rank'] = 'nicholas'
    #pdf_file = requests.get(link, stream=True)
    #bufferd = convert_pdf_to_txt(pdf_file)
    #File_object = open(r"local_text.txt","Access_Mode")
    file1 = open("local_text.txt","r") 
    txt = file1.readlines()
    new_str = ''
    for i in txt:
        new_str+=str(i)
    urlDat = text_proc(new_str,urlDat)
    print(urlDat)
    #add to benchmarks
    with open('benchmarks.p','rb') as f:
        urlDats = pickle.load(f)
    urlDats.append(urlDat)
    with open('benchmarks.p','wb') as f:
        pickle.dump(urlDats,f)

    return urlDat
"""

def get_bmarks():
    xkcd_self_sufficient = str('http://splasho.com/upgoer5/library.php')
    high_standard = str('https://elifesciences.org/download/aHR0cHM6Ly9jZG4uZWxpZmVzY2llbmNlcy5vcmcvYXJ0aWNsZXMvMjc3MjUvZWxpZmUtMjc3MjUtdjIucGRm/elife-27725-v2.pdf?_hash=WA%2Fey48HnQ4FpVd6bc0xCTZPXjE5ralhFP2TaMBMp1c%3D')
    the_science_of_writing = str('https://cseweb.ucsd.edu/~swanson/papers/science-of-writing.pdf')
    pmeg = str('http://www.elsewhere.org/pomo/') # Note this is so obfuscated, even the english language classifier rejects it.
    this_manuscript = str('https://www.overleaf.com/read/dqkttvmqjvhn')
    this_readme = str('https://github.com/russelljjarvis/ScienceAccessibility')
    links = [xkcd_self_sufficient,high_standard,the_science_of_writing,this_manuscript,this_readme ]
    urlDats = list(map(process,links))

    pmegs = []
    for i in range(0,9):
       p = process(pmeg)
       if p is not None:
           pmegs.append(p) # grab this constantly changing page 10 times to get the mean value.
    if pmegs[0] is not None:
        urlDats.append(process(pmegs[0]))
    big_complex_mess = ''
    urlDat = {}
    for p in pmegs:
        if p is not None:
            for s in p['tokens']:
                big_complex_mess += s+str(' ')
    bcm = ''
    for p in pmegs[0:2]:
        if p is not None:
            for s in p['tokens']:
                bcm += s+str(' ')

    pmegmess_2 = text_proc(bcm,urlDat)
    #import pdb; pdb.set_trace()
    with open('bcm.p','wb') as f:
        pickle.dump(big_complex_mess,f)

    urlDats[-1]['standard'] = np.mean([p['standard'] for p in pmegs])
    #import pdb
    #pdb.set_trace()
    urlDats[-1]['sp'] = np.mean([p['sp'] for p in pmegs])
    urlDats[-1]['gf'] = np.mean([p['gf'] for p in pmegs])
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


def getText(filename):
    # convert docx files.
    # https://stackoverflow.com/questions/44741226/converting-docx-to-pure-text
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        txt = para.text.encode('ascii', 'ignore')
        fullText.append(txt)
    return '\n'.join(fullText)
