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
import dask
import matplotlib # Its not that this file is responsible for doing plotting, but it calls many modules that are, such that it needs to pre-empt
# setting of an appropriate backend not an X11 one.
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
import pickle

#text analysis imports

import lzma
from nltk.tag.perceptron import PerceptronTagger
tagger = PerceptronTagger(load=False)

from nltk import word_tokenize,sent_tokenize
from nltk import sent_tokenize, word_tokenize, pos_tag
from nltk.probability import FreqDist
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.corpus import cmudict
from nltk.sentiment import SentimentAnalyzer
#from nltk import NgramAssocMeasures
from nltk import compat
from bs4 import BeautifulSoup
import json
from textstat.textstat import textstat

from natsort import natsorted, ns

import pandas as pd
import pycld2 as cld2
import pickle
import os
import base64

import zlib
#from nltk import NgramAssocMeasures
#from nltk.metrics import ContingencyMeasures
#from nltk import bigrams, trigrams
#from nltk.metrics import ContingencyMeasures
#import pandas as pd
#import lzma

#set filePath below to specify where the data will be going after the code runs
fileLocation = os.getcwd()

# params are defined in a seperate file, as they are prone to changing,
# yet, different programs draw on them, better to have to only change them in one
# place not three.
import os
from utils_and_paramaters import search_params, engine_dict_list
SEARCHLIST, WEB, LINKSTOGET = search_params()
se, _ = engine_dict_list()


def lzma_compression_ratio(test_string):
    import lzma
    c = lzma.LZMACompressor()
    bytes_in = bytes(test_string,'utf-8')
    bytes_out = c.compress(bytes_in)
    return len(bytes_out)/len(bytes_in)


WORD_LIM = 100 # word limit, should be imposed to exclude many pages from analysis, but is not yet used.

def web_iter(flat_iter):

    p, fileName, file_contents, index = flat_iter
    urlDat = {}
    _, _, details = cld2.detect(' '.join(file_contents.iloc[index]['snippet']), bestEffort=True)
    detectedLangName, _ = details[0][:2]
    
    server_status = bool(file_contents.iloc[index]['status']=='successful')
    word_lim = bool(len(file_contents.iloc[index]['snippet']) > WORD_LIM)
    # It's not that we are cultural imperialists, but the people at textstat, and nltk may have been, 
    # so we are also forced into this tacit agreement.
    # Japanese characters massively distort information theory estimates, as they are potentially very concise.
    english = bool(detectedLangName == 'ENGLISH')

    if server_status and word_lim and bool:
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
        ########################################################################
        corpus = file_contents.iloc[index]['snippet']
        #remove unreadable characters
        corpus = corpus.replace("-", " ") #remove characters that nltk can't read
        textNum = re.findall(r'\d', corpus) #locate numbers that nltk cannot see to analyze
        tokens = word_tokenize(corpus)
        tokens = [w.lower() for w in tokens] #make everything lower case
        urlDat['wcount'] = textstat.lexicon_count(str(tokens))
        #sentences
        sents = sent_tokenize(corpus) #split all of text in to sentences
        sents = [w.lower() for w in sents] #lowercase all

        urlDat['sentcount'] = len(sents) #determine number of sentences

        ########################################################################
        ##frequency distribtuion of text
        tokens = [ w.lower() for w in tokens if w.isalpha() ]
        fdist = FreqDist(tokens) #frequency distribution of words only
        urlDat['uniqueness'] = len(set(tokens))/float(len(tokens))
        compression_ratio = lzma_compression_ratio(corpus)
        # big deltas mean redudancy/sparse information/information/density

        # long file lengths lead to big deltas.
        urlDat['info_density'] = compression_ratio
        # cast dict to list
        fd_temp = list(fdist.items())
        urlDat['stfreq'] = fdist[str(file_contents.iloc[index]['query']).lower()] #frequency of search term

        #frequency of all words
        fAll = {}
        for x in range(0,len(fd_temp)):
            fAll[x,1], fAll[x,2] = [y.strip('}()",{:') for y in (str(fd_temp[x])).split(',')]

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

        ########################################################################
        #Sentiment and Subjectivity analysis
        testimonial = TextBlob(corpus)
        urlDat['sp'] = testimonial.sentiment.polarity
        urlDat['ss'] = testimonial.sentiment.subjectivity

        ########################################################################
        #determine syllable count for all words in each sentece
        sentSyl = {}
        WperS = {}
        for n, sent in enumerate(sents):

            #setup sent variable to analyze each sentence individually
            sent = word_tokenize(sent) #tokenize sentence n in to words
            sent = [w.lower() for w in sent if w.isalpha()] #remove any non-text

            WperS[n] = len(sent) #number of words per sentence

            #syllable analysis
            for x in range(0,len(sent)):
                word = sent[x]
                # Count the syllables in the word.
                syllables = textstat.syllable_count(str(word))
                sentSyl[n,x] = syllables

        if len(tokens) != 0:
            # explanation of metrics
            # https://github.com/shivam5992/textstat
            urlDat['fkg']  = textstat.flesch_kincaid_grade(str(tokens))
            # Mostly not used:
            # need more clarity about what to plot:
            urlDat['fre'] = textstat.flesch_reading_ease(str(tokens))
            urlDat['smog']  = textstat.smog_index(str(tokens))
            urlDat['cliau']  = textstat.coleman_liau_index(str(tokens))
            urlDat['ri']  = textstat.automated_readability_index(str(tokens))
            urlDat['gf'] = textstat.gunning_fog(str(tokens))
            urlDat['dcr']  = textstat.dale_chall_readability_score(str(tokens))
            urlDat['dw']  = textstat.difficult_words(str(tokens))
            urlDat['lwf']  = textstat.linsear_write_formula(str(tokens))
            urlDat['standard']  = textstat.text_standard(str(tokens))
            urlDat['file_path'] = fileName
            urlDat['WperS'] = WperS
            urlDat['sentSyl'] = sentSyl
            urlDat['fM'] = fM
            urlDat['fAll'] = fAll
    return urlDat

flat_iter = []
# naturally sort a list of files, as machine sorted is not the desired file list hierarchy.
lo_query_links = natsorted(glob.glob(str(os.getcwd())+'/*.csv'))
list_per_links = []
for p,fileName in enumerate(lo_query_links):
    b = os.path.getsize(fileName)
    if b>250: # this is just to prevent reading in of incomplete data.
        file_contents = pd.read_csv(fileName)
        for index in range(0,len(file_contents)):
            flat_iter.append((p,fileName,file_contents,index))
print(flat_iter)
import pdb; pdb.set_trace()

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

import dask
import dask.bag as db
grid = db.from_sequence(flat_iter)
urlDats = list(db.map(web_iter,grid).compute())

if frames ==True:
    unravel = process_dics(urlDats)
else:
    unravel = urlDats

with open('unraveled_links.p','wb') as handle:
    pickle.dump(unravel,handle)
