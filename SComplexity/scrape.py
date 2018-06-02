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
from delver import Crawler
from GoogleScraper import scrape_with_config, GoogleSearchError
from SComplexity.crawl import html_to_txt, convert_pdf_to_txt, print_best_text
import tempfile
import pickle
# from SComplexity.utils_and_paramaters import search_params, engine_dict_list, search_known_corpus

C = Crawler()
CWD = os.getcwd()

display = Display(visible=0, size=(1024, 768))
display.start()


useragent = UserAgent()
# Rotate through random user profiles.
profile = webdriver.FirefoxProfile()

def rotate_profiles():
    driver = None
    profile.set_preference("general.useragent.override", useragent.random)
    profile.set_preference("javascript.enabled", True)
    driver = webdriver.Firefox(firefox_profile=profile)
    return driver
driver = rotate_profiles()

def convert(fileName):
    b = os.path.getsize(fileName)
    text = None
    try: # this is just to prevent reading in of incomplete data.
        file = open(fileName)
        if str('zip') in fileName:
            pass
        elif str('.html') in fileName:
            text = html_to_txt(file)
        elif str('.pdf') in fileName:
            text = convert_pdf_to_txt(file)
        else:
            try:
                print('probably html')
                text = html_to_txt(file)
            except:
                text = None 
                print('perhaps video or image')
        file.close()
    except:
        text = None
    return text

def url_to_file(link_tuple):
    se_b, page_rank, link, category = link_tuple

    fname = '{0}_{1}_{2}'.format(category,se_b,page_rank)
    # Bulk download wht is scrapped by GS.
    if str('pdf') in link:
        fname = '{0}.{1}'.format(fname,str('pdf'))
    if str('html') in link:
        fname = '{0}.{1}'.format(fname,str('html'))
    if str('other') in link:
        fname = '{0}.{1}'.format(fname,str('other'))


    # note it's possible that downloaded link is neither html, nor pdf (ie jpg). Incorrectly assigning extensions to such resources will cause
    # problems further down the road.
    try:
        #f = tempfile.NamedTemporaryFile(delete=True)
        local_file_path = C.download(local_path = CWD, url = link, name = fname)

        #text = convert(local_file_path)
        if os.path.isfile(local_file_path):
            #f.close()
            pname = '{0}.p'.format(fname)#local_file_path.split(".")[0])
            file_contents = [link_tuple, local_file_path]
            with open(pname,'wb') as f:
                pickle.dump(file_contents,f)
        print('success')
    except:
        print('failure')
    return


class SW(object):
    def __init__(self,nlinks=10):
        self.NUM_LINKS = nlinks


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
        plm = {}

        try:
            search = scrape_with_config(config)

            links = []
            for serp in search.serps:
                print(serp)
                links.extend([link.link for link in serp.links])
            #links = [ (l,config) for l in links ]
            # This code block jumps over gate two
            # The (possibly private, or hosted server as a gatekeeper).
            if len(links) > self.NUM_LINKS: links = links[0:self.NUM_LINKS]
            if len(links) > 0:
                print(links)
                get_links = ( (se_,index,link,category) for index, link in enumerate(links) )
                _ = list(map(url_to_file,get_links))

        except GoogleSearchError as e:
            print(e)
            return None
        return
# Use this variable to later reconcile file names with urls
# As there was no, quick and dirty way to bind the two togethor here, without complicating things later.
