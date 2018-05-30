import os
from bs4 import BeautifulSoup
from crawl import collect_pubs
import os.path
import pickle
import numpy as np

#from SComplexity import t_analysis, utils_and_paramaters
from SComplexity.crawl import FetchResource# html_to_txt, convert_pdf_to_txt
from SComplexity.t_analysis import text_proc

from SComplexity. utils_and_paramaters import black_string

peter = str('https://academic.oup.com/beheco/article-abstract/29/1/264/4677340')
xkcd_self_sufficient = str('http://splasho.com/upgoer5/library.php')
high_standard = str('https://elifesciences.org/download/aHR0cHM6Ly9jZG4uZWxpZmVzY2llbmNlcy5vcmcvYXJ0aWNsZXMvMjc3MjUvZWxpZmUtMjc3MjUtdjIucGRm/elife-27725-v2.pdf?_hash=WA%2Fey48HnQ4FpVd6bc0xCTZPXjE5ralhFP2TaMBMp1c%3D')
the_science_of_writing = str('https://cseweb.ucsd.edu/~swanson/papers/science-of-writing.pdf')
simple_science = str('https://www.bnl.gov/newsroom/news.php?a=23678')
pmeg = str('http://www.elsewhere.org/pomo/') # Note this is so obfuscated, even the english language classifier rejects it.

try:
    assert 1 == 2
    assert os.path.isfile('benchmarks.p')
    with open('benchmarks.p','rb') as f:
        benchmarks = pickle.load(f)
        [ (pm,pmegr),(hss,hsr),(xkcd,xkcdr),(sow,sowr)] = benchmarks

except:
    # Hardest to read,
    fr = FetchResource(pmeg)
    pmegr = fr.run()
    with open('pmr.p','wb') as f: pickle.dump(pmegr,f)
    # Easiest to read
    fr = FetchResource(xkcd_self_sufficient)
    xkcdr = fr.run()

    # Propounding a very high standard of scientific communication are they hypocrites?
    fr = FetchResource(the_science_of_writing)
    sowr = fr.run()

    fr = FetchResource(high_standard)
    hsr = fr.run()


urlDat = {'link':xkcd_self_sufficient}
xkcd = text_proc(xkcdr,urlDat, WORD_LIM = 100)

urlDat = {'link':the_science_of_writing}
sow = text_proc(sowr,urlDat, WORD_LIM = 100)

urlDat = {'link':high_standard}
hss = text_proc(hsr,urlDat, WORD_LIM = 100)

with open('pmr.p','rb') as f:
    pmegr = pickle.load(f)
urlDat = {'link':pmeg}
pm = text_proc(pmegr,urlDat, WORD_LIM = 100)

#import pdb; pdb.set_trace()

benchmarks = [ (pm,pmegr),(hss,hsr),(xkcd,xkcdr),(sow,sowr)]

with open('benchmarks.p','wb') as f: pickle.dump(benchmarks,f)

ranked = [('post modern essay generator',pm),('upgoer5_corpus',xkcd),('the readability of science decr over time', hss), ('science of writing',sow)]
#winners.append(('simple_science',ss),('sarah_jarvis',sj),('melanie_jarvis',mj),)
ranked = [ r[1] for r in ranked ]
winners = sorted(ranked, key=lambda w: w['gf'])
import pdb; pdb.set_trace()

with open('benchmarks_ranked.p','wb') as f: pickle.dump(winners,f)
