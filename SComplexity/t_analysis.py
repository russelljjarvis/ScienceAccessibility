# Scientific readability project
# authors ...,
# Russell Jarvis
# https://github.com/russelljjarvis/
# rjjarvis@asu.edu
# Patrick McGurrin
# patrick.mcgurrin@gmail.com


#general python imports
import os
#import dask
import matplotlib # Its not that this file is responsible for doing plotting, but it calls many modules that are, such that it needs to pre-empt
# setting of an appropriate backend not an X11 one.
matplotlib.use('Agg')
import sys
import numpy
import copy
import math
import re
import time
from tabulate import tabulate
from textblob import TextBlob
import pickle


import base64
import pandas as pd
import pickle
import os
import numpy as np

#text analysis imports

from nltk.tag.perceptron import PerceptronTagger
tagger = PerceptronTagger(load=False)

from nltk import word_tokenize,sent_tokenize
from nltk import sent_tokenize, word_tokenize, pos_tag
from nltk.probability import FreqDist
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.corpus import cmudict
from nltk.sentiment import SentimentAnalyzer

from textstat.textstat import textstat

from nltk.corpus import stopwords


from SComplexity.utils import black_string, english_check, comp_ratio, clue_words, clue_links, publication_check

DEBUG = False
#from numba import jit

# word limit smaller than 1000 gets product/merchandise sites.
#@jit
def text_proc(corpus, urlDat = {}, WORD_LIM = 100):
    #if type(corpus) is type((0,0)):
    #    pub = corpus[0]
    #    corpus = corpus[1]
    #    urlDat['pub'] = pub
    #print(type(corpus),corpus)
    #r emove unreadable characters
    if type(corpus) is str:
        corpus = corpus.replace("-", " ") #remove characters that nltk can't read
        textNum = re.findall(r'\d', corpus) #locate numbers that nltk cannot see to analyze
        tokens = word_tokenize(corpus)

        stop_words = stopwords.words('english')
        #We create a list comprehension which only returns a list of words #that are NOT IN stop_words and NOT IN punctuations.
    
        tokens = [ word for word in tokens if not word in stop_words]
        tokens = [w.lower() for w in tokens] #make everything lower case

        # the kind of change that might break everything
        urlDat['wcount'] = textstat.lexicon_count(str(tokens))
        word_lim = bool(urlDat['wcount']  > WORD_LIM)

        # Word limits can be used to filter out product merchandise websites, which otherwise dominate scraped results.
        # Search engine business model is revenue orientated, so most links will be for merchandise.

        urlDat['publication'] = publication_check(str(tokens))
        urlDat['english'] = english_check(str(tokens))
        urlDat['clue_words'] = clue_words(str(tokens))
        urlDat['clue_links'] = clue_links(urlDat['link'])

        # The post modern essay generator is so obfuscated, that ENGLISH classification fails, and this criteria needs to be relaxed.
        not_empty = bool(len(tokens) != 0)
        print(not_empty,urlDat['english'],word_lim)
        if urlDat['english']==False:
            pass
        #print(str(tokens))

        if not_empty and word_lim: #  and server_error:
            
            tokens = [ w.lower() for w in tokens if w.isalpha() ]
            #fdist = FreqDist(tokens) #frequency distribution of words only
            # The larger the ratio of unqiue words to repeated words the more colourful the language.
            lexicon = textstat.lexicon_count(corpus, True)
            urlDat['uniqueness'] = len(set(tokens))/float(len(tokens))
            # It's harder to have a good unique ratio in a long document, as 'and', 'the' and 'a', will dominate.
            # big deltas mean redudancy/sparse information/information/density


            urlDat['info_density'] =  comp_ratio(corpus)

            #Sentiment and Subjectivity analysis
            testimonial = TextBlob(corpus)
            urlDat['sp'] = testimonial.sentiment.polarity
            urlDat['ss'] = testimonial.sentiment.subjectivity
            urlDat['sp_norm'] = np.abs(testimonial.sentiment.polarity)
            urlDat['ss_norm'] = np.abs(testimonial.sentiment.subjectivity)
            urlDat['gf'] = textstat.gunning_fog(corpus)

            # explanation of metrics
            # https://github.com/shivam5992/textstat

            standard_  = textstat.text_standard(corpus)
            try:
                urlDat['standard']  = float(standard_[0:2])
            except:
                urlDat['standard']  = float(standard_[0:1])

            # special sauce
            # Good writing should be readable, objective, concise.
            # The writing should be articulate/expressive enough not to have to repeat phrases,
            # thereby seeming redundant. Articulate expressive writing then employs
            # many unique words, and does not yield high compression savings.
            # Good writing should not be obfucstated either. The reading level is a check for obfucstation.
            # The resulting metric is a balance of concision, low obfucstation, expression.
            penalty = 1.0/urlDat['standard']  + abs(urlDat['sp']) + abs(urlDat['ss']) +1.0/urlDat['uniqueness']# +float(scaled_density)
            urlDat['penalty'] = penalty
        return urlDat


def process_dics(urlDats):
    dfs = []
    for urlDat in urlDats:
        # pandas Data frames are best data container for maths/stats, but steep learning curve.
        # Other exclusion criteria. Exclude reading levels above grade 100,
        # as this is most likely a problem with the metric algorithm, and or rubbish data in.
        # TODO: speed everything up, by performing exclusion criteri above not here.
        if len(dfs) == 0:
            dfs = pd.DataFrame(pd.Series(urlDat)).T
        dfs = pd.concat([ dfs, pd.DataFrame(pd.Series(urlDat)).T ])
    return dfs
