
import os

from os import path
from wordcloud import WordCloud
import matplotlib
matplotlib.use('Agg')
import pdb
import pandas as pd
from pandas.tools.plotting import table
#import bokeh
from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.models import HoverTool
from bokeh.plotting import figure, output_file, show
#%matplotlib inline
from bokeh.plotting import show, output_notebook, save
from bokeh.models import ColumnDataSource, OpenURL, TapTool
import os
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

import matplotlib.pyplot as plt
from SComplexity import get_bmark_corpus as gbc

import pickle
texts = pickle.load(open('scraped_new.p','rb'))
try:
    assert 1==2
    references = pickle.load(open('references.p','rb'))
    print(references[-1]['standard'])
except:
    references = gbc.get_bmarks()
    pickle.dump(references,open('references.p','wb'))
#import pdb; pdb.set_trace()


pre_science = ''
pre_not_science = ''
wikis = ''

for t in texts:
    if t['science'] == False:
        for s in t['tokens']:
            pre_not_science+=str(' ')+s
    elif t['science'] == True:
        for s in t['tokens']:
            pre_science+=str(' ')+s
    if str('wiki') in t['link']:
        for s in t['tokens']:
            wikis+=str(' ')+s

mean_wiki_pedia = []
for t in texts:
    if t['wiki'] == True:
        if str('standard') in t.keys():

            mean_wiki_pedia.append(t['standard'])
mwp = np.mean(mean_wiki_pedia)

def make_word_clouds(pre_science,pre_not_science,wikis):
    import matplotlib.pyplot as plt

    with open('science.csv', 'w') as f:
        f.write(pre_science)

    with open('not_science.csv', 'w') as f:
        f.write(pre_not_science)
    # Generate a word cloud image
    wordcloud = WordCloud().generate(pre_science)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.savefig('science_cloud.png')# Generate a word cloud image



    wordcloud = WordCloud().generate(pre_not_science)
    #import matplotlib.pyplot as plt
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")

    # lower max_font_size
    wordcloud = WordCloud(max_font_size=40).generate(pre_not_science)
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.savefig('not_science_cloud.png')

    print(wikis)
    wordcloud = WordCloud().generate(wikis)
    #import matplotlib.pyplot as plt
    plt.figure()

    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")

    # lower max_font_size
    #wordcloud = WordCloud(max_font_size=40).generate(wikis)
    #plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.savefig('wikis_cloud.png')
make_word_clouds(pre_science,pre_not_science,wikis)





plt.clf()
plt.title('Sentiment versus Complexity')
## Set x-axis label
references = [ t for t in references if t is not None ]

references = [ t for t in references if str('russell_fog') in t.keys() ]
#references = [ t for t in references if str('russell_fog') in t.keys() ]

df = pd.DataFrame({
    'russell_fog':[ f['russell_fog'] for f in references],
        'sentiment':[ f['sp'] for f in references ],
    'URL':[ f['link'] for f in references ],

})
indexs = [ f['link'] for f in references ]
print(mwp,'mean wikipedia')
df = pd.DataFrame({'complexity':[ f['standard'] for f in references],'texts':indexs})
latex = df.to_latex(index=False)

plt.savefig('xkcd.png')



texts = [ t for t in texts if str('gf') in t.keys() ]



# Create dataframe
df = pd.DataFrame({
    'gunning_fog':[ f['gf'] for f in texts],
    'sentiment':[ f['sp'] for f in texts ],
    'URL':[ f['link'] for f in texts ],
})

ax = sns.lmplot('sentiment','gunning_fog', # Horizontal axis
           data=df, # Data source
           fit_reg=False, # Don't fix a regression line
           size = 10,
           aspect =2 ) # size and dimension


plt.title('Sentiment versus Complexity')
## Set x-axis label
def label_point(x, y, val, ax):
    a = pd.concat({'x': x, 'y': y, 'val': val}, axis=1)
    for i, point in a.iterrows():
        ax.text(point['x']+.02, point['y'], str(point['val']))



#label_point(df.sentiment, df.gunning_fog, df.URL, plt.gca())
plt.savefig('preliminary.png')


source = ColumnDataSource(data=dict(
    y=[ f['gf'] for f in texts ],
    x=[ f['sp'] for f in texts ],
    links=[ f['link'] for f in texts ],
))


hover = HoverTool(tooltips=[
    ("index", "$index"),
    ("(x,y)", "($x, $y)"),
    ("links", "@links"),
])
p = figure(plot_width=1000, plot_height=1000, tools=["tap","hover"],
           title="Sentiment versus Complexity")

p.circle('x', 'y', size=8, source=source)


url = "@links"
taptool = p.select(type=TapTool)
taptool.callback = OpenURL(url=url)

output_file("output_file_name.html")
save(p)
