# Scientific readability project
# author Russell Jarvis
# https://github.com/russelljjarvis/
# rjjarvis@asu.edu

#import dask
from GoogleScraper import scrape_with_config, GoogleSearchError
from utils_and_paramaters import search_params, engine_dict_list, map_wrapper
SEARCHLIST, WEB, LINKSTOGET = search_params()
se, _ = engine_dict_list()
from numpy import random
flat_iter = [ (b,category) for category in SEARCHLIST for b in range(0,5) ]

def scraplandtext(fi):
    b,category = fi
    
    if b==4:
        temp = {}
        temp['keyword'] = str('!scholar')+str(category)

    else:
        temp = {}
        temp['keyword'] = str(category)

    temp['search_engine'] = str(se[b])
    temp['scrape_method'] = str('selenium')
    #temp['scrape_method'] = str('http-async')

    temp['num_pages_for_keyword'] = 15
    temp['use_own_ip'] = True
    temp['sel_browser'] = str('chrome')
    temp['do_caching'] = True
    temp['output_filename'] = str(category)+str(se[b])+str('.csv')
    print(temp)
    scrape_with_config(temp)
_ = list(map(scraplandtext,flat_iter))
