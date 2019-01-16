
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
from SComplexity.analysis import Analysis
import pandas as pd

FILES = natsorted(glob.glob(str(os.getcwd())+'/results_dir/*.p'))
# This cannot properly handle wiki files
A = Analysis(FILES, min_word_length = 200)
urlDats = A.cas()
print(urlDats)

scraped = list(filter(lambda url: str('query') in url.keys(), urlDats))

sps = [ w['sp'] for w in scraped ]
fogss = [ w['gf'] for w in scraped ]
infos = [ w['scaled_info_density'] for w in scraped ]
ranks = [ w['page_rank'] for w in scraped ]
print(scraped)

by_query = {}
by_engine = {}

by_engine[str('yahoo')] = list(filter(lambda url: str('yahoo') in url['se'], urlDats))
by_engine[str('scholar')] = list(filter(lambda url: str('scholar') in url['se'], urlDats))
by_engine[str('bing')] = list(filter(lambda url: str('bing') in url['se'], urlDats))
by_engine[str('google')] = list(filter(lambda url: str('google') in url['se'], urlDats))
by_engine[str('duckduckgo')] = list(filter(lambda url: str('duckduckgo') in url['se'], urlDats))
by_engine[str('wiki')] = list(filter(lambda url: str('wikipedia') in url['se'], urlDats))
print(by_engine)
for i in urlDats:
    if 'wikipedia' in i['se']:
        print(i)
#by_query[str('science')]['urlDats']

plt.clf()

fig, ax = plt.subplots()
plt.title('rank versus standard reading level'+str(' wikipedia'))
plt.xlabel('rank')
plt.ylabel('standard')
#print(by_engine['wiki']['ranks'],by_engine['wiki']['standard'])
plt.scatter([i['page_rank'] for i in by_engine['wiki']],[i['standard'] for i in by_engine['wiki']])

#print(by_engine[key]['standard'], by_engine[key]['ranks'])
plt.savefig('standard_vs_rank'+str('wiki')+'.png')

plt.clf()
plt.title('rank versus standard reading level'+str(' wikipedia'))
plt.xlabel('rank')
plt.ylabel('standard')
df1 = pd.DataFrame({'reading_level':[i['standard'] for i in by_engine['wiki']],'rank':[i['page_rank'] for i in by_engine['wiki']]})
ax = sns.regplot(x="rank", y="reading_level", data=df1, x_estimator=np.mean, x_jitter=.1)
plt.legend(loc="upper left")
plt.savefig('Trend rank versus standard reading level'+str(' wikipedia'))
plt.close()

plt.clf()
fig, ax = plt.subplots()
plt.title('compression ratio versus rank'+str(' wikipedia'))
plt.xlabel('rank')
plt.ylabel('compression ratio')
#plt.scatter(by_engine['wiki']['ranks'],by_engine['wiki']['standard'])
plt.scatter([i['page_rank'] for i in by_engine['wiki']],[i['info_density'] for i in by_engine['wiki']])

#print(by_engine[key]['info_density'], by_engine[key]['ranks'])
plt.savefig('compression_ratio'+str('wiki')+'.png')


plt.clf()
plt.title('rank versus compression ratio'+str(' wikipedia'))
plt.xlabel('rank')
plt.ylabel('standard')
df1 = pd.DataFrame({'compressiion_ratio':[ i['info_density'] for i in by_engine['wiki']],'rank':[    i['page_rank'] for i in by_engine['wiki']]})
ax = sns.regplot(x="rank", y="compressiion_ratio", data=df1, x_estimator=np.mean, x_jitter=.1)
plt.legend(loc="upper left")
plt.savefig('Trend rank versus compression ratio'+str(' wikipedia'))
plt.close()


reference = A.get_reference_web()
labels = [ w['link'] for w in reference ]
by_query['reference'] = {}
by_query['reference']['sp'] = [ w['sp'] for w in reference ]
by_query['reference']['standard'] = [ w['standard'] for w in reference ]
by_query['reference']['info_density'] = [ w['info_density'] for w in reference ]


plt.clf()
fig, axes = plt.subplots()
axes.set_title('gunning fog complexity versus sentiment polarity')
plt.xlabel('reference source')
plt.ylabel('reading level')
#plt.scatter(sps,fogss,label="scrapped data points")
plt.scatter([i for i in range(0,len(labels))],by_query['reference']['standard'],label=labels)
plt.savefig('reference_versus_reading_level.png')

plt.clf()
fig, axes = plt.subplots()
axes.set_title('gunning fog complexity versus sentiment polarity')
plt.xlabel('reference source')
plt.scatter([i for i in range(0,len(labels))],by_query['reference']['info_density'],label=labels)
plt.savefig('reference_versus_compression_ratio.png')



query_keys = list(set([ s['query'] for s in urlDats ]))
engine_keys = by_engine.keys()

science_keys = [ 'evolution', 'photosysnthesis' ,'Transgenic', 'GMO', 'climate change', 'cancer', 'Vaccines', 'Genetically Modified Organism']
culture_keys = ['reality TV', 'prancercise philosophy',  'play dough delicious deserts', 'unicorn versus brumby', 'football soccer']

by_query[str('science')] = {}
by_query[str('science')]['urlDats'] = list(filter(lambda url: url['query'] in science_keys, scraped))

by_query[str('culture')] = {}
by_query[str('culture')]['urlDats'] = list(filter(lambda url: url['query'] in culture_keys, scraped))


fogss_culture = [ w['gf'] for w in by_query[str('culture')]['urlDats'] ]
ranks_culture = [ w['page_rank'] for w in by_query[str('culture')]['urlDats'] ]



fogss_science = [ w['gf'] for w in by_query[str('science')]['urlDats'] ]
ranks_science = [ w['page_rank'] for w in by_query[str('science')]['urlDats'] ]


plt.clf()
fig, ax = plt.subplots()



plt.clf()
plt.title('culture rank versus complexity')
plt.xlabel('rank')
plt.ylabel('standard')
df0 = pd.DataFrame({'complexity':fogss_culture,'rank':ranks_culture})
ax = sns.regplot(x="rank", y="complexity", data=df0, x_estimator=np.mean, x_jitter=.1)
plt.legend(loc="upper left")
plt.savefig('culture_rank_vs_complexity.png')
plt.close()


plt.clf()
plt.title('science rank versus complexity')
plt.xlabel('rank')
plt.ylabel('standard')
df1 = pd.DataFrame({'complexity':fogss_science,'rank':ranks_science})
ax = sns.regplot(x="rank", y="complexity", data=df1, x_estimator=np.mean, x_jitter=.1)
plt.legend(loc="upper left")
plt.savefig('science_rank_vs_complexity.png')
plt.close()


ses = [ url['se'] for url in scraped ]

plt.clf()
fig, axes = plt.subplots()
axes.set_title('gunning fog complexity versus sentiment polarity')
#plt.xlabel('sentiment')
plt.scatter(spk,fogk,label="reference data")


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
plt.scatter(infok,fogk,label="reference data points")
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
axes.set_title('gunning fog complexity versus page rank in climate')
plt.xlabel('page rank')
plt.ylabel('gunning fog')
plt.scatter(climate_ranks,climate_fogs,label="scrapped data points")
#plt.scatter(spk,fogk,label="reference points")
plt.legend(loc="upper left")
fig.tight_layout()
plt.savefig(str('gf_vs_page_rank_climate.png'))
plt.close()

for key in query_keys:
    by_query[key] = {}
    by_query[key]['urlDats'] = list(filter(lambda url: str(key) == url['query'], scraped))
    by_query[key]['ranks'] = [ w['page_rank'] for w in by_query[key]['urlDats'] ]
    by_query[key]['standards'] = [ w['standard'] for w in by_query[key]['urlDats'] ]
    by_query[key]['penalty'] = [ w['penalty'] for w in by_query[key]['urlDats'] ]
    by_query[key]['sp'] = [ w['sp'] for w in by_query[key]['urlDats'] ]
    by_query[key]['s_mean'] = np.mean([ w['standard'] for w in by_query[key]['urlDats'] ])
    by_query[key]['s_std'] = np.std([ w['standard'] for w in by_query[key]['urlDats'] ])

    by_query[key]['scaled_info_density'] = [ w['scaled_info_density'] for w in by_query[key]['urlDats'] ]
    plt.clf()
    fig, ax = plt.subplots()

    plt.title('sent versus complexity')
    plt.xlabel('sentiment')
    plt.ylabel('standard')
    df = pd.DataFrame({'complexity': by_query[key]['standards'],'sentiment': by_query[key]['sp']})
    ##
    # Uncomment to compare to reference data points.
    ##

    # ref = pd.DataFrame({'complexity': [ w['standard'] for w in reference ],'sentiment': [ w['sp'] for w in reference ]})
    # ax = sns.regplot(x="complexity",y="sentiment", data=ref, ax=ax)

    ax = sns.regplot(x="complexity",y="sentiment", data=df, ax=ax)

    legend = ax.legend(loc='upper center', shadow=True)
    plt.legend(loc="upper left")

    plt.savefig('sentiment_vs_complexity_{0}.png'.format(key))
    plt.close()


    plt.clf()
    plt.title('rank versus complexity')
    plt.xlabel('rank')
    plt.ylabel('standard')
    df = pd.DataFrame({'complexity':by_query[key]['standards'],'rank':by_query[key]['ranks']})
    ax = sns.regplot(x="complexity",y="rank", data=df)
    plt.legend(loc="upper left")
    plt.savefig('rank_vs_complexity{0}.png'.format(key))
    plt.close()



for key in engine_keys:
    by_engine[key] = {}

    by_engine[key]['urlDats'] = list(filter(lambda url: str(key) == url['se'], scraped))
    by_engine[key]['ranks'] = [ w['page_rank'] for w in by_engine[key]['urlDats'] ]
    by_engine[key]['standard'] = [ w['standard'] for w in by_engine[key]['urlDats'] ]
    by_engine[key]['penalty'] = [ w['penalty'] for w in by_engine[key]['urlDats'] ]
    by_engine[key]['sp'] = [ w['sp'] for w in by_engine[key]['urlDats'] ]
    by_engine[key]['s_mean'] = np.mean([ w['standard'] for w in by_engine[key]['urlDats'] ])
    by_engine[key]['s_std'] = np.std([ w['standard'] for w in by_engine[key]['urlDats'] ])

    by_engine[key]['info_density'] = [ w['info_density'] for w in by_engine[key]['urlDats'] ]
    plt.clf()

    fig, ax = plt.subplots()
    plt.title('rank versus standard reading level'+str(key))
    plt.xlabel('rank')
    plt.ylabel('standard')
    plt.scatter(by_engine[key]['ranks'],by_engine[key]['standard'])
    #print(by_engine[key]['standard'], by_engine[key]['ranks'])
    plt.savefig('standard_vs_rank'+str(key)+'.png')

    plt.clf()
    fig, ax = plt.subplots()
    plt.title('compression ratio versus rank'+str(key))
    plt.xlabel('rank')
    plt.ylabel('compression ratio')
    plt.scatter(by_engine[key]['ranks'],by_engine[key]['standard'])
    #print(by_engine[key]['info_density'], by_engine[key]['ranks'])
    plt.savefig('compression_ratio'+str(key)+'.png')

    #df = pd.DataFrame({'complexity': by_engine[key]['standards'],'ranks':by_engine[key]['ranks']})
    ##
    # Uncomment to compare to reference data points.

    #ax = sns.regplot(x="complexity",y="ranks", data=df, ax=ax)
    #df = pd.DataFrame({'scaled_info_density': by_engine[key]['scaled_info_density'],'ranks':by_engine[key]['ranks']})
    ##
    # Uncomment to compare to reference data points.
    ##

    # ref = pd.DataFrame({'complexity': [ w['standard'] for w in reference ],'sentiment': [ w['sp'] for w in reference ]})
    # ax = sns.regplot(x="complexity",y="sentiment", data=ref, ax=ax)
    #ax = sns.regplot(x="scaled_info_density",y="ranks", data=df, ax=ax)
    #legend = ax.legend(loc='upper center', shadow=True)
    #plt.legend(loc="upper left")

    #plt.savefig('sentiment_vs_complexity_{0}.png'.format(key))
    #plt.close()

    '''
    plt.clf()
    plt.title('rank versus complexity')
    plt.xlabel('rank')
    plt.ylabel('standard')
    df = pd.DataFrame({'complexity':by_engine[key]['standards'],'rank':by_engine[key]['ranks']})
    ax = sns.regplot(x="complexity",y="rank", data=df)
    plt.legend(loc="upper left")
    plt.savefig('rank_vs_complexity{0}.png'.format(key))
    plt.close()
    '''

'''
plt.clf()
fig, axes = plt.subplots()
axes.set_title('gunning fog complexity versus sentiment polarity')
#plt.xlabel('sentiment')
plt.scatter(spk,fogk,label="reference data")


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
plt.scatter(infok,fogk,label="reference data points")
plt.legend(loc="upper left")
fig.tight_layout()
plt.savefig(str('info_density_vs_complexity.png'))
plt.close()


plt.clf()
axes.set_title('gunning fog complexity versus page rank in climate')
plt.xlabel('page rank')
plt.ylabel('gunning fog')
plt.scatter(climate_ranks,climate_fogs,label="scrapped data points")
#plt.scatter(spk,fogk,label="reference points")
plt.legend(loc="upper left")
fig.tight_layout()
plt.savefig(str('gf_vs_page_rank_climate.png'))
plt.close()

Word Complexity Project:

General hypothesis: The language that scientists and many science educators use online is more complex than language used by non-scientists and science deniers.

Problem: This leads to the most readable and findable information being potentially less accurate (especially regarding controversial issues),
while the most accurate information is likely more difficult to find in searches and will have less impact.

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
