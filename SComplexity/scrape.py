# Scientific readability project
# authors: other authors,
# ...,
# Russell Jarvis
# https://github.com/russelljjarvis/
# rjjarvis@asu.edu

# Patrick McGurrin
# patrick.mcgurrin@gmail.com
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
#import duckduckgo

import requests
#import scholar_scrape
from SComplexity.crawl import collect_pubs
from SComplexity.scholar_scrape import scholar



display = Display(visible=0, size=(1024, 768))
display.start()


useragent = UserAgent()
# Rotate through random user profiles.
profile = webdriver.FirefoxProfile()

def rotate_profiles():
    # keep changing the header associated with browser requests to SE
    # Its hard to tell if its a convincing masquarade but it's low cost.
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
    se_b, page_rank, link, category, buff = link_tuple
    if str('wiki') in category:
        se_b = 'wikipedia'

    if str('scholar') in category:
        se_b = 'scholar'

    link_tuple = se_b, page_rank, link, category, buff

    fname = 'results_dir/{0}_{1}_{2}.p'.format(category,se_b,page_rank)
    print(fname,se_b)

    if type(buff) is not None:
        with open(fname,'wb') as f:
            pickle.dump(link_tuple,f)
    return

def process(item):
    text = url_to_text(item)
    buffer_to_pickle(text)
    return


NUM_LINKS = 10

def wiki_get(get_links):
    se_,index,link,category,buffer = get_links
    url_of_links = str('https://en.wikipedia.org/w/index.php?search=')+str(category)
    links = collect_pubs(url_of_links)
    if len(links) > NUM_LINKS: links = links[0:NUM_LINKS]
    [ process((se_,index,l,category,buffer)) for index,l in enumerate(links) ]

def search_scholar(get_links):
    # from https://github.com/ckreibich/scholar.py/issues/80
    se_,index,link,category,buffer = get_links

    querier = scholar.ScholarQuerier()
    settings = scholar.ScholarSettings()
    querier.apply_settings(settings)
    query = scholar.SearchScholarQuery()

    query.set_words(category)
    links = query.get_url()
    querier.send_query(query)
    if len(links) > NUM_LINKS: links = links[0:NUM_LINKS]
    [ process((se_,index,l,category,buffer)) for index,l in enumerate(links) ]

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
            if str('wiki') in config['keyword']:
                st_ = config['keyword'].split('!wiki')
                search_term = st_[1]
                get_links = (str('wikipedia'),0,None,search_term,None)
                wiki_get(get_links)

            elif str('scholar') in config['keyword']:
                st_ = config['keyword'].split('!scholar')
                search_term = st_[1]
                get_links = (str('scholar'),0,None,search_term,None)
                search_scholar(get_links)
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

                    # map over the function in parallel since it's 2018
                    b = db.from_sequence(get_links,npartitions=8)
                    _ = list(b.map(process).compute())
        except GoogleSearchError as e:
            print(e)
            return None
        print('done scraping')

    def scrapelandtext(self,fi):
        se_,category = fi
        config = {}
        driver = rotate_profiles()
    	# This code block, jumps over gate one (the search engine as a gatekeeper)
        # google scholar or wikipedia is not supported by google scraper
        # duckduckgo bang expansion can be used as to access engines that GS does not support.
        # for example twitter etc

        config['keyword'] = str(category)

        if str('scholar') in se_: config['keyword'] = '!scholar {0}'.format(category)
        if str('wikipedia') in se_ : config['keyword'] = '!wiki {0}'.format(category)
        if str('scholar') in se_ or str('wikipedia') in se_:
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

        self.slat_(config)
        return

    def run(self):
        print(self.iterable)
        self.iterable.insert(0,("duckduckgo",str("!scholar arbitrary test")))
        _ = list(map(self.scrapelandtext,self.iterable))
        return
