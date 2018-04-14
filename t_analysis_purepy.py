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
from nltk import compat
#from nltk.compat import Counter
#from nltk.draw import dispersion_plot

from bs4 import BeautifulSoup
import json
#!pip install git+"https://github.com/russelljjarvis/textstat.git"
from textstat.textstat import textstat

from natsort import natsorted, ns

########################################################################
########################################################################
########################################################################
# Set user parameters based on type of analysis
searchList = ['Play Dough','GMO','Genetically_Modified_Organism','Transgenic','Vaccine', 'Neutron']
NWEB = 5 #number of search websites being implemented (google, google scholar, bing, yahoo, duckduckgo)
numURLs = 49 #number of URLs per search website  (number determined by 1.scrape code)

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

se = {}
se[0] = "google_"
se[1] = "gScholar_"
se[2] = "bing_"
se[3] = "yahoo_"
se[4] = "duckduckgo_"
#NWEB = 5


def map_wrapper(function_item,list_items):
    from dask.distributed import Client
    import dask.bag as db
    c = Client()
    NCORES = len(c.ncores().values())
    b0 = db.from_sequence(list_items, npartitions=NCORES)
    list_items = list(db.map(function_item,b0).compute())
    return list_items


def web_iter(keyword):
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
        file_contents = pickle.load(fileHandle)

        if TEXT_FOUNTAIN == True:
            # Recover the initial text file data, corresponding to both PDFs and html web page content.
            # Used to generate data for people who lack python, reproducibility.
            f = open(str(base_path + fileName)+'.txt','w')
            f.write(str(file_contents.encode('ascii','ignore')))
            f.close()

        if len(file_contents) == 2:
            date_created.append((str(base_path + fileName), file_contents[0]))
            url_text = file_contents[1]

        else:

            url_text = file_contents
        fileHandle.close()

        #initialize dataArray Dictionary


        urlDat['link_rank'] = p
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
        urlDat['keyword'] = keyword
        if 'last_iterator' in fileName:
            break
        if 'unraveled_links' in fileName:
            break
        if 'last_state' in fileName:
            break
        #elif:
        #assert urlDat['se'] is not None

        ########################################################################
        #remove unreadable characters
        url_text = url_text.replace("-", " ") #remove characters that nltk can't read
        textNum = re.findall(r'\d', url_text) #locate numbers that nltk cannot see to analyze
        for x in range(0,len(textNum)) :
            url_text.find(textNum[x])

        URLtext = word_tokenize(url_text)
        URLtext = [w.lower() for w in URLtext] #make everything lower case
        #model = unigram(url_text)
        #urlDat['perplexity'] = perplexity(url_text, model)
        #print(urlDat['perplexity'], 'a bit like shannon entropy of text, but on the level of words as symbols, rather than letters as symbols')
        urlDat['wcount'] = textstat.lexicon_count(str(url_text))
        #sentences
        sents = sent_tokenize(url_text) #split all of text in to sentences
        sents = [w.lower() for w in sents] #lowercase all

        urlDat['sentcount'] = len(sents) #determine number of sentences

        ########################################################################
        ##frequency distribtuion of text
        fdist = FreqDist(w.lower() for w in URLtext if w.isalpha()) #frequency distribution of words only

        # Bug fix
        # cast dict to list
        fd_temp = list(fdist.items())
        urlDat['stfreq'] = fdist[keyword.lower()] #frequency of search term

        #frequency of all words
        fAll = {}
        for x in range(0,len(fd_temp)):
            fAll[x,1], fAll[x,2] = [y.strip('}()",{:') for y in (str(fd_temp[x])).split(',')]

        obj_arr['frequencies'] = sorted([ (f[1],f[0]) for f in fd_temp ],reverse=True)
        number_of_words = sum([ f[0] for f in obj_arr['frequencies'] ])

        probs = [float(c[0]) / number_of_words for c in obj_arr['frequencies'] ]
        probs = [p for p in probs if p > 0.]
        ent = 0
        for p in probs:
            if p > 0.:
                ent -= p * math.log(p, 2)
        obj_arr['eofh'] = ent

        #frequency of the most used n number of words
        frexMost = fdist.most_common(15) #show N most common words
        fM = {}
        for x in range(0,len(frexMost)) :
            fM[x,1], fM[x,2] = [y.strip('}()",{:') for y in (str(frexMost[x])).split(',')]

        ########################################################################
        #Sentiment and Subjectivity analysis
        testimonial = TextBlob(url_text)
        testimonial.sentiment

        urlDat['sp'] = testimonial.sentiment.polarity
        urlDat['ss'] = testimonial.sentiment.subjectivity

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
            obj_arr['raw_text'] = str(url_text)
            obj_arr['urlDat'] = urlDat
            obj_arr['WperS'] = WperS
            obj_arr['sentSyl'] = sentSyl
            obj_arr['fM'] = fM
            obj_arr['fAll'] = fAll
        #obj_arr['visited_files'] = visited_files
        list_per_links.append(obj_arr)
    print(len(lo_query_links) == len(list_per_links))
    #assert len(lo_query_links) == len(list_per_links)
    return list_per_links

#To use functions above with ipython notebook uncomment this code.
'''
import dask.bag as db
from t_analysis_purepy import web_iter, map_wrapper
grid = {}
query_list = ['GMO','Genetically_Modified_Organism','Transgenic','Vaccine', 'Neutron', 'Play Dough']
#grid['search_term'] = query_list #[ (i, q) for i,q in enumerate(query_list) ]
#from sklearn.grid_search import ParameterGrid
#grid = list(ParameterGrid(grid))
#grid = [(dicti['search_term'][0],dicti['search_term'][1]) for dicti in grid ]
#import pdb
#pdb.set_trace()
#import dask.bag as db
grid = db.from_sequence(query_list,npartitions = 8)
#list_per_links = map_wrapper(web_iter,grid)
list_per_links = list(db.map(web_iter,grid).compute());
remove_empty = [i for i in list_per_links if len(i)>0 ]
unravel = []
for i in remove_empty:
    unravel.extend(i)

with open('unraveled_links.p','wb') as handle:
    pickle.dump(unravel,handle)
'''
#import pdb; pdb.set_trace()
#import pandas as pd
#df = pd.DataFrame(data=obj_arr_add)
#print(obj_arr_add)
