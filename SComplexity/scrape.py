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
from bs4 import BeautifulSoup
import pickle
import _pickle as cPickle #Using cPickle will result in performance gains
from GoogleScraper import scrape_with_config, GoogleSearchError
import dask.bag as db

from SComplexity.crawl import convert_pdf_to_txt
from SComplexity.crawl import print_best_text
from delver import Crawler
C = Crawler()
import requests



display = Display(visible=0, size=(1024, 768))
display.start()


useragent = UserAgent()
# Rotate through random user profiles.
profile = webdriver.FirefoxProfile()

def rotate_profiles():
    driver = None
    profile.set_preference("general.useragent.override", useragent.random)
    profile.set_preference("javascript.enabled", True)
    driver = webdriver.Firefox(firefox_profile = profile)
    return driver
driver = rotate_profiles()


def pdf_to_txt(content):
    pdf = io.BytesIO(content.content)
    parser = PDFParser(pdf)
    document = PDFDocument(parser, password=None) # this fails
    write_text = ''
    for page in PDFPage.create_pages(document):
        interpreter.process_page(page)
        write_text = write_text.join(retstr.getvalue())
    # Process all pages in the document
    text = str(write_text)
    return text

def html_to_txt(content):
    soup = BeautifulSoup(content, 'html.parser')
    #strip HTML
    for script in soup(["script", "style"]):
        script.extract()    # rip it out
    text = soup.get_text()
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
        elif str('.pdf') in link:
            text = pdf_to_txt(content)
        else:
            try:
                text = html_to_txt(content)
            except:
                text = None
    except:
        text = None
    return text

def url_to_text(link_tuple):
    se_b, page_rank, link, category, buffer = link_tuple
    try:
        if str('pdf') not in link:
            content = C.open(link).content
            buffer = convert(content,link)
        else:
            pdf_file = requests.get(link, stream=True)
            buffer = pdf_to_txt(pdf_file)
    except:
        buffer = None
    link_tuple = ( se_b, page_rank, link, category, buffer )
    return link_tuple

def buffer_to_pickle(link_tuple):
    se_b, page_rank, link, category, buffer = link_tuple
    fname = 'results_dir/{0}_{1}_{2}.p'.format(category,se_b,page_rank)
    if type(buffer) is not None:
        with open(fname,'wb') as f:
            pickle.dump(link_tuple,f)
    return

def process(item):
    text = url_to_text(item)
    buffer_to_pickle(text)
    return


class SW(object):
    def __init__(self,iterable,nlinks=10):
        self.NUM_LINKS = nlinks
        self.iterable = iterable
        self.links = None
        if not os.path.exists('results_dir'):
            os.makedirs('results_dir')

    def scrapelandtext(self,fi):
        se_,category = fi
        config = {}
        driver = rotate_profiles()
    	# This code block, jumps over fence one (the search engine as a gatekeeper)
        # google scholar or wikipedia is not supported by google scraper
        # duckduckgo bang expansion can be used as to access engines that GS does not support.
        # for example twitter etc

        config['keyword'] = str(category)

        if str('scholar') in se_: config['keyword'] = '!scholar {0}'.format(category)
        if str('wiki') in se_ : config['keyword'] = '!wiki {0}'.format(category)
        if str('scholar') in se_ or str('wiki') in se_:
            config['search_engines'] = 'duckduckgo'
        else:
            config['search_engines'] = se_

        config['scrape_method'] = 'selenium'
        config['num_pages_for_keyword'] = 1
        config['use_own_ip'] = True
        config['sel_browser'] = 'firefox'
        config['do_caching'] = False # bloat warning.

        # Google scrap + selenium implements a lot of human centric browser masquarading tools.
        # Search Engine: 'who are you?' code: 'I am an honest human centric browser, and certainly note a robot surfing in the nude'. Search Engine: 'good, here are some pages'.
        # Time elapses and the reality is exposed just like in 'the Emperors New Clothes'.
        # The file crawl.py contains methods for crawling the scrapped links.
        # For this reason, a subsequent action, c.download (crawl download ) is ncessary.

        config['output_filename'] = '{0}_{1}.csv'.format(category,se_)

        try:
            search = scrape_with_config(config)

            links = []
            for serp in search.serps:
                print(serp)
                links.extend([link.link for link in serp.links])
            # This code block jumps over gate two
            # The (possibly private, or hosted server as a gatekeeper).
            if len(links) > self.NUM_LINKS: links = links[0:self.NUM_LINKS]
            if len(links) > 0:
                buffer = None
                get_links = ((se_,index,link,category,buffer) for index, link in enumerate(links) )
                b = db.from_sequence(get_links,npartitions=8)
                # grid = db.from_sequence(self.files,npartitions=8)
                _ = list(db.map(process,b).compute())
                # _ = list(map(process,get_links))

        except GoogleSearchError as e:
            print(e)
            return None
        print('done scraping')
        return

    def run(self):
        print(self.iterable)
        _ = list(map(self.scrapelandtext,self.iterable))
        return
