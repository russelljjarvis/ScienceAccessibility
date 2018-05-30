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


import base64
import pandas as pd
import pickle
import os


# params are defined in a seperate file, as they are prone to changing,
# yet, different programs draw on them, better to have to only change them in one
# place not three.
# Local imports
from utils_and_paramaters import black_string, english_check, comp_ratio, science_string

DEBUG = False

# word limit smaller than 4000 gets product/merchandise sites.
def text_proc(corpus,urlDat, WORD_LIM = 4000):
    #remove unreadable characters
    corpus = corpus.replace("-", " ") #remove characters that nltk can't read
    textNum = re.findall(r'\d', corpus) #locate numbers that nltk cannot see to analyze
    tokens = word_tokenize(corpus)
    tokens = [w.lower() for w in tokens] #make everything lower case
    # the kind of change that might break everything
    sc = ''
    for t in tokens:
         sc += t
    urlDat['wcount'] = textstat.lexicon_count(str(tokens))
    word_lim = bool(urlDat['wcount']  > WORD_LIM)

    try:
        urlDat['english'] = english_check(corpus)
        urlDat['science'] = science_string(sc)
        sc = None
    except:
        urlDat['english'] = True
        urlDat['science'] = False
        server_error = bool(not black_string(corpus))

    if str('keyword') in urldDat.keys():   
        if str('!gs') in urlDat['keyword']:
            urlDat['se'] = 'g_scholar'
        elif str('!wiki') in urlDat['keyword']:
            urlDat['se'] = 'wiki'
        elif str('!twitter') in urlDat['keyword']:
            urlDat['se'] = 'twitter'
    

    # The post modern essay generator is so obfuscated, that ENGLISH classification fails, and this criteria needs to be relaxed.

    if len(tokens) != 0 and urlDat['english'] and word_lim: #  and server_error:

        ##frequency distribtuion of text
        tokens = [ w.lower() for w in tokens if w.isalpha() ]
        fdist = FreqDist(tokens) #frequency distribution of words only
        # The larger the ratio of unqiue words to repeated words the more colourful the language.
        lexicon = textstat.lexicon_count(corpus, True)
        urlDat['uniqueness'] = len(set(tokens))/float(len(tokens))
        urlDat['other_uniqueness'] = lexicon/len(tokens)
        # It's harder to have a good unique ratio in a long document, as 'and', 'the' and 'a', will dominate.
        # big deltas mean redudancy/sparse information/information/density

        # long file lengths lead to big deltas.
        urlDat['info_density'] =  comp_ratio(corpus)
        scaled_density = urlDat['info_density'] * 1/float(urlDat['wcount'])
        urlDat['scaled_info_density'] = scaled_density


        #Sentiment and Subjectivity analysis
        testimonial = TextBlob(corpus)
        urlDat['sp'] = testimonial.sentiment.polarity
        urlDat['ss'] = testimonial.sentiment.subjectivity
        # explanation of metrics
        # https://github.com/shivam5992/textstat

        standard_  = textstat.text_standard(corpus)
        try:
            urlDat['standard']  = float(standard_[0:2])
        except:
            urlDat['standard']  = float(standard_[0:1])

        urlDat['gf'] = textstat.gunning_fog(corpus)
        # special sauce
        # Good writing should be readable, objective, concise.
        # The writing should be articulate/expressive enough not to have to repeat phrases,
        # thereby seeming redundant. Articulate expressive writing then employs
        # many unique words, and does not yield high compression savings.
        # Good writing should not be obfucstated either. The reading level is a check for obfucstation.
        # The resulting metric is a balance conflicted priotities of concision, low obfucstation, expression.
        penalty = urlDat['standard'] - scaled_density - urlDat['uniqueness'] + abs(urlDat['sp'])
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
from utils_and_paramaters import search_params, engine_dict_list
SEARCHLIST, WEB, LINKSTOGET = search_params()
se, _ = engine_dict_list()

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


        else:
            urlDat['se'] = file_contents.iloc[index]['search_engine_name']
        urlDat['stfreq'] = fdist[str(file_contents.iloc[index]['query']).lower()] #frequency of search term

        urlDat['file_path'] = fileName

        ########################################################################
        corpus = file_contents.iloc[index]['snippet']
        urlDat = text_proc(corpus,urlDat)


    return urlDat
'''
