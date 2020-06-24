#import scholar
#from SComplexity.
#!pip install -e +git https://github.com/ckreibich/scholar.py
import sys
from scholar_scrape import scholar
import pandas as pd

#sys.version_info[0] == 3:
unicode = str # pylint: disable-msg=W0622
encode = lambda s: unicode(s) # pylint: disable-msg=C0103                                                                                                                                                                                '''

def csv(querier, header=False, sep='|'):
    articles = querier.articles
    results = []
    for art in articles:
        result = art.as_csv(header=header, sep=sep)
        results.append(result)
        print(encode(result))
        header = False
    return results
from delver import Crawler
C = Crawler()
import requests

from SComplexity.crawl import collect_pubs
from SComplexity.scholar_scrape import scholar

import io

from delver import Crawler
C = Crawler()
import requests


import io

import selenium

from selenium import webdriver
from pyvirtualdisplay import Display

display = Display(visible=0, size=(1024, 768))
display.start()


#from StringIO import StringIO

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import os
import sys, getopt
from io import StringIO

from selenium.webdriver.firefox.options import Options

import re
from bs4 import BeautifulSoup
import bs4 as bs
import urllib.request
from io import StringIO
import io

display = Display(visible=0, size=(1024, 768))
display.start()


from selenium.webdriver.firefox.options import Options

import re
from bs4 import BeautifulSoup


import PyPDF2
from PyPDF2 import PdfFileReader
import textract

def html_to_author(content,link):
    soup = BeautifulSoup(content, 'html.parser')

    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, 'lxml')
    mydivs = soup.findAll("h3", { "class" : "gsc_1usr_name"})
    outputFile = open('sample.csv', 'w', newline='')
    outputWriter = csv.writer(outputFile)
    for each in mydivs:
        for anchor in each.find_all('a'):
            print(anchor.text)


    #strip HTML
    '''
    for script in soup(["script", "style"]):
        script.extract()    # rip it out
    text = soup.get_text()
    wt = copy.copy(text)
    #organize text
    lines = (line.strip() for line in text.splitlines())  # break into lines and remove leading and trailing space on each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  ")) # break multi-headlines into a line each
    text = '\n'.join(chunk for chunk in chunks if chunk) # drop blank lines
    str_text = str(text)
    '''
    return str_text

def url_to_text(tuple_link):
    index,link = tuple_link
    buff = None
    #se_b, page_rank, link, category, buff = link_tuple
    if str('pdf') not in link:
        if C.open(link) is not None:
            content = C.open(link).content
            #print(content)
            content = requests.get(link, stream=True)
            buff = html_to_author(content,link)
            print(buff)

        else:
            print('problem')
    else:
        pass
        #pdf_file = requests.get(link, stream=True)
        #f = io.BytesIO(pdf_file.content)
        #reader = PdfFileReader(f)
        #buff = reader.getPage(0).extractText().split('\n')

    import pdb; pdb.set_trace()
    return buff

#@jit
'''
def buffer_to_pickle(link_tuple):
    se_b, page_rank, link, category, buff = link_tuple
    link_tuple = se_b, page_rank, link, category, buff
    fname = 'results_dir/{0}_{1}_{2}.p'.format(category,se_b,page_rank)
    if type(buff) is not None:
        with open(fname,'wb') as f:
            pickle.dump(link_tuple,f)
    return
'''
def process(item):
    text = url_to_text(item)

    #buffer_to_pickle(text)
    return


def search_author(author):
    # from https://github.com/ckreibich/scholar.py/issues/80

    querier = scholar.ScholarQuerier()
    settings = scholar.ScholarSettings()
    querier.apply_settings(settings)
    query = scholar.SearchScholarQuery()

    query.set_words(str('author:')+author)
    querier.send_query(query)
    #results0 = csv(querier)
    #results1 = citation_export(querier)
    links = [ a.attrs['url'][0] for a in querier.articles if a.attrs['url'][0] is not None ]
    sp = scholar.ScholarArticleParser()
    #sp._parse_article(links[0])
    #[ process((index,l)) for index,l in enumerate(links) ]
    import pdb
    pdb.set_trace()
    return links#, results1, links

links = search_author('R Gerkin')


print(links)


'''
NUM_LINKS but can't be bothered refactoring.
def search_scholar(get_links):
    # from https://github.com/ckreibich/scholar.py/issues/80
    se_,index,category,category,buff = get_links
    querier = scholar.ScholarQuerier()
    settings = scholar.ScholarSettings()
    querier.apply_settings(settings)
    query = scholar.SearchScholarQuery()

    query.set_words(category)
    querier.send_query(query)
    links = [ a.attrs['url'][0] for a in querier.articles if a.attrs['url'][0] is not None ]
    #links = query.get_url()
    #print(links)
    #if len(links) > NUM_LINKS: links = links[0:NUM_LINKS]

    [ process((se_,index,l,category,buff)) for index,l in enumerate(links) ]

'''
