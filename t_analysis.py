#set parameters- THESE ARE ALL USER DEFINED
#searchList = ['GMO']
import os
#os.system('ipcluster start -n 8 --profile=default & sleep 15 ;  ')
import dask
searchList = ['GMO','Genetically Modified Organism']
#import os
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
from nltk import word_tokenize,sent_tokenize
import matplotlib # Its not that this file is responsible for doing plotting, but it calls many modules that are, such that it needs to pre-empt
# setting of an appropriate backend.
matplotlib.use('Agg')
import sys
import os

current_dir = os.getcwd()
web = 4 #number of search websites being implemented (google, google scholar, bing, yahoo)
numURLs = 50 #number of URLs per search website  (number determined by 1.scrape code)

#set filePath below to specify where the text Data is located on your machine
fileLocation = os.getcwd()

if not os.path.exists(fileLocation):
    os.makedirs(fileLocation)

#import ipyparallel as ipp
#rc = ipp.Client(profile='default')
#from ipyparallel import depend, require, dependent
#dview = rc[:]


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

import glob

########################################################################

searchList = ['GMO','Genetically_Modified_Organism','Transgenic','Vaccine']

#for s, value in enumerate(searchList):
def iter_over(searchListElement):
    s, value = searchListElement

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
    web = [ "google_","gScholar_","bing_","yahoo_" ]
    #web = [ "bing_"]
    # Note for long term code maintaince it will be better to flatten the
    # Iterator, as below by building the iterator first in a list comprehension
    # The idea is multilayered nested clauses leads to more bugs.
    # cflattened = [ (p,b,textName) for b, textName in enumerate(web) for p in range(0,numURLs) ]
    for b, _ in enumerate(web):
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
        if len(list_of_files) >= 50:
            list_of_files =  sorted(list_of_files[0:49])

        for p,fileName in enumerate(list_of_files):
            print ("-------------------------------------------")
            print ("Analyzing Search Engine " + str(b+1) + " of " + str(web) + ": Link " + str(p)); print ("");
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
            #print(url_text)
                #fileHandle.read()
            #fileHandle.close()
            #url_text = url_text.decode('ascii','ignore')

            #initialize dataArray Dictionary
            urlDat = {}
            '''
            urlDat[1,1] = 0#"Number of Words"
            urlDat[2,1] = 1#"Number of Sentences"
            urlDat[3,1] = 2#"Frequency of Search Term"
            urlDat[4,1] = 3#"Sentiment Analysis"
            urlDat[5,1] = 4#"Subjectivity Analysis"
            urlDat[6,1] = 5#"Grade level"
            urlDat[7,1] = 6#"Flesch Reading Ease"
            urlDat[8,1] = 7#"SMOG Index"
            urlDat[9,1] = 8#"Coleman Liau"
            urlDat[10,1] = 9#"Automated Readability Index"
            urlDat[11,1] = 10#"Gunning Fog"
            urlDat[12,1] = 11#"Dale Chall Readability Score"
            urlDat[13,1] = 12#"Difficult Words"
            urlDat[14,1] = 13#"Linsear Write Formula"
            urlDat[15,1] = 14#"Text Standard"


            urlDat[1,1] = "Number of Words".encode('ascii','ignore')
            urlDat[2,1] = "Number of Sentences".encode('ascii','ignore')
            urlDat[3,1] = "Frequency of Search Term".encode('ascii','ignore')
            urlDat[4,1] = "Sentiment Analysis".encode('ascii','ignore')
            urlDat[5,1] = "Subjectivity Analysis".encode('ascii','ignore')
            urlDat[6,1] = "Grade level".encode('ascii','ignore')
            urlDat[7,1] = "Flesch Reading Ease".encode('ascii','ignore')
            urlDat[8,1] = "SMOG Index".encode('ascii','ignore')
            urlDat[9,1] = "Coleman Liau".encode('ascii','ignore')
            urlDat[10,1] = "Automated Readability Index".encode('ascii','ignore')
            urlDat[11,1] = "Gunning Fog".encode('ascii','ignore')
            urlDat[12,1] = "Dale Chall Readability Score".encode('ascii','ignore')
            urlDat[13,1] = "Difficult Words".encode('ascii','ignore')
            urlDat[14,1] = "Linsear Write Formula".encode('ascii','ignore')
            urlDat[15,1] = "Text Standard".encode('ascii','ignore')

            urlDat[1,1] = "Number of Words".encode("utf-16")
            urlDat[2,1] = "Number of Sentences".encode("utf-16")
            urlDat[3,1] = "Frequency of Search Term".encode("utf-16")
            urlDat[4,1] = "Sentiment Analysis".encode("utf-16")
            urlDat[5,1] = "Subjectivity Analysis".encode("utf-16")
            urlDat[6,1] = "Grade level".encode("utf-16")
            urlDat[7,1] = "Flesch Reading Ease".encode("utf-16")
            urlDat[8,1] = "SMOG Index".encode("utf-16")
            urlDat[9,1] = "Coleman Liau".encode("utf-16")
            urlDat[10,1] = "Automated Readability Index".encode("utf-16")
            urlDat[11,1] = "Gunning Fog".encode("utf-16")
            urlDat[12,1] = "Dale Chall Readability Score".encode("utf-16")
            urlDat[13,1] = "Difficult Words".encode("utf-16")
            urlDat[14,1] = "Linsear Write Formula".encode("utf-16")
            urlDat[15,1] = "Text Standard".encode("utf-16")
            '''
            urlDat[1,1] = str("Number of Words")
            urlDat[2,1] = str("Number of Sentences")#.encode("utf-16")
            urlDat[3,1] = str("Frequency of Search Term")#.encode("utf-16")
            urlDat[4,1] = str("Sentiment Analysis")#.encode("utf-16")
            urlDat[5,1] = str("Subjectivity Analysis")#.encode("utf-16")
            urlDat[6,1] = str("Grade level")#.encode("utf-16")
            urlDat[7,1] = str("Flesch Reading Ease")#.encode("utf-16")
            urlDat[8,1] = str("SMOG Index")#.encode("utf-16")
            urlDat[9,1] = str("Coleman Liau")#.encode("utf-16")
            urlDat[10,1] = str("Automated Readability Index")#.encode("utf-16")
            urlDat[11,1] = str("Gunning Fog")#.encode("utf-16")
            urlDat[12,1] = str("Dale Chall Readability Score")#.encode("utf-16")
            urlDat[13,1] = str("Difficult Words")#.encode("utf-16")
            urlDat[14,1] = str("Linsear Write Formula")#.encode("utf-16")
            urlDat[15,1] = str("Text Standard")#.encode("utf-16")

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
            #import pdb; pdb.set_trace()
            #sentences
            sents = sent_tokenize(url_text) #split all of text in to sentences
            sents = [w.lower() for w in sents] #lowercase all

            urlDat[2,2]   = len(sents) #determine number of sentences

            ########################################################################
            ##frequency distribtuion of text
            fdist = FreqDist(w.lower() for w in URLtext if w.isalpha()) #frequency distribution of words only


            # Bug fix
            # cast dict to list
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
            # for n,sent in enumerate(sents):
            # future use
            for n, _ in enumerate(sents):

                #setup sent variable to analyze each sentence individually
                sent = sents[n] #select sentence n in total text
                sent = word_tokenize(sent) #tokenize sentence n in to words
                sent = [w.lower() for w in sent if w.isalpha()] #remove any non-text

                WperS[n] = len(sent) #number of words per sentence

                #syllable analysis
                # aetna student health
                # 8774804161
            for x, _ in enumerate(sent):

                word = sent[x]

                # Count the syllables in the word.
                syllables = textstat.syllable_count(str(word))
                sentSyl[n,x] = syllables
            #
            ########################################################################
            ## Complexity Analysis
            try:
                assert len(url_text) != 0
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
                wordsPOS = pos_tag([w.lower() for w in URLtext if w.isalpha()])

                PS = {}
                for x in range(0,len(wordsPOS)) :
                    PS[x,1], PS[x,2] = [y.strip('}()",{:') for y in (str(wordsPOS[x])).split(',')]

                ########################################################################
                ##Sentiment and Subjectivity analysis
                testimonial = TextBlob(url_text)
                testimonial.sentiment
                ##defining part of speech for each word
                from nltk.tag.perceptron import PerceptronTagger
                tagger = PerceptronTagger(load=False)

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
                urlDat = list(urlDat.items())
                sentSyl = list(sentSyl.items())
                WperS = list(WperS.items())
                fAll = list(fAll.items())
                fM = list(fM.items())
                PS = list(PS.items())

                ##generate a .mat file for further analysis in matlab
                if b == 0 and p == 0:
                    obj_arr = np.array([urlDat,WperS, sentSyl, fM, PS, fAll], dtype=np.object)
                else:
                    obj_arr_add = np.array([urlDat,WperS, sentSyl, fM, PS, fAll], dtype=np.object)
                    obj_arr = np.vstack( [obj_arr, obj_arr_add] , dtype=np.object)
                my_dict = {'obj_arr':obj_arr}
                import scipy
                handle = searchList[s]  + '.mat'
                scipy.io.savemat(handle, mdict={ 'obj_arr' : my_dict}, oned_as='row')
                
            except:
                print('number of words is zero on that link, so analysis will fail')
            
            return obj_arr
            #h.create_dataset(name=str(p)+searchList[s], data=np.array(obj_arr))
            #save('test.mat','-v7')
            #f = h5py.File(handle,'wr')
            #data = f.get('data/variable1')
            #mat_contents = scipy.io.loadmat(handle)
            #print(mat_contents, 'matrix contents')


#searchList


#exit()
