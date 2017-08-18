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
term = 'Transgenic'
web = 3 #number of search websites being implemented
num = 26 #number of URLs per search website + 1

#set loop variables for larger analysis
os.chdir('D:/Dropbox (ASU)/RESEARCH/Pat_Projects/textAnalyze/'+ str(term) +'/')
#os.chdir('/Users/PMcG/Dropbox (ASU)/AAB_files/Pat-files/WCP/code/Data Files/'+ str(term) +'/')

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
        words = [w.lower() for w in words]

        len(words) #count for all words and punctuation
    
        words_np = [word.lower() for word in words if word.isalpha()]
        numWords = len(words_np)#count without punctutation
          
        ########################################################################
        ##frequency distribtuion of text
        #fdist = FreqDist(words) #frequency distribution of all words in the text (including punctuation)
        ##
        fdist = FreqDist(w.lower() for w in words if w.isalpha()) #frequency distribution of words only

        fd_temp = fdist.items()
        fd = {}

        for x in range(0,len(fd_temp)):
            fd[x,1], fd[x,2] = [y.strip('}()",{:') for y in (str(fd_temp[x])).split(',')]
        ##
            
        frexTop = fdist.max() #show most frequently used word
        frexTerm = fdist[str(term)] #show frequency of some word

        ##
        frexMost = fdist.most_common(10) #show n number of most common words

        fM = {}
        for x in range(0,len(frexMost)) :
            fM[x,1], fM[x,2] = [y.strip('}()",{:') for y in (str(frexMost[x])).split(',')]
        ##
            
        #identify long words based on word length of n characters
        #long_words = [w for w in words if len(w) > 8] #last number is character length
        #sorted(long_words)

        #raster plot of term use
        #wordtext = nltk.Text(words)
        #wordtext.dispersion_plot(["gmo","the"])

        ########################################################################
        ##defining the part of speech
        wordsPOS = pos_tag(words_np) 
        #print wordsPOS

        PS = {}
        for x in range(0,len(wordsPOS)) :
            PS[x,1], PS[x,2] = [y.strip('}()",{:') for y in (str(wordsPOS[x])).split(',')]

        ########################################################################
        ##Sentiment analysis using hierarchical classification
        #http://text-processing.com/demo/
        r = requests.post('http://text-processing.com/api/sentiment/', data = {'text':url_text})
        sentiment = [y.strip('}()",{:') for y in (str(r.text)).split()]

        SA = {}
        #define polarity labels and corresponding values
        SA[1,1] = sentiment[1]
        SA[1,2] = sentiment[2]
        SA[2,1] = sentiment[3]
        SA[2,2] = sentiment[4]
        SA[3,1] = sentiment[5]
        SA[3,2] = sentiment[6]

        #print SA

        ########################################################################
        ##Splitting sentences from the body of text.
        sents = sent_tokenize(url_text)
        sents = [w.lower() for w in sents]

        #determine number of sentences
        numSents = len(sents) 
        print sents

        ########################################################################       
        ##determine number of sentences and syllables for all words in each sentece
        sentSyl = {}
        WperS = {}
        numChar = {}

        for n in range (0,len(sents)):

            #setup sent variable to analyze each sentence individually
            sent = sents[n]
            sent = word_tokenize(sent)
            sent = [word.lower() for word in sent if word.isalpha()]

            #number of words per sentence
            WperS[n] = len(sent)

            #syllable analysis    
            for x in range (0,len(sent)):
                
                word = sent[x]
                #print(word)
                
                # Count the syllables in the word.
                syllables = 0
                for i in range(len(word)) :

                   # If the first letter in the word is a vowel then it is a syllable.
                   if i == 0 and word[i] in "aeiouy" :
                      syllables = syllables + 1

                   # Else if the previous letter is not a vowel.
                   elif word[i - 1] not in "aeiouy" :

                      # If it is no the last letter in the word and it is a vowel.
                      if i < len(word) - 1 and word[i] in "aeiouy" :
                         syllables = syllables + 1

                      # Else if it is the last letter and it is a vowel that is not e.
                      elif i == len(word) - 1 and word[i] in "aiouy" :
                         syllables = syllables + 1

                # Adjust syllables from 0 to 1.
                if len(word) > 0 and syllables == 0 :
                   syllables == 0
                   syllables = 1

                # Display the result.
                sentSyl[n,x] = syllables
                numChar[n,x] = len(word)
                #print("The word contains", syllables, "syllable(s)")

        #print WperS

        ########################################################################
        ##run text through Read-Able
        url = "http://www.webpagefx.com/tools/read-able/check.php"
        payload = {'directInput':url_text, 'tab': 'Test by Direct Link'}
        r = requests.post(url, data=payload)

        soup = BeautifulSoup(r.content, 'html.parser')

        #strip HTML scripting and style
        for script in soup(["script", "style"]):
                script.extract()    # rip it out
                
        text = soup.get_text()
        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)

        text =  text.split('\n')
        text = text[9:38]

        temp = text[0].rsplit('.'); temp = temp[0]

        Read = {}
        Read[1,1] = "grade level"; Read[1,2] = [re.findall(r'\d', temp)[:2]]
        Read[2,1] = text[3]; Read[2,2] = text[4]
        Read[3,1] = text[5]; Read[3,2] = text[6]
        Read[4,1] = text[7]; Read[4,2] = text[8]
        Read[5,1] = text[9]; Read[5,2] = text[10]
        Read[6,1] = text[11]; Read[6,2] = text[12]
        Read[7,1] = text[13]; Read[7,2] = text[14]
        Read[8,1] = text[16]; Read[8,2] = text[17]
        Read[9,1] = text[18]; Read[9,2] = text[19]
        Read[10,1] = text[20]; Read[10,2] = text[21]
        Read[11,1] = text[22]; Read[11,2] = text[23]
        Read[12,1] = "average words for sentence"; Read[12,2] = text[26]
        Read[13,1] = text[27]; Read[13,2] = text[28]
        
        ########################################################################
        ##convert all dict variables to list for multidimensional conversion to matlab cell array
        sentSyl = sentSyl.items()
        WperS = WperS.items()
        fAll = fd.items()
        fM = fM.items()
        PS = PS.items()
        SA = SA.items()
        Read = Read.items()
        numChar= numChar.items()
        ##save to .mat file for further analysis - where each row is one url analysis
        if b == 0 and p == 1:
            obj_arr = np.array([numWords, numSents, WperS, sentSyl, frexTop, fM, frexTerm, PS, SA, fAll, Read, numChar], dtype=object)
        else:
            obj_arr_add = np.array([numWords, numSents, WperS, sentSyl, frexTop, fM, frexTerm, PS, SA, fAll, Read, numChar], dtype=object)
            obj_arr = np.vstack( [obj_arr, obj_arr_add] )

#after the full code runs export to a .mat file so I know what the heck I'm doing for analysis
sio.savemat('textAnalysis_' + str(term) + '.mat', {'obj_arr':obj_arr})
