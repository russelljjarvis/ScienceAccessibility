# Scientific readability project
# authors ...,
# Russell Jarvis
# https://github.com/russelljjarvis/
# rjjarvis@asu.edu
# Patrick McGurrin
# patrick.mcgurrin@gmail.com


##
# Probably 75% of the metrics computed here are not utilized, as the customers did not know what they wanted.
# The analysis tries to be everything for everyone, and this can and should change for the better.
##

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
from nltk import compat
#from bs4 import BeautifulSoup
#import json
from textstat.textstat import textstat

#from natsort import natsorted, ns

import pandas as pd
import pycld2 as cld2
import pickle
import os
import lzma

import base64
#import zlib


# params are defined in a seperate file, as they are prone to changing,
# yet, different programs draw on them, better to have to only change them in one
# place not three.

from utils_and_paramaters import search_params, engine_dict_list
SEARCHLIST, WEB, LINKSTOGET = search_params()
se, _ = engine_dict_list()

def lzma_compression_ratio(test_string):
    c = lzma.LZMACompressor()
    bytes_in = bytes(test_string,'utf-8')
    bytes_out = c.compress(bytes_in)
    return len(bytes_out)/len(bytes_in)


DEBUG = False


def text_proc(corpus,urlDat, WORD_LIM = 4000):
    #remove unreadable characters
    corpus = corpus.replace("-", " ") #remove characters that nltk can't read
    textNum = re.findall(r'\d', corpus) #locate numbers that nltk cannot see to analyze
    tokens = word_tokenize(corpus)
    tokens = [w.lower() for w in tokens] #make everything lower case

    urlDat['wcount'] = textstat.lexicon_count(str(tokens))
    word_lim = bool(urlDat['wcount']  > WORD_LIM)

    try:
        # It's not that we are cultural imperialists, but the people at textstat, and nltk may have been,
        # so we are also forced into this tacit agreement.
        # Japanese characters massively distort information theory estimates, as they are potentially very concise.
 
        _, _, details = cld2.detect(' '.join(corpus), bestEffort=True)
        detectedLangName, _ = details[0][:2]
        urlDat['english'] = bool(detectedLangName == 'ENGLISH')
    except:
        urlDat['english'] = True

    if len(tokens) != 0 and urlDat['english'] and word_lim:

        ##frequency distribtuion of text
        tokens = [ w.lower() for w in tokens if w.isalpha() ]
        fdist = FreqDist(tokens) #frequency distribution of words only
        urlDat['uniqueness'] = len(set(tokens))/float(len(tokens))
        compression_ratio = lzma_compression_ratio(corpus)
        # big deltas mean redudancy/sparse information/information/density

        # long file lengths lead to big deltas.
        urlDat['info_density'] = compression_ratio
        scaled_density = urlDat['info_density']/urlDat['wcount']
        urlDat['scaled_info_density'] = scaled_density
        #urlDat['info_density_explanation'] = 'the smaller the more redundancy exploited by compression'
        # cast dict to list
        fd_temp = list(fdist.items())

        #frequency of all words
        fAll = {}
        for x in range(0,len(fd_temp)):
            fAll[x,1], fAll[x,2] = [y.strip('}()",{:') for y in (str(fd_temp[x])).split(',')]
        #
        urlDat['frequencies'] = sorted([ (f[1],f[0]) for f in fd_temp ],reverse=True)
        number_of_words = sum([ f[0] for f in urlDat['frequencies'] ])

        probs = [float(c[0]) / number_of_words for c in urlDat['frequencies'] ]
        probs = [p for p in probs if p > 0.]
        ent = 0
        for p in probs:
            if p > 0.:
                ent -= p * math.log(p, 2)
        urlDat['eofh'] = ent

        #frequency of the most used n number of words
        frexMost = fdist.most_common(15) #show N most common words
        urlDat['frexMost'] = frexMost
        fM = {}
        for x in range(0,len(frexMost)) :
            fM[x,1], fM[x,2] = [y.strip('}()",{:') for y in (str(frexMost[x])).split(',')]
        if DEBUG == False:
            # These clutter readouts.
            urlDat['frexMost'] = None
            urlDat['frequencies'] = None
        #Sentiment and Subjectivity analysis
        testimonial = TextBlob(corpus)
        urlDat['sp'] = testimonial.sentiment.polarity
        urlDat['ss'] = testimonial.sentiment.subjectivity
        # explanation of metrics
        # https://github.com/shivam5992/textstat
        urlDat['fkg']  = textstat.flesch_kincaid_grade(corpus)
        # Mostly not used:
        # need more clarity about what to plot:
        urlDat['fre'] = textstat.flesch_reading_ease(corpus)
        urlDat['smog']  = textstat.smog_index(corpus)
        urlDat['cliau']  = textstat.coleman_liau_index(corpus)
        urlDat['gf'] = textstat.gunning_fog(corpus)
        urlDat['standard']  = textstat.text_standard(corpus)

        # Good writing should be readable, objective, concise.
        # The writing should be articulate/expressive enough not to have to repeat phrases,
        # thereby seeming redundant. Articulate expressive writing then employs
        # many unique words, and does not yield high compression savings.
        # Good writing should not be obfucstated either. The reading level is a check for obfucstation.
        # The resulting metric is a balance of concision, low obfucstation, expression.

        penalty = urlDat['gf'] + abs(urlDat['sp']) - scaled_density - urlDat['uniqueness']
        urlDat['penalty'] = penalty
    return urlDat


def process_dics(urlDats):
    for urlDat in urlDats:
        # pandas Data frames are best data container for maths/stats, but steep learning curve.
        # Other exclusion criteria. Exclude reading levels above grade 100,
        # as this is most likely a problem with the metric algorithm, and or rubbish data in.
        # TODO: speed everything up, by performing exclusion criteri above not here.
        if urlDat['fkg'] > 100.0 or urlDat['ss'] == 0 or urlDat['eofh'] == 0:
            pass
        else:
            if len(list_per_links) == 0:
                dfs = pd.DataFrame(pd.Series(urlDat)).T
            dfs = pd.concat([ dfs, pd.DataFrame(pd.Series(urlDat)).T ])
    return dfs

'''
Probably depreciated
def web_iter(flat_iter):
    p, fileName, file_contents, index = flat_iter
    urlDat = {}
    try:
        _, _, details = cld2.detect(' '.join(file_contents.iloc[index]['snippet']), bestEffort=True)
        detectedLangName, _ = details[0][:2]
        english = bool(detectedLangName == 'ENGLISH')
    except:
        english = True
    server_status = bool(file_contents.iloc[index]['status']=='successful')
    word_lim = bool(len(file_contents.iloc[index]['snippet']) > WORD_LIM)
    # It's not that we are cultural imperialists, but the people at textstat, and nltk may have been,
    # so we are also forced into this tacit agreement.
    # Japanese characters massively distort information theory estimates, as they are potentially very concise.
    if server_status and word_lim and word_lim:
        urlDat['link_rank'] = file_contents.iloc[index]['rank']
        rank_old = file_contents.iloc[index]['rank']
        urlDat['vslink'] = file_contents.iloc[index]['visible_link']
        urlDat['link'] = file_contents.iloc[index]['link']
        urlDat['keyword'] = file_contents.iloc[index]['query']

        if str('!gs') in urlDat['keyword']:
            urlDat['se'] = 'g_scholar'
        elif str('!yahoo') in urlDat['keyword']:
            urlDat['se'] = 'yahoo'
        elif str('!twitter') in urlDat['keyword']:
            urlDat['se'] = 'twitter'

        else:
            urlDat['se'] = file_contents.iloc[index]['search_engine_name']
        urlDat['stfreq'] = fdist[str(file_contents.iloc[index]['query']).lower()] #frequency of search term

        urlDat['file_path'] = fileName

        ########################################################################
        corpus = file_contents.iloc[index]['snippet']
        urlDat = text_proc(corpus,urlDat)


    return urlDat
'''
