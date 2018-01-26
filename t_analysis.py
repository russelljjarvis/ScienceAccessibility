import os
import dask
import matplotlib # Its not that this file is responsible for doing plotting, but it calls many modules that are, such that it needs to pre-empt
# setting of an appropriate backend.
matplotlib.use('Agg')
import sys
import numpy
import numpy as np
import scipy.io as sio
import scipy
import math
import re
from bs4 import BeautifulSoup
import matplotlib
import json
import requests
import time
from tabulate import tabulate
from textblob import TextBlob
import glob

#NLTK
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
from nltk import word_tokenize,sent_tokenize
from nltk import sent_tokenize, word_tokenize, pos_tag
from nltk.probability import FreqDist
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.corpus import cmudict
from nltk.sentiment import SentimentAnalyzer
from nltk import compat
#from nltk.compat import Counter
from nltk.draw import dispersion_plot

#functions to perform text analysis
from textstat.textstat import textstat

current_dir = os.getcwd()
########################################################################
########################################################################
########################################################################

# Set user parameters based on type of analysis
searchList = ['GMO','Genetically_Modified_Organism','Transgenic','Vaccine']
nweb = 2 #number of search websites being implemented (google, google scholar, bing, yahoo)
numURLs = 10 #number of URLs per search website  (number determined by 1.scrape code)

#save the parameters for analysis purposes
save_dict = { 'searchList':searchList, 'nweb':nweb, 'numURLs':numURLs}
handle = 'Data/analysis.mat'
scipy.io.savemat(handle, mdict=save_dict, oned_as='row')


#set filePath below to specify where the text Data is located on your machine
fileLocation = os.getcwd()

if not os.path.exists(fileLocation):
    os.makedirs(fileLocation)

########################################################################
########################################################################
########################################################################

#for s, value in enumerate(searchList):
#def iter_over(searchListElement):
sl = [ (i, val) for i, val in enumerate(searchList) ]
for s, value in sl:
    #s, value = searchListElement

    if not os.path.exists(str(fileLocation) + '/' + str(value) +'/'):
        os.makedirs(str(fileLocation) + '/' + str(value) +'/')
    os.chdir(fileLocation +str('/') + str(value) +'/')

    ##start analysis code
    print (" ")
    print ("###############################################")
    print (" ")
    print ("Term {0} of {1} : {2}".format(s+1 , str(len(searchList)), value))
    print (" ")
    print ("###############################################")
    #web = [ "google_","gScholar_","bing_","yahoo_" ]
    #web = [0:nweb]
    for b in range(0,nweb):
    #for b, _ in enumerate(web):
        #search engine selection
        if b == 0:
            textName = "google_"
            print ("Google")
        elif b == 1:
            textName = "gScholar_"
            print ("Google Scholar")
        elif b == 2:
            textName = "bing_"
            print ("Bing")
        elif b == 3:
            textName = "yahoo_"
            print ("Yahoo")

        #import pdb; pdb.set_trace()
        #list_of_files = glob.glob(r'textName*.p')
        list_of_files = sorted(glob.glob(str(textName)+r'*.p'))
        #if len(list_of_files) >= 50:
        list_of_files =  sorted(list_of_files[0:numURLs-1])

        for p,fileName in enumerate(list_of_files):
            print ("-------------------------------------------")
            print ("Analyzing Search Engine " + str(b+1) + " of " + str(nweb) + ": Link " + str(p)); print ("");
            #open and read text q

            #fileName = l#'{0}{1}.p'.format(textName,p+1)
            print(fileName)
            print(os.getcwd(), 'pwd')
            import pickle

            fileHandle = open(fileName, 'rb');
            file_contents = pickle.load(fileHandle)
            if len(file_contents) == 2:
                date_created = file_contents[0]
                url_text = file_contents[1]
            else:

                url_text = file_contents

            #initialize dataArray Dictionary
            urlDat = {}
            
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

            urlDat[1,1] = textstat.lexicon_count(str(url_text))
            #import pdb; pdb.set_trace()
            #sentences
            sents = sent_tokenize(url_text) #split all of text in to sentences
            sents = [w.lower() for w in sents] #lowercase all

            urlDat[2,1]   = len(sents) #determine number of sentences

            ########################################################################
            ##frequency distribtuion of text
            fdist = FreqDist(w.lower() for w in URLtext if w.isalpha()) #frequency distribution of words only


            # Bug fix
            # cast dict to list
            fd_temp = list(fdist.items())


            urlDat[3,1] = fdist[searchList[s].lower()] #frequency of search term
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
            # for n,sent in enumerate(sents):
            # future use
            for n, _ in enumerate(sents):

                #setup sent variable to analyze each sentence individually
                sent = sents[n] #select sentence n in total text
                sent = word_tokenize(sent) #tokenize sentence n in to words
                sent = [w.lower() for w in sent if w.isalpha()] #remove any non-text

                WperS[n] = len(sent) #number of words per sentence

                #syllable analysis

            for x, _ in enumerate(sent):

                word = sent[x]

                # Count the syllables in the word.
                syllables = textstat.syllable_count(str(word))
                sentSyl[n,x] = syllables
            #
            ########################################################################
            ## Complexity Analysis
            #try:
            assert len(url_text) != 0
            assert type(url_text) is not type(None)
            urlDat[6,1]  = textstat.flesch_kincaid_grade(str(url_text))
            urlDat[7,1] = textstat.flesch_reading_ease(str(url_text))
            urlDat[8,1]  = textstat.smog_index(str(url_text))
            urlDat[9,1]  = textstat.coleman_liau_index(str(url_text))
            urlDat[10,1]  = textstat.automated_readability_index(str(url_text))
            urlDat[11,1] = textstat.gunning_fog(str(url_text))

            urlDat[12,1]  = textstat.dale_chall_readability_score(str(url_text))
            urlDat[13,1]  = textstat.difficult_words(str(url_text))
            urlDat[14,1]  = textstat.linsear_write_formula(str(url_text))
            urlDat[15,1]  = textstat.text_standard(str(url_text))
            #import pdb
            #pdb.set_trace()

            ########################################################################
            ##Sentiment and Subjectivity analysis
            testimonial = TextBlob(url_text)
            testimonial.sentiment
            ##defining part of speech for each word
            from nltk.tag.perceptron import PerceptronTagger
            tagger = PerceptronTagger(load=False)

            urlDat[4,1] = testimonial.sentiment.polarity
            urlDat[5,1] = testimonial.sentiment.subjectivity

            #time.sleep(1); #print (""); print (""); print ("");
            ########################################################################
            ##convert all dict variables to list for multidimensional conversion to matlab cell array
            urlDat = list(urlDat.items())
            sentSyl = list(sentSyl.items())
            WperS = list(WperS.items())
            fAll = list(fAll.items())
            fM = list(fM.items())

            ##generate a .mat file for further analysis in matlab
            if b == 0 and p == 0:
                obj_arr = np.array([urlDat, WperS, sentSyl, fM, fAll], dtype=np.object)
                print('dimensions change of object array: ',np.shape(obj_arr),np.shape(urlDat))
                old = np.shape(obj_arr)

                #import pdb; pdb.set_trace()
            else:
                obj_arr_add = np.array([urlDat ,WperS, sentSyl, fM, fAll], dtype=np.object)
                assert type(obj_arr) is not type(None)


                print('dimensions change of object array: ',np.shape(obj_arr),np.shape(urlDat))
                obj_arr = np.vstack( [obj_arr, obj_arr_add])

                assert np.shape(obj_arr) != old
                old = np.shape(obj_arr)

            handle = str('../Data/') + str(searchList[s]) + str('_term_')+ str(s)+ '.mat'
            import scipy
            scipy.io.savemat(handle, {'obj_arr':obj_arr} , oned_as='row')
