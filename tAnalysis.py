#set parameters- THESE ARE ALL USER DEFINED
#searchList = ['GMO']
import os

import matplotlib # Its not that this file is responsible for doing plotting, but it calls many modules that are, such that it needs to pre-empt
# setting of an appropriate backend.
matplotlib.use('Agg')
# Uncomment to enable parallelization.
import sys
import os
'''
os.system('ipcluster start -n4 --profile=default &')
os.system('sleep 3')
import ipyparallel as ipp
from ipyparallel import depend, require, dependent
rc = ipp.Client(profile='default')
dview = rc[:]
'''

searchList = ['/GMO','/Genetically Modified Organism']
#searchList = ['Transgenic','Vaccine']

web = 4 #number of search websites being implemented (google, google scholar, bing, yahoo)
numURLs = 50 #number of URLs per search website  (number determined by 1.scrape code)

#set filePath below to specify where the text Data is located on your machine
#FileLocation = '/Users/PMcG/Dropbox(ASU)/AAB_files/Pat-files/WCP/code/Data Files/'
fileLocation = os.getcwd() + str('/dataFiles')
#if you're switchign computers you can use this to indicate a second location to use if the first doesn't exist
#if not os.path.exists(FileLocation):
#   FileLocaton = 'D:/Dropbox (ASU)/RESEARCH/Pat_Projects/textAnalyze/'


##once the above is set you can run the code!
#this code assumes you've run the ScrapLinksandText code - it requires the text files it generates

########################################################################
#call in necessary packages that code requires to operate and define additional vars
import numpy
import numpy as np
import scipy.io as sio
import math
import re
from bs4 import BeautifulSoup
import matplotlib
import json
import requests

import nltk
from nltk import sent_tokenize, word_tokenize, pos_tag
from nltk.probability import FreqDist
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.corpus import cmudict
from nltk.sentiment import SentimentAnalyzer
from nltk import compat
#from nltk.compat import Counter
from nltk.draw import dispersion_plot

from textstat.textstat import textstat
import time
from tabulate import tabulate
from textblob import TextBlob
########################################################################
#import ipyparallel

for s, value in enumerate(searchList):

    #set filepath where data is saved
    os.chdir(fileLocation + str(value))

    ##start analysis code
    print (" "); print ("###############################################")
    print (" "); print ("Term {0} of {1} : {2}".format(s+1 , str(len(searchList)), value))
    print (" "); print ("###############################################")
    web = ["google_","gScholar_","bing_","yahoo_"]

    flattened = [ (p,b,textName) for b, textName in enumerate(web) for p in range(0,numURLs) ]

    def map_search(flattened):
        p,b,textName = flattened
        #import pdb; pdb.set_trace()
        print ("-------------------------------------------")
        print ("Analyzing Search Engine " + str(b+1) + " of " + str(web) + ": Link " + str(p+1)); print ("");

        #open and read text q
        fileName = '{0}{1}.txt'.format(textName,p+1)
        print(fileName)
        fileHandle = open(fileName, 'r');
        url_text = fileHandle.read()
        fileHandle.close()

        #initialize dataArray Dictionary
        urlDat = {}
        urlDat[1,1] = "Number of Words"
        urlDat[2,1] = "Number of Sentences"
        urlDat[3,1] = "Frequency of Search Term"
        urlDat[4,1] = "Sentiment Analysis"
        urlDat[5,1] = "Subjectivity Analysis"
        urlDat[6,1] = "Grade level"
        urlDat[7,1] = "Flesch Reading Ease"
        urlDat[8,1] = "SMOG Index"
        urlDat[9,1] = "Coleman Liau"
        urlDat[10,1] = "Automated Readability Index"
        urlDat[11,1] = "Gunning Fog"
        urlDat[12,1] = "Dale Chall Readability Score"
        urlDat[13,1] = "Difficult Words"
        urlDat[14,1] = "Linsear Write Formula"
        urlDat[15,1] = "Text Standard"

        ########################################################################
        #remove unreadable characters
        url_text = url_text.replace("-", " ") #remove characters that nltk can't read
        textNum = re.findall(r'\d', url_text) #locate numbers that nltk cannot see to analyze
        for x in range(0,len(textNum)) :
            url_text.find(textNum[x])

        ########################################################################
        ##Splitting text into:
        #words.
        URLtext = word_tokenize(url_text)
        URLtext = [w.lower() for w in URLtext] #make everything lower case

        urlDat[1,2] = textstat.lexicon_count(str(url_text))

        #sentences
        sents = sent_tokenize(url_text) #split all of text in to sentences
        sents = [w.lower() for w in sents] #lowercase all

        urlDat[2,2]   = len(sents) #determine number of sentences

        ########################################################################
        ##frequency distribtuion of text
        fdist = FreqDist(w.lower() for w in URLtext if w.isalpha()) #frequency distribution of words only
        ##
        # Note casting the dictionary to a list is probably bad for long term code maintainability.
        # probably the same fAll = {} can be created
        # iterating through key value pairs of dictionaries
        # with the idiom:
        # for key, value in fdist.items():
        #    key, value
        ##
        fd_temp = list(fdist.items())

        urlDat[3,2] = fdist[searchList[s].lower()] #frequency of search term
        frexMost = fdist.most_common(15) #show N most common words

        fAll = {}
        for x in range(0,len(fd_temp)):
            fAll[x,1], fAll[x,2] = [y.strip('}()",{:') for y in (str(fd_temp[x])).split(',')]
        ##

        fM = {}
        for x in range(0,len(frexMost)) :
            fM[x,1], fM[x,2] = [y.strip('}()",{:') for y in (str(frexMost[x])).split(',')]
        ##

        #identify long words based on word length of n characters
        #long_words = [w for w in words if len(w) > 8] #last number is character length
        #sorted(long_words)

        ########################################################################
        ##determine syllable count for all words in each sentece
        sentSyl = {}
        WperS = {}
        # def sentence_processing(sent):
        # TODO turn this nested for loop into a map.
        # only problem is this
        for n,sent in enumerate(sents):
            #setup sent variable to analyze each sentence individually
            sent = word_tokenize(sent) #tokenize sentence n in to words
            sent = [w.lower() for w in sent if w.isalpha()] #remove any non-text

            WperS[n] = len(sent) #number of words per sentence

            #syllable analysis
            for word in sent:

                # Count the syllables in the word.
                syllables = textstat.syllable_count(str(word))
                sentSyl[n,x] = syllables

        ########################################################################
        ## Complexity Analysis
        urlDat[6,2]  = textstat.flesch_kincaid_grade(str(url_text))
        urlDat[7,2] = textstat.flesch_reading_ease(str(url_text))
        urlDat[8,2]  = textstat.smog_index(str(url_text))
        urlDat[9,2]  = textstat.coleman_liau_index(str(url_text))
        urlDat[10,2]  = textstat.automated_readability_index(str(url_text))
        urlDat[11,2] = textstat.gunning_fog(str(url_text))

        urlDat[12,2]  = textstat.dale_chall_readability_score(str(url_text))
        urlDat[13,2]  = textstat.difficult_words(str(url_text))
        urlDat[14,2]  = textstat.linsear_write_formula(str(url_text))
        urlDat[15,2]  = textstat.text_standard(str(url_text))

        ########################################################################
        ##defining part of speech for each word
        from nltk.tag.perceptron import PerceptronTagger

        tagger = PerceptronTagger(load=False)

        wordsPOS = pos_tag([w.lower() for w in URLtext if w.isalpha()])

        PS = {}
        for x in range(0,len(wordsPOS)) :
            PS[x,1], PS[x,2] = [y.strip('}()",{:') for y in (str(wordsPOS[x])).split(',')]

        ########################################################################
        ##Sentiment and Subjectivity analysis
        testimonial = TextBlob(url_text)
        testimonial.sentiment

        urlDat[4,2] = testimonial.sentiment.polarity
        urlDat[5,2] = testimonial.sentiment.subjectivity

        #print it all pretty-like
        plotDat = [[str(urlDat[1,1]) + ": " + str(urlDat[1,2])], [str(urlDat[2,1]) + ": " + str(urlDat[2,2])],
                       [str(urlDat[3,1]) + ": " + str(urlDat[3,2])], [str(urlDat[4,1]) + ": " + str(urlDat[4,2])],
                       [str(urlDat[5,1]) + ": " + str(urlDat[5,2])], [str(urlDat[6,1]) + ": " + str(urlDat[6,2])],
                       [str(urlDat[7,1]) + ": " + str(urlDat[7,2])], [str(urlDat[8,1]) + ": " + str(urlDat[8,2])],
                       [str(urlDat[9,1]) + ": " + str(urlDat[9,2])], [str(urlDat[10,1]) + ": " + str(urlDat[10,2])],
                       [str(urlDat[11,1]) + ": " + str(urlDat[11,2])], [str(urlDat[12,1]) + ": " + str(urlDat[12,2])],
                       [str(urlDat[13,1]) + ": " + str(urlDat[13,2])], [str(urlDat[14,1]) + ": " + str(urlDat[14,2])],
                       [str(urlDat[15,1]) + ": " + str(urlDat[15,2])]]

        headers = ["Complexity Results:"]; print (tabulate(plotDat,headers,tablefmt="simple",stralign="left"))
        time.sleep(1); print (""); print (""); print ("");
        ########################################################################
        ##convert all dict variables to list for multidimensional conversion to matlab cell array
        urlDat = urlDat.items()
        sentSyl = sentSyl.items()
        WperS = WperS.items()
        fAll = fAll.items()
        fM = fM.items()
        PS = PS.items()

        ##generate a .mat file for further analysis in matlab
        #if b == 0 and p == 0:
        obj_arr = np.array([urlDat,WperS, sentSyl, fM, PS, fAll], dtype=object)
        #else:
        obj_arr_add = np.array([urlDat,WperS, sentSyl, fM, PS, fAll], dtype=object)
        obj_arr = np.vstack( [obj_arr, obj_arr_add] )
        sio.savemat('textData_' + str(searchList[s]) + '.mat', {'obj_arr':obj_arr})

        return obj_arr
    returned_object = list(map(map_search,flattened))

    #returned_object = list(dview.map_sync(map_search,flattened))
    #after the full code runs export to a .mat file to a designed location
    os.chdir(FileLocation)

    #save
    #for obj_arr in
