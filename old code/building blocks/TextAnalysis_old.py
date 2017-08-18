#call in necessary packages that code requires to operate and define additional vars
import numpy
import numpy as np
import scipy.io as sio
import math
import re

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

#http://textminingonline.com/dive-into-nltk-part-i-getting-started-with-nltk
#http://www.nltk.org/book/ch01.html
#https://blogs.princeton.edu/etc/files/2014/03/Text-Analysis-with-NLTK-Cheatsheet.pdf
########################################################################
########################################################################
#set loop variables for larger analysis
os.chdir('/Users/PMcG/Dropbox (ASU)/AAB_files/Pat-files/WCP/code/testFiles/')

web = 1 #number of search websites being implemented
num = 1 #number of URLs per search website

########################################################################
##load file to analyze
fileHandle = open ( 'AABtest1.txt', 'rU' )

#read text file
url_text = fileHandle.read()
fileHandle.close()

########################################################################
##remove characters that causes nltk to become unable to see certain words
url_text = url_text.replace("-", " ") 

#locate numbers that nltk cannot see to analyze
textNum = re.findall(r'\d', url_text)

for x in range(0,len(textNum)) :
    url_text.find(textNum[x])

#print url_text

########################################################################
##Splitting text into words.
words = word_tokenize(url_text)
words = [w.lower() for w in words]

len(words) #count for all words and punctuation
print words

words_np = [word.lower() for word in words if word.isalpha()]

numWords = len(words_np)#count without punctutation
  
########################################################################
##frequency distribtuion of text
#fdist = FreqDist(words) #frequency distribution of all words in the text (including punctuation
fdist = FreqDist(w.lower() for w in words if w.isalpha()) #frequency distribution of words only

frexTop = fdist.max() #show most frequently used word
frexTerm = fdist['the'] #show frequency of some word

frexMost = fdist.most_common(10) #show n number of most common words

fM = {}
for x in range(0,len(frexMost)) :
    fM[x,1], fM[x,2] = [y.strip('}()",{:') for y in (str(frexMost[x])).split(',')]
    
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

print SA

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
        #print("The word contains", syllables, "syllable(s)")

print WperS
    
########################################################################
##convert all dict variables to list for multidimensional conversion to matlab cell array
sentSyl = sentSyl.items()
WperS = WperS.items()
fM = fM.items()
PS = PS.items()
SA = SA.items()

##save to .mat file for further analysis
obj_arr = np.array([numWords, numSents, WperS, sentSyl, frexTop, fM, frexTerm, PS, SA], dtype=object)
sio.savemat('DataOutput.mat', {'obj_arr':obj_arr})
