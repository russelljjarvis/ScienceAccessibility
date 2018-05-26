# Scientific readability project
# authors: other authors,
# ...,
# Russell Jarvis
# https://github.com/russelljjarvis/
# rjjarvis@asu.edu


# for some reason the docker build does not properly install the fake user_agent, oh well do it again here
# NB move this to the Docker container
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


import pickle
from GoogleScraper import scrape_with_config, GoogleSearchError
from utils_and_paramaters import search_params, engine_dict_list#, map_wrapper
from numpy import random
import pickle

SEARCHLIST, WEB, LINKSTOGET = search_params()
se, _ = engine_dict_list()
flat_iter = [ (b,category) for category in SEARCHLIST for b in range(0,4) ]
random.shuffle(flat_iter)

if not os.path.exists('cached'):
    os.makedirs('cached')
if not os.path.exists('text_dump'):
    os.makedirs('text_dump')
os.chdir('text_dump')
def scrapelandtext(fi):
    b,category = fi
    config = {}
    if b==4:
        config['keyword'] = str('!scholar ')+str(category)
    else:
        config['keyword'] = str(category)
    config['search_engine'] = str(se[b])
    config['scrape_method'] = str('selenium')
    config['num_pages_for_keyword'] = 10
    config['use_own_ip'] = True
    config['sel_browser'] = str('firefox')
    config['do_caching'] = True
    # NB this is only cached snippets
    # of the web pages, this is not a total
    # text dump suitable for analysis
    # It's more just log keeping of what has already been obtained, as opposed to substantial content
    config['output_filename'] = str(category)+str(' ')+str(se[b])+str('.csv')
    try:
        search = scrape_with_config(config)
    except GoogleSearchError as e:
        print(e)

_ = list(map(scrapelandtext,flat_iter))
