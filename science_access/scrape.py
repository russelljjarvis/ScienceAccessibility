# Scientific readability project
# authors: other authors,
# ...,
# Russell Jarvis
# https://github.com/russelljjarvis/
# rjjarvis@asu.edu

# Patrick McGurrin
# patrick.mcgurrin@gmail.com
from numpy import random
import os
from bs4 import BeautifulSoup
import pickle
import _pickle as cPickle #Using cPickle will result in performance gains
#from GoogleScraper import scrape_with_config, GoogleSearchError
import dask.bag as db

import pdfminer
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams
from pdfminer.converter import  TextConverter

import os
import sys, getopt
from io import StringIO

from delver import Crawler
C = Crawler()
import requests
import io
import selenium


from .crawl import convert_pdf_to_txt
from .crawl import print_best_text
from .crawl import collect_pubs
from science_access import scholar


import re
from bs4 import BeautifulSoup
import bs4 as bs
import urllib.request
from io import StringIO
import io
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
import os
from selenium import webdriver
if 'DYNO' in os.environ:
    heroku = False
else:
    heroku = True
def get_driver():
    if 'DYNO' in os.environ:
        heroku = True
    else:
        heroku = False

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    try:
        driver = webdriver.Firefox(options=options)
    except:
        try:
            options.binary_location = "/app/vendor/firefox/firefox"
            driver = webdriver.Firefox(options=options)
            GECKODRIVER_PATH=str(os.getcwd())+str("/geckodriver")
            driver = webdriver.Firefox(options=options,executable_path=GECKODRIVER_PATH)
        except:
            try:
                chrome_options = webdriver.ChromeOptions()
                chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
                chrome_options.add_argument("--headless")
                chrome_options.add_argument("--disable-dev-shm-usage")
                chrome_options.add_argument("--no-sandbox")
                driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
            except:
                try:
                    GECKODRIVER_PATH=str(os.getcwd())+str("/geckodriver")
                    options.binary_location = str('./firefox')
                    driver = webdriver.Firefox(options=options,executable_path=GECKODRIVER_PATH)
                except:
                    os.system("wget wget https://ftp.mozilla.org/pub/firefox/releases/45.0.2/linux-x86_64/en-GB/firefox-45.0.2.tar.bz2")
                    os.system("wget https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz")
                    os.system("tar -xf geckodriver-v0.26.0-linux64.tar.gz")
                    os.system("tar xvf firefox-45.0.2.tar.bz2")
                    GECKODRIVER_PATH=str(os.getcwd())+str("/geckodriver")
                    options.binary_location = str('./firefox')
                    driver = webdriver.Firefox(options=options,executable_path=GECKODRIVER_PATH)
    return driver


#driver = get_driver()

rsrcmgr = PDFResourceManager()
retstr = StringIO()
laparams = LAParams()
codec = 'utf-8'
device = TextConverter(rsrcmgr, retstr, laparams = laparams)
interpreter = PDFPageInterpreter(rsrcmgr, device)


#converts pdf, returns its text content as a string
def pdf_to_txt_(infile):#, pages=None):
    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close
    return text


import PyPDF2
from PyPDF2 import PdfFileReader


def pdf_to_txt(url):

    if str(content) == str('<Response [404]>'):
        return None
    else:
        # from
        # https://medium.com/@rqaiserr/how-to-convert-pdfs-into-searchable-key-words-with-python-85aab86c544f
        try:
            input_buffer = StringIO(content.content)
            pdfReader = PyPDF2.PdfFileReader(input_buffer)
        except:
            pdfFileObj = io.BytesIO(content.content)
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

        num_pages = pdfReader.numPages
        count = 0
        text = ""
        while count < num_pages:
            pageObj = pdfReader.getPage(count)
            count +=1
            text += pageObj.extractText()
        if text != "":
           text = text
        else:
           text = textract.process(fileurl, method='tesseract', language='eng')
    return text

def html_to_txt(content):
    soup = BeautifulSoup(content, 'html.parser')
    #strip HTML

    for script in soup(["script", "style"]):
        script.extract()    # rip it out
    text = soup.get_text()
    wt = copy.copy(text)
    #organize text
    lines = (line.strip() for line in text.splitlines())  # break into lines and remove leading and trailing space on each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  ")) # break multi-headlines into a line each
    text = '\n'.join(chunk for chunk in chunks if chunk) # drop blank lines
    str_text = str(text)

    return str_text

def convert(content,link):
    # This is really ugly, but it's proven to be both fault tolerant and effective.
    try:
        if str('.html') in link:
            text = html_to_txt(content)
            print(text)

        elif str('.pdf') in link:
            text = pdf_to_txt(content)
        else:
            try:
                text = html_to_txt(content)
                print(text)
            except:
                text = None
    except:
        text = None
    return text


def url_to_text(link_tuple):
    se_b, page_rank, link, category, buff = link_tuple
    if str('pdf') not in link:
        if C.open(link) is not None:
            content = C.open(link).content
            buff = convert(content,link)
        else:
            print('problem')
    else:
        pdf_file = requests.get(link, stream=True)
        f = io.BytesIO(pdf_file.content)
        reader = PdfFileReader(f)
        buff = reader.getPage(0).extractText().split('\n')


    print(buff)
    link_tuple = ( se_b, page_rank, link, category, buff )
    return link_tuple

#@jit
def buffer_to_pickle(link_tuple):
    se_b, page_rank, link, category, buff = link_tuple
    link_tuple = se_b, page_rank, link, category, buff
    fname = 'results_dir/{0}_{1}_{2}.p'.format(category,se_b,page_rank)
    if type(buff) is not None:
        with open(fname,'wb') as f:
            pickle.dump(link_tuple,f)
    return

def process(item):
    text = url_to_text(item)
    buffer_to_pickle(text)
    return


# this should not be hard coded, it should be set in the class init, but can't be bothered refactoring.
NUM_LINKS = 10



# this should be a class method with self and self.NUM_LINKS but can't be bothered refactoring.
def wiki_get(get_links):
    # wikipedia is robot friendly
    # surfraw is fine.
    se_,index,link,category,buff = get_links
    url_of_links = str('https://en.wikipedia.org/w/index.php?search=')+str(category)
    links = collect_pubs(url_of_links)
    if len(links) > NUM_LINKS: links = links[0:NUM_LINKS]
    [ process((se_,index,l,category,buff)) for index,l in enumerate(links) ]

# this should be a class method with self and self.NUM_LINKS but can't be bothered refactoring.

def scholar_pedia_get(get_links):
    # wikipedia is robot friendly
    # surfraw is fine.
    se_,index,link,category,buff = get_links
    url_of_links = str('http://www.scholarpedia.org/w/index.php?search=')+str(category)+str('&title=Special%3ASearch')
    links = collect_pubs(url_of_links)
    if len(links) > NUM_LINKS: links = links[0:NUM_LINKS]
    [ process((se_,index,l,category,buff)) for index,l in enumerate(links) ]

# this should be a class method with self and self.NUM_LINKS but can't be bothered refactoring.
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

def search_author(get_links):
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

class SW(object):
    def __init__(self,sengines,sterms,nlinks=10):
        self.NUM_LINKS = nlinks
        self.links = None
        if not os.path.exists('results_dir'):
            os.makedirs('results_dir')
        self.iterable = [ (v,category) for category in sterms for v in sengines.values() ]
        random.shuffle(self.iterable)

    def slat_(self,config):
        try:
            if str('wiki') in config['search_engines']:
                get_links = (str('wikipedia'),0,None,config['keyword'],None)
                wiki_get(get_links)

            elif str('info_wars') in config['search_engines']:
                get_links = (str('info_wars'),0,None,config['keyword'],None)
                info_wars_get(get_links)

            elif str('scholar') in config['search_engines']:
                get_links = (str('scholar'),0,None,config['keyword'],None)
                search_scholar(get_links)

            elif str('scholarpedia') in config['search_engines']:
                get_links = (str('scholar'),0,None,config['keyword'],None)
                scholar_pedia_get(get_links)

            else:
                search = scrape_with_config(config)
                links = []
                for serp in search.serps:
                    print(serp)
                    links.extend([link.link for link in serp.links])

                # This code block jumps over gate two
                # The (possibly private, or hosted server as a gatekeeper).
                if len(links) > self.NUM_LINKS: links = links[0:self.NUM_LINKS]
                if len(links) > 0:
                    print(links)
                    buffer = None
                    se_ = config['search_engines']
                    category = config['keyword']
                    get_links = ((se_,index,link,category,buffer) for index, link in enumerate(links) )
                    for gl in get_links:
                        process(gl)
                    # map over the function in parallel since it's 2018
                    #b = db.from_sequence(get_links,npartitions=8)
                    #_ = list(b.map(process).compute())
        except GoogleSearchError as e:
            print(e)
            return None
        print('done scraping')

    #@jit
    def scrapelandtext(self,fi):
        se_,category = fi
        config = {}
        #driver = rotate_profiles()
        # This code block, jumps over gate one (the search engine as a gatekeeper)
        # google scholar or wikipedia is not supported by google scraper
        # duckduckgo bang expansion _cannot_ be used as to access engines that GS does not support
        # without significant development. Redirection to the right search results does occur,
        # but google scrape also has tools for reading links out of web pages, and it needs to know
        # which brand of SE to expect in order to deal with idiosyncratic formatting.
        # it's easier not to use bang expansion, for that reason.
        # for example twitter etc

        config['keyword'] = str(category)


        config['search_engines'] = se_
        #config['scrape_method'] = 'http'

        config['scrape_method'] = 'selenium'
        config['num_pages_for_keyword'] = 1
        config['use_own_ip'] = True
        config['sel_browser'] = 'chrome'
        config['do_caching'] = False # bloat warning.

        # Google scrap + selenium implements a lot of human centric browser masquarading tools.
        # Search Engine: 'who are you?' code: 'I am an honest human centric browser, and certainly note a robot surfing in the nude'. Search Engine: 'good, here are some pages'.
        # Time elapses and the reality is exposed just like in 'the Emperors New Clothes'.
        # The file crawl.py contains methods for crawling the scrapped links.
        # For this reason, a subsequent action, c.download (crawl download ) is ncessary.

        config['output_filename'] = '{0}_{1}.csv'.format(category,se_)

        self.slat_(config)
        return

    def run(self):
        # someone should write a unit_test.
        # one reason I have not, is I would want to use travis.cl, and scrapping probably violates policies.
        # a unit test might begin like this:
        # self.iterable.insert(0,("scholar"),str("arbitrary test")))
        # self.iterable.insert(0,("wiki"),str("arbitrary test")))

        _ = list(map(self.scrapelandtext,self.iterable))
        return
