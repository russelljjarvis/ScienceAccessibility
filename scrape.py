# Scientific readability project
# authors: other authors,
# ...,
# Russell Jarvis
# https://github.com/russelljjarvis/
# rjjarvis@asu.edu


# for some reason the docker build does not properly install the fake user_agent, oh well do it again here
import os
os.system('sudo /opt/conda/bin/pip install fake_useragent')

import selenium
from pyvirtualdisplay import Display
from selenium import webdriver

display = Display(visible=0, size=(1024, 768))
display.start()
driver = webdriver.Firefox()
from fake_useragent import UserAgent
ua = UserAgent()


from GoogleScraper import scrape_with_config, GoogleSearchError
from utils_and_paramaters import search_params, engine_dict_list#, map_wrapper
SEARCHLIST, WEB, LINKSTOGET = search_params()
se, _ = engine_dict_list()
from numpy import random
flat_iter = [ (b,category) for category in SEARCHLIST for b in range(0,5) ]
random.shuffle(flat_iter)
random.shuffle(flat_iter)

def scrapelandtext(fi):
    b,category = fi
    if b==4:
        temp = {}
        temp['keyword'] = str('!scholar ')+str(category)
    elif b ==5:
        temp = {}
        temp['keyword'] = str('!bing ')+str(category)
    else:
        temp = {}
        temp['keyword'] = str(category)

    temp['search_engine'] = str(se[b])
    temp['scrape_method'] = str('selenium')
    # asynchronous is preferred, does it work?
    # temp['scrape_method'] = str('http-async')
    
    temp['num_pages_for_keyword'] = 15
    temp['use_own_ip'] = True
    temp['sel_browser'] = str('firefox')
    temp['do_caching'] = True
    temp['output_filename'] = str(category)+str(se[b])+str('.csv')
    try:
        search = scrape_with_config(temp)
    except GoogleSearchError as e:
        print(e)

        # let's inspect what we got
        
    for serp in search.serps:
        print(serp)
        

#stuff = []
#for fi in flat_iter:
#    stuff.append(scrapelandtext(fi))
_ = list(map(scrapelandtext,flat_iter))
