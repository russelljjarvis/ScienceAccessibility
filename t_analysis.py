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

#text analysis imports
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
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

from textstat.textstat import textstat

import os
os.system('pip install natsort')
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

########################################################################
########################################################################
########################################################################
#start all the analysis code

#for s, value in enumerate(searchList):
#def iter_over(searchListElement):
date_created = []

# Terms need to be to evaluated per search engine.
# Terms have their own file name, but search engine results are collated togethor per term.


def iter_over(b):
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
    # grab all the file names ending with pickle suffix.
    list_of_files = natsorted(glob.glob(str(textName)+r'*.p'))
    # select only a subset of them.
    list_of_files =  natsorted(list_of_files[0:numURLs-1])

    #def iter_over(searchListElement):
    #s, value = searchListElement
    sl = [ (i, val) for i, val in enumerate(searchList) ]
    for s, value in sl:
        if not os.path.exists(str(fileLocation) + '/' + str(value) +'/'):
            os.makedirs(str(fileLocation) + '/' + str(value) +'/')
        os.chdir(fileLocation +str('/') + str(value) +'/')

        print (" ")
        print ("###############################################")
        print (" ")
        print ("Term {0} of {1} : {2}".format(s+1 , str(len(searchList)), value))
        print (" ")
        print ("###############################################")
    #web = [ "google_","gScholar_","bing_","yahoo_" ]
    #web = [0:nweb]

    #for b, _ in enumerate(web):
        #search engine selection




        for p,fileName in enumerate(list_of_files):
            print ("-------------------------------------------")
            print ("Analyzing Search Engine " + str(b+1) + " of " + str(nweb) + ": Link " + str(p)); print ("");
            #open and read text q

            import pickle

            fileHandle = open(fileName, 'rb');
            file_contents = pickle.load(fileHandle)

            #fileHandle = open(fileName, 'r');
            #with open(fileName, 'r') as myfile:
            #    data = myfile.read().replace('\n', '')
            #file_contents =str(fileHandle.read_lines())

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
            #sentences
            sents = sent_tokenize(url_text) #split all of text in to sentences
            sents = [w.lower() for w in sents] #lowercase all

            urlDat[2,1] = len(sents) #determine number of sentences

            ########################################################################
            ##frequency distribtuion of text
            fdist = FreqDist(w.lower() for w in URLtext if w.isalpha()) #frequency distribution of words only

            # Bug fix
            # cast dict to list
            fd_temp = list(fdist.items())

            urlDat[3,1] = fdist[searchList[s].lower()] #frequency of search term

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

            urlDat[4,1] = testimonial.sentiment.polarity
            urlDat[5,1] = testimonial.sentiment.subjectivity

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
            #
            ########################################################################
            ## Complexity Analysis
            try:
                assert len(url_text) != 0
                #assert type(url_text) is not type(None)
                urlDat[6,1]  = textstat.flesch_kincaid_grade(str(url_text))
                urlDat[7,1] = textstat.flesch_reading_ease(str(url_text))
                urlDat[8,1]  = textstat.smog_index(str(url_text))
                urlDat[9,1]  = textstat.coleman_liau_index(str(url_text))
                urlDat[10,1]  = textstat.automated_readability_index(str(url_text))
                urlDat[11,1] = textstat.gunning_fog(str(url_text))

                urlDat[12,1]  = textstat.dale_chall_readability_score(str(url_text))
                urlDat[13,1]  = textstat.difficult_words(str(url_text))
                urlDat[14,1]  = textstat.linsear_write_formula(str(url_text))

                ########################################################################
                ########################################################################
                ########################################################################
                ########################################################################
                #clean-up and prep for saving for subsequent analysis and plotting

                ##convert all dict variables to list for multidimensional conversion to matlab cell array
                urlDat = list(urlDat.items())
                sentSyl = list(sentSyl.items())
                WperS = list(WperS.items())
                fAll = list(fAll.items())
                fM = list(fM.items())

                ##generate a .mat file for further analysis in matlab
                obj_arr_add = np.array([urlDat, WperS, sentSyl, fM, fAll], dtype=np.object)
                print('dimensions change of object array: ',np.shape(obj_arr),np.shape(urlDat))
                assert len(obj_arr_add[-1])!= 0
                assert len(obj_arr_add[-2])!= 0
                assert len(obj_arr_add[-3])!= 0
                assert type(obj_arr) is not type(None)
                assert np.shape(obj_arr) != old
                old = np.shape(obj_arr)
                # File path is equivalent to Term.mat
                handle = str('../Data/') + str(searchList[s]) + '.mat'
                #import scipy
                scipy = None
                import scipy
                scipy.io.savemat(handle, {'obj_arr':obj_arr})
                print(scipy.io.loadmat(handle))
                handle = None
            except:
                print(len(url_text), 'zero size link text badness!')
                pass
            return obj_arr_add

            import dask.bag as db

            web_iter = [0,1,2,3]
            b = db.from_sequence(web_iter)

            obj_arr_add = list(db.map(iter_over,b).compute())
            obj_arr = obj_arr_add[0]
            #obj_arr = np.array(0)
            for oaa in obj_arr_add[1:-1]:
                obj_arr = np.vstack( [obj_arr, oaa])

            scipy = None
            import scipy
            scipy.io.savemat(handle, {'obj_arr':obj_arr})
            print(scipy.io.loadmat(handle))
            handle = str('../Data/') + str(searchList[s]) + '.mat'

handle = None

os.chdir('../Data/')

handle = 'file_name_versus_date.mat'
scipy.io.savemat(handle, {'infoDated':date_created})

os.system('octave read_mat.m')
os.system('octave read_matSoft.m')
exit
