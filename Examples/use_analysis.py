
import glob
from natsort import natsorted, ns
import pprint
import numpy as np
import os

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import math as math
from pylab import rcParams


import pickle
from SComplexity.scrape import SW
from SComplexity.analysis import Analysis

#
# naturally sort a list of files, as machine sorted is not the desired file list hierarchy.
# Note this mess could be avoided if I simply stored the mined content somewhere else.
files = natsorted(glob.glob(str(os.getcwd())+'/results_dir/*.p'))

A = Analysis(files)
benchmark = A.get_bench()# may need debugging
urlDats = A.cas()
urlDats.extend(benchmark)
winners = sorted(urlDats, key=lambda w: w['penalty'])   # sort by age


known = list(filter(lambda url: str('query') not in url.keys(), urlDats))
labels = [ w['link'] for w in known ]

scraped = list(filter(lambda url: str('query') in url.keys(), urlDats))

fogss = [ w['gf'] for w in scraped ]
sps = [ w['sp'] for w in scraped ]

spk = [ w['sp'] for w in known ]
fogk = [ w['gf'] for w in known ]

infos = [ w['scaled_info_density'] for w in scraped ]
infok = [ w['scaled_info_density'] for w in known ]


penaltys = [ w['penalty'] for w in scraped ]
penaltyk = [ w['penalty'] for w in known ]


ranks = [ w['page_rank'] for w in scraped ]


#urlDats = list(filter(lambda url: str('penalty') in url.keys(), urlDats))

GMOs = list(filter(lambda url: str('GMO') == url['query'], scraped))
climate = list(filter(lambda url: str('climate') in url['query'], scraped))
vaccine = list(filter(lambda url: str('Vaccine') in url['query'], scraped))

#import pdb; pdb.set_trace()

plt.clf()
fig, axes = plt.subplots()
axes.set_title('gunning fog complexity versus sentiment polarity')
plt.xlabel('sentiment')
plt.ylabel('gunning fog')
plt.scatter(sps,fogss,label="scrapped data points")
plt.scatter(spk,fogk,label="reference data")
#labels = ['Variable {0}'.format(i+1) for i in range(n)]
for label, x, y in zip(labels, spk, fogk):
    plt.annotate(
        label,
        xy=(x, y), xytext=(40, 40),
        textcoords='offset points', ha='left', va='top',
        bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
        arrowprops=dict(arrowstyle = '->', connectionstyle='arc3,rad=0'))

plt.plot()
plt.legend(loc="upper left")
fig.tight_layout()
plt.savefig(str('sentiment_vs_complexity.png'))
plt.close()

plt.clf()
axes.set_title('info versus fog')
plt.xlabel('info density')
plt.ylabel('gunning fog')
plt.scatter(infos,fogss,label="scrapped data points")
#plt.scatter(infok,fogk,label="reference data points")
plt.legend(loc="upper left")
fig.tight_layout()
plt.savefig(str('info_density_vs_complexity.png'))
plt.close()

plt.clf()
axes.set_title('penalty versus fog')
plt.xlabel('penalty')
plt.ylabel('gunning fog')
plt.scatter(penaltys,fogss,label="scrapped data points")
plt.scatter(penaltyk,fogk,label="reference data points")
for label, x, y in zip(labels, penaltyk, fogk):
    plt.annotate(
        label,
        xy=(x, y), xytext=(40, 40),
        textcoords='offset points', ha='left', va='top',
        bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
        arrowprops=dict(arrowstyle = '->', connectionstyle='arc3,rad=0'))

plt.legend(loc="upper left")
fig.tight_layout()
plt.savefig(str('penalty_vs_fog.png'))
plt.close()

plt.clf()
axes.set_title('gunning fog complexity versus page rank')
plt.xlabel('page rank')
plt.ylabel('gunning fog')
plt.scatter(ranks,fogss,label="scrapped data points")
#plt.scatter(spk,fogk,label="reference points")
plt.legend(loc="upper left")
fig.tight_layout()
plt.savefig(str('gf_vs_page_rank.png'))
plt.close()
'''
Word Complexity Project:

General hypothesis: The language that scientists and many science educators use online is more complex than language used by non-scientists and science deniers.

Problem: This leads to the most readable and findable information being potentially less accurate (especially regarding controversial issues), while the most accurate information is likely more difficult to find in searches and will have less impact.

1. Text complexity vs. site ranking within and between searches
Are simpler texts ranking higher in Google?
How do scientific texts fare within this ranking?
a. For various scientific searches vs. various non-scientific searches
i. Sci searches may be: Genetics, evolution, cancer, vaccine, GMO, climate change, photosynthesis
ii. Non-sci searches may be: Soccer, culture, reality television, ???
b. Also perhaps targeted comparisons of ideal educational websites vs average?

2. Text complexity vs. text sentiment
Are more neutral/factual websites more complex?
a. Rank pro, anti, and neutral websites for text complexity
i. Vaccines
ii. GMOs
iii. Climate change

3. Case studies: Complexity of texts using scientific vs. non-scientific terms
Are scientists using overly complex (but more precise) language online?
a. GMO vs. transgenics
b. Global warming vs. climate change vs. anthropogenic climate change
c. (though non-scientific, perhaps) Intelligent design vs. evolution
d. Also perhaps targeted comparisons of scientist-led blogs vs. public-led blogs covering specific scientific subjects? *can’t be batch processed

Additional questions:
-In Russell’s general search graphs, two clusters of websites seemed to fall out in the graphs. How do we figure out what is causing this?

Issues to consider:
-Are the first few, super successful sites outliers? Should we run these with and without the first page of results to see the differences?

-If AAB sources come up in any of these, should they be automatically excluded?
'''


#ax = sns.regplot(x=x, y=y, color="g")
#sns.lmplot("x", "y", data=df, hue='dataset', fit_reg=False)
