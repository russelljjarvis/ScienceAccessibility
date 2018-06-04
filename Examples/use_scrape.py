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
from SComplexity.scrape import SW

LINKSTOGET= 10 #number of links to pull from each search engine (this can be any value, but more processing with higher number)


def engine_dict_list():
    se = {0:"google",1:"yahoo",2:"duckduckgo",3:"wikipedia",4:"scholar",5:"bing"}
    return se, list(se.values())

def search_params():
    SEARCHLIST = ["evolution","cancer", "photosysnthesis",'climate change','Vaccines','Transgenic','GMO','Genetically Modified Organism','reality TV', 'unicorn versus brumby', 'football soccer', 'prancercise philosophy', 'play dough delicious deserts']
    return SEARCHLIST, se, LINKSTOGET
# Use this variable to later reconcile file names with urls
# As there was no, quick and dirty way to bind the two togethor here, without complicating things later.
se, _ = engine_dict_list()

SEARCHLIST, se, LINKSTOGET = search_params()
flat_iter = [ (se[b],category) for category in SEARCHLIST for b in range(0,4) ]

# traverse this list randomly as hierarchial traversal may be a bot give away.
random.shuffle(flat_iter)

# configure the scrapers with search terms and search indexs
sw = SW(flat_iter,nlinks=15)
# This line is sufficient to execute the scrapper:
sw.run()
import use_analysis
