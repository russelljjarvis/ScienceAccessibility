#general python imports
import os
import dask
import matplotlib # Its not that this file is responsible for doing plotting, but it calls many modules that are, such that it needs to pre-empt
# setting of an appropriate backend.
matplotlib.use('Agg')
import sys
import numpy
import numpy as np
import scipy
import scipy.io as sio
import math
import re
#import requests
import time
from tabulate import tabulate
from textblob import TextBlob
import glob
import pickle

#text analysis imports
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
import os
os.system('pip install natsort')

from nltk.tag.perceptron import PerceptronTagger
tagger = PerceptronTagger(load=False)

from nltk import word_tokenize,sent_tokenize
from nltk import sent_tokenize, word_tokenize, pos_tag
from nltk.probability import FreqDist
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.corpus import cmudict
from nltk.sentiment import SentimentAnalyzer
from nltk import NgramAssocMeasures
#pmi as nentropy
mi = NgramAssocMeasures.mi_like

from nltk import compat
#from nltk.compat import Counter
#from nltk.draw import dispersion_plot

from bs4 import BeautifulSoup
import json
#!pip install git+"https://github.com/russelljjarvis/textstat.git"
from textstat.textstat import textstat

from natsort import natsorted, ns

import pandas as pd

########################################################################
########################################################################
########################################################################
# Set user parameters based on type of analysis
searchList = ['Play Dough','GMO','Genetically_Modified_Organism','Transgenic','Vaccine', 'Neutron']
NWEB = 5 #number of search websites being implemented (google, google scholar, bing, yahoo, duckduckgo)
numURLs = 50 #number of URLs per search website  (number determined by 1.scrape code)

#also save these parameters for analysis purposes
spec_dict = { 'searchList':searchList, 'nweb':NWEB, 'numURLs':numURLs}
handle = 'Data/analysisSpecs.mat'
scipy.io.savemat(handle, mdict=spec_dict, oned_as='row')
handle = None
TEXT_FOUNTAIN = False
########################################################################
########################################################################
########################################################################
#set filePath below to specify where the data will be going after the code runs
fileLocation = os.getcwd()

if not os.path.exists(fileLocation):
    os.makedirs(fileLocation)

date_created = []
import pickle
import os


import utils
se, _ = utils.engine_dict_list()
#NWEB = 5


def map_wrapper(function_item,list_items):
    from dask.distributed import Client
    import dask.bag as db
    c = Client()
    NCORES = len(c.ncores().values())
    b0 = db.from_sequence(list_items, npartitions=NCORES)
    list_items = list(db.map(function_item,b0).compute())
    return list_items


def web_iter(keyword, frames = False):
    #keyword = args
    visited_files = []
    # grab all the file names ending with pickle suffix.
    base_path = fileLocation + str('/') + str(keyword)
    lo_query_links = natsorted(glob.glob(str(base_path)+'/*.p'))
    lo_query_links =  natsorted(lo_query_links[0:numURLs-1])
    list_per_links = []

    for p,fileName in enumerate(lo_query_links):
        urlDat = {}
        obj_arr = {}
        fileHandle = open(fileName, 'rb');
        visited_files.append(fileHandle)
        print(keyword,fileHandle,'location before crash')
        file_contents = pickle.load(fileHandle)
        fileHandle.close()

        if TEXT_FOUNTAIN == True:
            # Recover the initial text file data, corresponding to both PDFs and html web page content.
            # Used to generate data for people who lack python, reproducibility.
            f = open(str(base_path + fileName)+'.txt','w')
            f.write(str(file_contents.encode('ascii','ignore')))
            f.close()

        date_created.append((str(base_path + fileName), file_contents[0]))
        url_text = file_contents[1]

        #initialize dataArray Dictionary

        if len(file_contents)==3:
            print('crashes in file type read')
            print(str(file_contents[2]))
            urlDat['link_string'] = str(file_contents[2])
        urlDat['link_rank'] = p
        urlDat['keyword'] = keyword


        print(urlDat['link_rank'])
        if 'google_' in fileName:
            urlDat['se'] = 'google_'#se[b]
        if 'gScholar_' in fileName:
            urlDat['se'] = 'gScholar_'#se[b]
        if 'yahoo_' in fileName:
            urlDat['se'] = 'yahoo_'#se[b]
        if 'duckduckgo_' in fileName:
            urlDat['se'] = 'duckduckgo_'#se[b]
        if 'bing_' in fileName:
            urlDat['se'] = 'bing_'#se[b]
        assert type(urlDat['se']) is not None

        ########################################################################
        #remove unreadable characters
        url_text = url_text.replace("-", " ") #remove characters that nltk can't read
        textNum = re.findall(r'\d', url_text) #locate numbers that nltk cannot see to analyze
        for x in range(0,len(textNum)) :
            url_text.find(textNum[x])

        URLtext = word_tokenize(url_text)
        URLtext = [w.lower() for w in URLtext] #make everything lower case
        urlDat['wcount'] = textstat.lexicon_count(str(url_text))
        #sentences
        sents = sent_tokenize(url_text) #split all of text in to sentences
        sents = [w.lower() for w in sents] #lowercase all

        urlDat['sentcount'] = len(sents) #determine number of sentences

        ########################################################################
        ##frequency distribtuion of text
        fdist = FreqDist(w.lower() for w in URLtext if w.isalpha()) #frequency distribution of words only

        # cast dict to list
        fd_temp = list(fdist.items())
        urlDat['stfreq'] = fdist[keyword.lower()] #frequency of search term

        #frequency of all words
        fAll = {}
        for x in range(0,len(fd_temp)):
            fAll[x,1], fAll[x,2] = [y.strip('}()",{:') for y in (str(fd_temp[x])).split(',')]

        urlDat['frequencies'] = sorted([ (f[1],f[0]) for f in fd_temp ],reverse=True)
        number_of_words = sum([ f[0] for f in urlDat['frequencies'] ])

        probs = [float(c[0]) / number_of_words for c in urlDat['frequencies'] ]
        probs = [p for p in probs if p > 0.]
        ent = 0
        for p in probs:
            if p > 0.:
                ent -= p * math.log(p, 2)
        urlDat['eofh'] = ent

        #frequency of the most used n number of words
        frexMost = fdist.most_common(15) #show N most common words
        urlDat['frexMost'] = frexMost
        fM = {}
        for x in range(0,len(frexMost)) :
            fM[x,1], fM[x,2] = [y.strip('}()",{:') for y in (str(frexMost[x])).split(',')]

        ########################################################################
        #Sentiment and Subjectivity analysis
        testimonial = TextBlob(url_text)
        urlDat['sp'] = testimonial.sentiment.polarity
        urlDat['ss'] = testimonial.sentiment.subjectivity

            #break
        #else:
        ########################################################################
        #determine syllable count for all words in each sentece
        sentSyl = {}
        WperS = {}
        # for n,sent in enumerate(sents):
        # future use
        for n in range(0,len(sents)):

            #setup sent variable to analyze each sentence individually
            sent = sents[n] #select sentence n in total text
            sent = word_tokenize(sent) #tokenize sentence n in to words
            sent = [w.lower() for w in sent if w.isalpha()] #remove any non-text

            WperS[n] = len(sent) #number of words per sentence

            #syllable analysis
            for x in range(0,len(sent)):
                word = sent[x]
                # Count the syllables in the word.
                syllables = textstat.syllable_count(str(word))
                sentSyl[n,x] = syllables

        if len(URLtext) != 0:
            # explanation of metrics
            # https://github.com/shivam5992/textstat
            urlDat['fkg']  = textstat.flesch_kincaid_grade(str(url_text))


            urlDat['fre'] = textstat.flesch_reading_ease(str(url_text))
            urlDat['smog']  = textstat.smog_index(str(url_text))
            urlDat['cliau']  = textstat.coleman_liau_index(str(url_text))
            urlDat['ri']  = textstat.automated_readability_index(str(url_text))
            urlDat['gf'] = textstat.gunning_fog(str(url_text))
            #print(dir(textstat))
            #urlDat['gl'] =  textstat.grade_level(str(url_text))
            urlDat['dcr']  = textstat.dale_chall_readability_score(str(url_text))
            urlDat['dw']  = textstat.difficult_words(str(url_text))
            urlDat['lwf']  = textstat.linsear_write_formula(str(url_text))
            urlDat['standard']  = textstat.text_standard(str(url_text))
            urlDat['file_path'] = fileHandle
            urlDat['WperS'] = WperS
            urlDat['sentSyl'] = sentSyl
            urlDat['fM'] = fM
            urlDat['fAll'] = fAll

        if len(list_per_links) == 0:
            dfs = pd.DataFrame(pd.Series(urlDat)).T
        dfs = pd.concat([ dfs, pd.DataFrame(pd.Series(urlDat)).T ])
        if textstat.flesch_kincaid_grade(str(url_text)) > 100.0:
            objarr = {}
        list_per_links.append(urlDat)
    if frames == False:

        print(len(list_per_links))
        return list_per_links
    else:
        return dfs

#To use functions above with ipython notebook uncomment this code.
import dask.bag as db
grid = {}
query_list = ['GMO','Genetically_Modified_Organism','Transgenic','Vaccine', 'Neutron', 'Play Dough']
'''
grid = db.from_sequence(query_list,npartitions = 8)
#list_per_links = map_wrapper(web_iter,grid)
list_per_links = list(map(web_iter,grid))
remove_empty = [i for i in list_per_links if len(i)>0 ]
unravel = []
for i in remove_empty:
    unravel.extend(i)
#print(unravel)

with open('unraveled_links.p','wb') as handle:
    pickle.dump(unravel,handle)
'''
