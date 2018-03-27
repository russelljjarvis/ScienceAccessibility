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
searchList = ['GMO','Genetically_Modified_Organism','Transgenic','Vaccine']
nweb = 4 #number of search websites being implemented (google, google scholar, bing, yahoo)
numURLs = 26 #number of URLs per search website  (number determined by 1.scrape code)

#also save these parameters for analysis purposes
spec_dict = { 'searchList':searchList, 'nweb':nweb, 'numURLs':numURLs}
handle = 'Data/analysisSpecs.mat'
scipy.io.savemat(handle, mdict=spec_dict, oned_as='row')
handle = None
TEXT_FOUNTAIN = False
########################################################################
########################################################################
########################################################################
#what are we analyzing???? - this is the list of text analysis features
infoDat = {}
infoDat[1,1] = "Number of Words"
infoDat[2,1] = "Number of Sentences"
infoDat[3,1] = "Frequency of Search Term"
infoDat[4,1] = "Sentiment Analysis"
infoDat[5,1] = "Subjectivity Analysis"
infoDat[6,1] = "Grade level"
infoDat[7,1] = "Flesch Reading Ease"
infoDat[8,1] = "SMOG Index"
infoDat[9,1] = "Coleman Liau"
infoDat[10,1] = "Automated Readability Index"
infoDat[11,1] = "Gunning Fog"
infoDat[12,1] = "Dale Chall Readability Score"
infoDat[13,1] = "Difficult Words"
infoDat[14,1] = "Linsear Write Formula"

#save these parameters for analysis purposes
infoDat = list(infoDat.items())
handle = 'Data/analysisInfo.mat'
scipy.io.savemat(handle, {'infoDat':infoDat})
handle = None
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

nweb = 4


def map_wrapper(function_item,list_items):
    from dask.distributed import Client
    import dask.bag as db
    c = Client()
    NCORES = len(c.ncores().values())
    b0 = db.from_sequence(list_items, npartitions=NCORES)
    list_items = list(db.map(function_item,b0).compute())
    return list_items


def web_iter(args):
    i,keyword,b = args
    os.chdir(fileLocation +str('/') + str(keyword) +'/')

    #textName = 
    # grab all the file names ending with pickle suffix.
    lo_query_links = natsorted(glob.glob(+r'*.p'))
    print(lo_query_links)
    print(se[b])
    # select only a subset of them.str(se[b])
    lo_query_links =  natsorted(lo_query_links[0:numURLs-1])
    list_per_links = []
    for p,fileName in enumerate(lo_query_links):
        

        print ("Analyzing Search Engine " + str(se[b]) + " of " + str(nweb) + ": Link " + str(p)); print ("");

        fileHandle = open(fileName, 'rb');
        file_contents = pickle.load(fileHandle)

        if TEXT_FOUNTAIN == True:
            # Recover the initial text file data, corresponding to both PDFs and html web page content.
            # Used to generate data for people who lack python, reproducibility.
            f = open(str(fileName)+'.txt','w')
            f.write(str(file_contents.encode('ascii','ignore')))
            f.close()

        if len(file_contents) == 2:
            date_created.append((str(fileName), file_contents[0]))
            url_text = file_contents[1]

        else:

            url_text = file_contents
        fileHandle.close()

        #initialize dataArray Dictionary
        urlDat = {}
        urlDat['link_rank'] = p
        print(urlDat['link_rank'])
        urlDat['se'] = se[b]
        urlDat['keyword'] = keyword
        

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

        # Bug fix
        # cast dict to list
        fd_temp = list(fdist.items())
        #keyword
        urlDat['stfreq'] = fdist[keyword.lower()] #frequency of search term

        #frequency of all words
        fAll = {}
        for x in range(0,len(fd_temp)):
            fAll[x,1], fAll[x,2] = [y.strip('}()",{:') for y in (str(fd_temp[x])).split(',')]

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
            # https://github.com/shivam5992/textstat
            # explanation of metrics    
            urlDat['fkg']  = textstat.flesch_kincaid_grade(str(url_text))
            urlDat['fre'] = textstat.flesch_reading_ease(str(url_text))
            urlDat['smog']  = textstat.smog_index(str(url_text))
            urlDat['cliau']  = textstat.coleman_liau_index(str(url_text))
            urlDat['ri']  = textstat.automated_readability_index(str(url_text))
            urlDat['gf'] = textstat.gunning_fog(str(url_text))
            urlDat['gl'] =  textstat.grade_level(str(url_text))
            urlDat['dcr']  = textstat.dale_chall_readability_score(str(url_text))
            urlDat['dw']  = textstat.difficult_words(str(url_text))
            urlDat['lwf']  = textstat.linsear_write_formula(str(url_text))
            urlDat['standard']  = textstat.text_standard(str(url_text))
            '''
            infoDat[6,1] = "Grade level"
            infoDat[7,1] = "Flesch Reading Ease"
            infoDat[8,1] = "SMOG Index"
            infoDat[9,1] = "Coleman Liau"
            infoDat[10,1] = "Automated Readability Index"
            infoDat[11,1] = "Gunning Fog"
            infoDat[12,1] = "Dale Chall Readability Score"
            infoDat[13,1] = "Difficult Words"
            infoDat[14,1] = "Linsear Write Formula"
            '''
            

           
            obj_arr = {}
            obj_arr['urlDat'] = urlDat
            obj_arr['WperS'] = WperS
            obj_arr['sentSyl'] = sentSyl
            obj_arr['fM'] = fM
            obj_arr['fAll'] = fAll
            if type(obj_arr) is not None:
                list_per_links.append(obj_arr)
            
            #obj_arr = [urlDat, WperS, sentSyl, fM, fAll]

            
            
            
            #, WperS, sentSyl, fM, fAll]
            '''

            assert len(fAll) != 0
            assert len(fM) != 0
            assert len(sentSyl) != 0
            assert len(obj_arr[-1])!= 0
            assert len(obj_arr[-2])!= 0
            assert len(obj_arr[-3])!= 0
            assert type(obj_arr) is not type(None)
                
            f = open('last_iterator.p', 'wb')
            fi = [i,keyword, obj_arr]
            pickle.dump(fi,f)
            fi = None
            '''
            # File path is equivalent to Term.mat

    return list_per_links

def finish_up(obj_arr_add):

    obj_arr_add = [ i for i in obj_arr_add  if i is not type(None) ]
    obj_arr = obj_arr_add[0]
    for oaa in obj_arr_add[1:-1]:
        print(np.shape(oaa), np.shape(obj_arr))
    return

#sl = [ (i, keyword, b) for i, keyword in enumerate(searchList) for b in range(0,nweb) ]

'''
import dask.bag as db
grid = {}
grid['b']=[0,1,2,3]
query_list = ['GMO','Genetically_Modified_Organism','Transgenic','Vaccine']
grid['search_term'] = [ (i, q) for i,q in enumerate(query_list) ]
from sklearn.grid_search import ParameterGrid
grid = list(ParameterGrid(grid))
grid = [(dicti['search_term'][0],dicti['search_term'][1],dicti['b']) for dicti in grid ]
#grid = db.from_sequence(grid,npartitions = 8)
list_per_links = list(db.map(web_iter,grid).compute())
#import pdb; pdb.set_trace()
import pandas as pd
df = pd.DataFrame(data=obj_arr_add)
print(obj_arr_add)
#df
'''
'''
import dask.bag as db
#sl = [ (i, keyword, b) for i, keyword in enumerate(searchList) for b in range(0,nweb) ]
b0 = db.from_sequence(sl)
obj_arr_add = list(db.map(web_iter,b0).compute())
obj_arr = finish_up(obj_arr_add)
'''



# For all of these,
# I think it may be best if we keep text complexity on the y axes,
# mainly for ease of reading the graphs. For the correlation
# it won’t really matter which way it goes, as these both seem to be independent;
# for the others, I think bar charts would work with complexity on the
# y axes… so I figure we should stay consistent as there isn’t a real
# reason to change for #1.
# I’m having a brain fart right now… did we get
# the sentimentality analysis figured out (pro vs. con vs. neutral)?
# If not, I’m willing to work on going through and judging them one by one…
# But as for the figures, here are 3 ideas to start
# 1.       Text complexity vs site ranking
# (I think this would be really cool to see in general; do more popular sites,
#  in general, have lower complexity?), likely pooled for each major subject
# (e.g., GMO and transgenics results pooled together)

# 2.       Pro/anti/neutral vs. text complexity#

# 3.       GMO/transgenics vs. text complexity



#:
