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

SENGINES = {0:"google",1:"yahoo",2:"duckduckgo",3:"wikipedia",4:"scholar",5:"bing"}

SEARCHLIST = ["evolution","cancer", "photosysnthesis",'climate change','Vaccines','Transgenic','GMO','Genetically Modified Organism','reality TV', 'unicorn versus brumby', 'football soccer', 'prancercise philosophy', 'play dough delicious deserts']
# Use this variable to later reconcile file names with urls
# As there was no, quick and dirty way to bind the two togethor here, without complicating things later.
# traverse this list randomly as repititve query sequences eminating from simple incremental traversal may be a robot give away.
# configure the scrapers with search terms and search indexs
sw = SW(SENGINES,SEARCHLIST,nlinks=15)
# This line is sufficient to execute the scrapper:
sw.run()
import use_analysis
import use_code_complexity
