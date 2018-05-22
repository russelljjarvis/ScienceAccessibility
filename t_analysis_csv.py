# Scientific readability project
# authors ...,
# Russell Jarvis
# https://github.com/russelljjarvis/
# rjjarvis@asu.edu

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
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
import os
#os.system('pip install natsort')

from nltk.tag.perceptron import PerceptronTagger
tagger = PerceptronTagger(load=False)

from nltk import word_tokenize,sent_tokenize
from nltk import sent_tokenize, word_tokenize, pos_tag
from nltk.probability import FreqDist
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.corpus import cmudict
from nltk.sentiment import SentimentAnalyzer
from nltk import NgramAssocMeasures
from nltk import compat
from bs4 import BeautifulSoup
import json
#!pip install git+"https://github.com/russelljjarvis/textstat.git"
from textstat.textstat import textstat

from natsort import natsorted, ns

os.system('pip install pycld2')
import pandas as pd
import pycld2 as cld2
import pickle
import os
import base64

import zlib
from nltk import NgramAssocMeasures
from nltk.metrics import ContingencyMeasures
from nltk import bigrams, trigrams
from nltk.metrics import ContingencyMeasures
import pandas as pd

########################################################################
########################################################################
########################################################################


handle = None
TEXT_FOUNTAIN = False
########################################################################
########################################################################
########################################################################
#set filePath below to specify where the data will be going after the code runs
fileLocation = os.getcwd()

if not os.path.exists(fileLocation):
    os.makedirs(fileLocation)

date_created = []

# params are defined in a seperate file, as they are prone to changing,
# yet, different programs draw on them, better to have to only change them in one
# place not three.
from utils_and_paramaters import search_params, engine_dict_list
SEARCHLIST, WEB, LINKSTOGET = search_params()
se, _ = engine_dict_list()

# we first tokenize the text corpus


def lzma_compression_ratio(test_string):
    c = lzma.LZMACompressor()
    bytes_in = bytes(test_string,'utf-8')
    bytes_out = c.compress(bytes_in)
    return len(bytes_out)/len(bytes_in)


WORD_LIM = 600 # word limit

def web_iter(flat_iter):
    # better to rewrite nested for loop as a function to map over.
    # note it's likely that p and index are the same and one should be factored out.
    p, fileName, file_contents, index = flat_iter
    urlDat = {}
    _, _, details = cld2.detect(' '.join(file_contents.iloc[index]['snippet']), bestEffort=True)
    detectedLangName, _ = details[0][:2]
    if file_contents.iloc[index]['status']=='successful' and len(file_contents.iloc[index]['snippet']) > WORD_LIM and detectedLangName == 'ENGLISH':
        urlDat['link_rank'] = file_contents.iloc[index]['rank']
        rank_old = file_contents.iloc[index]['rank']
        urlDat['keyword'] = file_contents.iloc[index]['query']
        urlDat['vslink'] = file_contents.iloc[index]['visible_link']
        urlDat['link'] = file_contents.iloc[index]['link']

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


        # information dense articles are already compressed in language
        # They are concise due to low redundancy
        # if an article is already very dense it's entropy is high
        # and compression savings will be low
        # the difference between compressed and uncompressed should be small.
        comp = str(zlib.compress(corpus.encode(),6))
        comp = comp.split("\\")
        #afc = len(comp)
        ratio = len(corpus.encode())/len(comp)

        #https://pudding.cool/2017/05/song-repetition/
        import lzma

        compression_ratio = lzma_compression_ratio(corpus)
        # big deltas mean redudancy/sparse information/information/density

        # long file lengths lead to big deltas.

        urlDat['info_density'] = compression_ratio

        bm = nltk.collocations.BigramAssocMeasures()
        tm = nltk.collocations.TrigramAssocMeasures()
        bgs = bigrams(tokens)
        tgs = trigrams(tokens)

        trigram = nltk.collocations.TrigramCollocationFinder.from_words(tokens)
        trigram.score_ngrams(tm.raw_freq)
        tpmi = trigram.score_ngrams(tm.pmi)
        urlDat['trimi'] = tpmi


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

        if len(tokens) != 0:
            # explanation of metrics
            # https://github.com/shivam5992/textstat
            urlDat['fkg']  = textstat.flesch_kincaid_grade(str(tokens))


            urlDat['fre'] = textstat.flesch_reading_ease(str(tokens))
            urlDat['smog']  = textstat.smog_index(str(tokens))
            urlDat['cliau']  = textstat.coleman_liau_index(str(tokens))
            urlDat['ri']  = textstat.automated_readability_index(str(tokens))
            urlDat['gf'] = textstat.gunning_fog(str(tokens))
            #print(dir(textstat))
            #urlDat['gl'] =  textstat.grade_level(str(tokens))
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
visited_files = []
# naturally sort a list of files, as machine sorted is not the desired file list hierarchy.
lo_query_links = natsorted(glob.glob(str(os.getcwd())+'/*.csv'))
list_per_links = []

for p,fileName in enumerate(lo_query_links):
    file_contents = pd.read_csv(fileName)
    for index in range(0,len(file_contents)):
        flat_iter.append((p,fileName,file_contents,index))



def process_dics(urlDats,frames = False):
    for urlDat in urlDats:
        #pandas Data frames are best data container for maths/stats, but steep learning curve.
        if frames == True:
            #
            # Other exclusion criteria. Exclude reading levels above grade 100,
            # as this is most likely a problem with the metric algorithm, and or rubbish data in.
            if urlDat['fkg'] > 100.0 or urlDat['ss'] == 0 or urlDat['eofh'] == 0:
                pass
            else:
                if len(list_per_links) == 0:
                    dfs = pd.DataFrame(pd.Series(urlDat)).T
                dfs = pd.concat([ dfs, pd.DataFrame(pd.Series(urlDat)).T ])

        if frames == False:

            # Other exclusion criteria. Exclude reading levels above grade 100,
            # as this is most likely a problem with the metric algorithm, and or rubbish data in.
            if urlDat['fkg'] > 100.0 or urlDat['ss'] == 0 or urlDat['eofh'] == 0:
                pass
            else:
                list_per_links.append(urlDat)

    if frames == False:
        return list_per_links
    else:
        return dfs

urlDats = map(web_iter,flat_iter)
unravel = process_dics(urlDats, frames = False)
with open('unraveled_links.p','wb') as handle:
    pickle.dump(unravel,handle)

'''
#To use functions above with ipython notebook uncomment this code.
import dask.bag as db
grid = {}
import utils_and_parameters
grid , WEB, LINKSTOGET = utils_and_parameters.search_params()

#grid = db.from_sequence(query_list,npartitions = 8)
#list_per_links = map_wrapper(web_iter,grid)
list_per_links = list(map(web_iter,grid))
remove_empty = [i for i in list_per_links if len(i)>0 ]
unravel = []
for i in remove_empty:
    unravel.extend(i)
#print(unravel)

with open('unraveled_links.p','wb') as handle:
    pickle.dump(unravel,handle)
'''
