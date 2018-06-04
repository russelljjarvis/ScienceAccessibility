import os
from bs4 import BeautifulSoup
import os.path
import pickle
import numpy as np

from SComplexity.crawl import FetchResource
from SComplexity.t_analysis import text_proc
from SComplexity.utils import black_string
from SComplexity.crawl import collect_pubs

peter = str('https://academic.oup.com/beheco/article-abstract/29/1/264/4677340')
xkcd_self_sufficient = str('http://splasho.com/upgoer5/library.php')
high_standard = str('https://elifesciences.org/download/aHR0cHM6Ly9jZG4uZWxpZmVzY2llbmNlcy5vcmcvYXJ0aWNsZXMvMjc3MjUvZWxpZmUtMjc3MjUtdjIucGRm/elife-27725-v2.pdf?_hash=WA%2Fey48HnQ4FpVd6bc0xCTZPXjE5ralhFP2TaMBMp1c%3D')
the_science_of_writing = str('https://cseweb.ucsd.edu/~swanson/papers/science-of-writing.pdf')
simple_science = str('https://www.bnl.gov/newsroom/news.php?a=23678')
pmeg = str('http://www.elsewhere.org/pomo/') # Note this is so obfuscated, even the english language classifier rejects it.

try:
    assert os.path.isfile('../BenchmarkCorpus/benchmarks.p')
    with open('../BenchmarkCorpus/benchmarks.p','rb') as f:
        benchmarks = pickle.load(f)
        #[ (sj,sjtext),(hss,hsr),(xkcd,xkcdr),(sow,sowr)] = benchmarks
        [ (pm,pmr),(hss,hsr),(xkcd,xkcdr),(sow,sowr),(klpdfp,klpdf)] = benchmarks
except:
    klpd = '../BenchmarkCorpus/planning_document.txt'
    #urlDat = {'link':'githublink'}
    klpdf = open(klpd)
    strText = klpdf.read()
    urlDat = {'link':'local_resource'}

    klpdfp = text_proc(strText,urlDat, WORD_LIM = 100)

    # Hardest to read,
    fr = FetchResource(pmeg)
    pmr = fr.run()
    urlDat = {'link':pmeg}
    pm = text_proc(pmr,urlDat, WORD_LIM = 100)
    # Easiest to read
    fr = FetchResource(xkcd_self_sufficient)
    xkcdr = fr.run()
    urlDat = {'link':xkcd_self_sufficient}
    xkcd = text_proc(xkcdr,urlDat, WORD_LIM = 100)

    # Propounding a very high standard of scientific communication are they hypocrites?
    fr = FetchResource(the_science_of_writing)
    sowr = fr.run()
    urlDat = {'link':the_science_of_writing}
    sow = text_proc(sowr,urlDat, WORD_LIM = 100)

    fr = FetchResource(high_standard)
    hsr = fr.run()
    urlDat = {'link':high_standard}
    hss = text_proc(hsr,urlDat, WORD_LIM = 100)

    benchmarks = [ (pm,pmr),(hss,hsr),(xkcd,xkcdr),(sow,sowr),(klpdfp,klpd)]

    with open('benchmarks.p','wb') as f: pickle.dump(benchmarks,f)
'''
ranked = [('post modern essay generator',pm),('upgoer5_corpus',xkcd),('the readability of science decr over time', hss), ('science of writing',sow), ('planning_document',klpdfp)]
#winners.append(('simple_science',ss),('sarah_jarvis',sj),('melanie_jarvis',mj),)
winners = sorted(ranked, key=lambda w: w[1]['penalty'])

with open('benchmarks_ranked.p','wb') as f: pickle.dump(winners,f)
'''
