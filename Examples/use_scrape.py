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


import pickle
from SComplexity.scrape import scrapelandtext

def engine_dict_list():
    se = {0:"google",1:"yahoo",2:"duckduckgo",3:"wikipedia",4:"scholar",5:"bing"}
    return se, list(se.values())

def search_params():
    SEARCHLIST = ["autosomes","respiration", "bacteriophage",'Neutron','Vaccine','Transgenic','GMO','Genetically Modified Organism','neuromorphic hardware', 'mustang unicorn', 'scrook rgerkin neuron', 'prancercise philosophy', 'play dough delicious deserts']


    LINKSTOGET = 5 #number of links to pull from each search engine (this can be any value, but more processing with higher number)
    return SEARCHLIST, se, LINKSTOGET

def search_known_corpus():
    SEARCHLIST = []
    LINKSTOGET = []
    SEARCHLIST = [str('rcgerkin'),str('smcrook'), str('s jarvis optogenetics'), str('Patrick mcgurrin ASU'), str('Melanie jarvis neonate')]
    LINKSTOGET = []
    LINKSTOGET.append(str('https://academic.oup.com/beheco/article-abstract/29/1/264/4677340'))
    LINKSTOGET.append(str('http://splasho.com/upgoer5/library.php'))
    LINKSTOGET.append(str('https://elifesciences.org/download/aHR0cHM6Ly9jZG4uZWxpZmVzY2llbmNlcy5vcmcvYXJ0aWNsZXMvMjc3MjUvZWxpZmUtMjc3MjUtdjIucGRm/elife-27725-v2.pdf?_hash=WA%2Fey48HnQ4FpVd6bc0xCTZPXjE5ralhFP2TaMBMp1c%3D'))
    LINKSTOGET.append(str('https://scholar.google.com/scholar?hl=en&as_sdt=0%2C3&q=Patrick+mcgurrin+ASU&btnG='))
    LINKSTOGET.append(str('https://scholar.google.com/citations?user=GzG5kRAAAAAJ&hl=en&oi=sra'))
    LINKSTOGET.append(str('https://scholar.google.com/citations?user=xnsDhO4AAAAJ&hl=en&oe=ASCII&oi=sra'))
    LINKSTOGET.append(str('https://scholar.google.com/citations?user=2agHNksAAAAJ&hl=en&oi=sra'))
    #_, ses = engine_dict_list()
    #WEB = len(ses) #how many search engines to include (many possible- google google scholar bing yahoo)
    LINKSTOGET= 10 #number of links to pull from each search engine (this can be any value, but more processing with higher number)
    se, ses = engine_dict_list()
    return SEARCHLIST, se, LINKSTOGET
# Use this variable to later reconcile file names with urls
# As there was no, quick and dirty way to bind the two togethor here, without complicating things later.
COMPETITION = False
se, _ = engine_dict_list()

if COMPETITION:
    SEARCHLIST, se_, LINKSTOGET = search_known_corpus()
    flat_iter = [ category for category in SEARCHLIST ]
    # traverse this list randomly as hierarchial traversal may be a bot give away.
    random.shuffle(flat_iter)
    flat_iter = [ (se[4],f) for f in flat_iter ]
    # TODO check if lazy evaluation works.
    # flat_iter = ( (se[4],f) for f in flat_iter )


else:
    SEARCHLIST, se, LINKSTOGET = search_params()
    flat_iter = [ (se[b],category) for category in SEARCHLIST for b in range(0,4) ]
    # traverse this list randomly as hierarchial traversal may be a bot give away.
    random.shuffle(flat_iter)
    # TODO check if lazy evaluation works.
    flat_iter = iter(flat_iter)

path_link_maps = list(map(scrapelandtext,flat_iter))
with open('path_link_maps.p','wb') as f: pickle.dump(path_link_maps,f)
