#call in necessary packages that code requires to operate and define additional vars
import numpy
import numpy as np
import scipy.io as sio
import math
import re
from bs4 import BeautifulSoup
import matplotlib
import os
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
from nltk.compat import Counter
from nltk.draw import dispersion_plot

########################################################################
########################################################################
term = 'GenModOrg'
web = 3 #number of search websites being implemented
num = 26 #number of URLs per search website + 1

#set loop variables for larger analysis
#os.chdir('D:/Dropbox (ASU)/RESEARCH/Pat_Projects/textAnalyze/'+ str(term) +'/')
os.chdir('/Users/PMcG/Dropbox (ASU)/AAB_files/Pat-files/WCP/code/Data Files/'+ str(term) +'/')

########################################################################
##load file to analyze

for b in range(0,web) :

    if b == 0:
        textName = "google_"
    elif b == 1:
        textName = "yahoo_"
    elif b == 2:
        textName = "bing_"  
    
    for p in range(1,num) :
        print b,p
        
        fileName = textName + str(p) + ".txt"        
        fileHandle = open(fileName, 'rU');

        #read text file
        url_text = fileHandle.read()
        fileHandle.close()

        url_text = url_text.decode('ascii','ignore')

        ########################################################################
        ##remove characters that causes nltk to become unable to see certain words
        url_text = url_text.replace("-", " ") 

        #locate numbers that nltk cannot see to analyze
        textNum = re.findall(r'\d', url_text)

        for x in range(0,len(textNum)) :
            url_text.find(textNum[x])

        #print url_text
        #numChar = len(url_text)
        ########################################################################
        ##Splitting text into words.
        words = word_tokenize(url_text)
 
