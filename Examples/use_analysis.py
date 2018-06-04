
import glob
from natsort import natsorted, ns
import pprint
import numpy as np
import os


import pickle
from SComplexity.scrape import SW
from SComplexity.analysis import Analysis

#
# naturally sort a list of files, as machine sorted is not the desired file list hierarchy.
# Note this mess could be avoided if I simply stored the mined content somewhere else.
files = natsorted(glob.glob(str(os.getcwd())+'/results_dir/*.p'))



A = Analysis(files)
# A.get_bench() may need debugging

urlDats = A.cas()
with open('unraveled_links.p','wb') as handle:
    pickle.dump(urlDats,handle)

winners = sorted(urlDats, key=lambda w: w['penalty'])   # sort by age


def print_best_text(f):
    link_tuple = pickle.load(open(f,'rb'))
    se_b, page_rank, link, category, buffer = link_tuple
    return buffer


pp = pprint.PrettyPrinter(indent=4)
print('best')
pp.pprint(winners[0])
print('worst')

pp.pprint(winners[-1])

frames = False
if frames ==True:
    unravel = process_dics(urlDats)
else:
    unravel = urlDats
with open('winners.p','wb') as handle:
    pickle.dump(urlDats,handle)


import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import math as math
from pylab import rcParams

known = [ w for w in winners if 'page_rank' not in w.keys()  ]
labels = [ k['link'] for k in known ]
import pdb; pdb.set_trace()

labels = ['upgoer5','Science of Writing','ROFSTDOT','post modern EG']


scraped = [ w for w in winners if 'page_rank' in w.keys()  ]
fogss = [ w['gf'] for w in scraped ]
sps = [ w['sp'] for w in scraped ]
spk = [ w['sp'] for w in known ]
fogk = [ w['gf'] for w in known ]

infos = [ w['scaled_info_density'] for w in scraped ]
infok = [ w['scaled_info_density'] for w in known ]


penaltys = [ w['penalty'] for w in scraped ]
penaltyk = [ w['penalty'] for w in known ]


ranks = [ w['page_rank'] for w in scraped ]

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


#ax = sns.regplot(x=x, y=y, color="g")
#sns.lmplot("x", "y", data=df, hue='dataset', fit_reg=False)
