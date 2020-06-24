

import streamlit as st
import os

import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
print(os.system("which firefox"))

from online_app_backend import call_from_front_end
from online_app_backend import ar_manipulation


import pandas as pd
import pickle
import numpy as np
import plotly.figure_factory as ff
import os
import plotly.express as px

#from plotly.subplots import make_subplots

import nltk

trainingDats = pickle.load(open('data/traingDats.p','rb'))
bio_chem = [ t['standard'] for t in trainingDats ]
biochem_labels =  [ x['file_name'] for x in trainingDats if 'file_name' in x.keys()]
biochem_labels = [x.split("/")[-1] for x in biochem_labels ]

lods = []
for i,j,k in zip(bio_chem,[str('Comparison Data') for i in range(0,len(bio_chem))],biochem_labels):
     lods.append({'Reading_Level':i,'Origin':j,'Web_Link':k})
df0 = pd.DataFrame(lods)

theme = px.colors.diverging.Portland
colors = [theme[0], theme[1]]
st.title('Search Reading Difficulty of Academic')
author_name = st.text_input('Enter Author:')
def make_clickable(link):
    # target _blank to open new window
    # extract clickable text to display for your link
    text = link#.split('=')[1]
    return f'<a target="_blank" href="{link}">{text}</a>'

    
if author_name:
    ar = call_from_front_end(author_name)
    standard_sci = [ t['standard'] for t in ar ]
    group_labels = ['Author: '+str(author_name)]#, 'Group 2', 'Group 3']
    scraped_labels = [ str(x['link']) for x in ar]


    lods = []
    for i,j,k in zip(standard_sci,[str(author_name) for i in range(0,len(ar))],scraped_labels):
        lods.append({'Reading_Level':i,'Origin':j,'Web_Link':k})
    df1 = pd.DataFrame(lods)
    df = pd.concat([df1,df0])

    fig0 = px.histogram(df, x="Reading_Level", y="Web_Link", color="Origin",
                    marginal="box",
                    opacity=0.7,# marginal='violin',# or violin, rug
                    hover_data=df.columns,
                    hover_name=df["Web_Link"],
                    color_discrete_sequence=colors)

    fig0.update_layout(title_text='Scholar scraped {0} Versus Art Corpus'.format(author_name),width=900, height=900)#, hovermode='x')
            
    st.write(fig0)


else:      

    with open('data/_author_specificSayali Phatak.p','rb') as f: 
        contents = pickle.load(f)   
    (NAME,ar,df,datay,scholar_link) =  contents     
    (ar, trainingDats) = ar_manipulation(ar)
    standard_sci = [ t['standard'] for t in ar ]

    scraped_labels = [ str(x['link']) for x in ar]
    group_labels = ['Author Scraped']#, 'Group 2', 'Group 3']
    lods = []
    for i,j,k in zip(standard_sci,[str('S Phatak') for i in range(0,len(ar))],scraped_labels):
        lods.append({'Reading_Level':i,'Origin':j,'Web_Link':k})
    df1 = pd.DataFrame(lods)
    df = pd.concat([df1,df0])



    fig0 = px.histogram(df, x="Reading_Level", y="Web_Link", color="Origin",
                    marginal="box",
                    opacity=0.7,# marginal='violin',# or violin, rug
                    hover_data=df.columns,
                    hover_name=df["Web_Link"],
                    color_discrete_sequence=colors)

    fig0.update_layout(title_text='Scholar S Phatak Versus Art Corpus',width=900, height=600)#, hovermode='x')
            
    st.write(fig0)
'''

### Total number scraped documents:

'''
st.text(len(ar))

if np.mean(standard_sci) < np.mean(bio_chem):
    '''


    ### This author was on average easier to read as the average of ARTCORPUS:
    A varied collection of biochemistry science papers
    '''

if np.mean(standard_sci) >= np.mean(bio_chem):
    '''


    ### This author was on average harder or just as hard to read as average of ARTCORPUS:
    A varied collection of biochemistry science papers
    '''


sci_corpus = ''

for t in ar:
    if 'tokens' in t.keys():
        for s in t['tokens']:
            sci_corpus+=str(' ')+s


def art_cloud(acorpus):

    # Generate a word cloud image

    wordcloud = WordCloud().generate(acorpus)
    fig = plt.figure()

    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    st.pyplot()

    return fig


'''


### Here are some word clouds, that show the frequency of scraped texts
You can eye ball them to see if they fit your intuition about what your searched author writes about
'''
fig = art_cloud(sci_corpus)





df_links = pd.DataFrame()
df_links['Web_Link'] = pd.Series(scraped_labels)
df_links['Reading_Level'] = pd.Series(standard_sci)
#st.write(df)
# link is the column with hyperlinks
df_links['Web_Link'] = df_links['Web_Link'].apply(make_clickable)
df_links = df_links.to_html(escape=False)
st.write(df_links, unsafe_allow_html=True)

x1 = df0['Reading_Level']#np.random.randn(200)
x2 = df1['Reading_Level']#np.random.randn(200) + 2
if author_name:
    group_labels = ['Comparison Data ', str(author_name)]
else:
    group_labels = ['Comparison Data ', str('S Phatak')]


colors = [theme[-1], theme[-2]]
rt=list(pd.Series(scraped_labels))
fig = ff.create_distplot([x1, x2], group_labels, bin_size=2,colors=colors,rug_text=rt)

hover_trace = [t for t in fig['data'] if 'text' in t]

fig.update_layout(title_text='Scholar scraped Author Versus Art Corpus')
fig.update_layout(width=900, height=600)#, hovermode='x')

st.write(fig)

list_df = pickle.load(open("data/benchmarks.p","rb")) 
bm = pd.DataFrame(list_df)

bm = bm.rename(columns={'link': 'Web_Link', 'standard': 'Reading_Level'})
bm["Origin"] = pd.Series(["Benchmark" for i in range(0,len(bm))])

bm = bm.drop(4, axis=0)
bm = bm.drop(5, axis=0)

bm_temp = pd.DataFrame()
bm_temp["Origin"] = bm["Origin"]
bm_temp["Web_Link"] = bm["Web_Link"]
bm_temp["Reading_Level"] = bm["Reading_Level"]
import copy
bm = copy.copy(bm_temp)

bm_temp['Web_Link'] = bm_temp['Web_Link'].apply(make_clickable)
bm_temp = bm_temp.to_html(escape=False)

'''
In the table below there are benchmarks texts that are 
used as a comparison to investigate some very easy to read scientific writing.
and some very cryptic and unreadable texts too.
'''

st.write(bm_temp, unsafe_allow_html=True)

x1 = bm['Reading_Level']
x2 = df1['Reading_Level']

x3 = df0['Reading_Level']


rt=list(bm['Web_Link'])
rt.extend(list(df1['Web_Link']))
rt.extend(list(df0['Web_Link']))

colors = [theme[0], theme[4],theme[2]]
if author_name:
    group_labels = ['Ideal Bench Marks ', str(author_name), str('Comparison Data')]
else:
    group_labels = ['Ideal Bench Marks  ', str('S Phatak'), str('Comparison Data')]

fig = ff.create_distplot([x1, x2, x3], group_labels, bin_size=1,colors=colors,rug_text=rt)

hover_trace = [t for t in fig['data'] if 'text' in t]

fig.update_layout(title_text='Benchmarks versus scraped Author')
fig.update_layout(width=900, height=600)#, hovermode='x')

st.write(fig)

#ARTCORPUS = pickle.load(open('traingDats.p','rb'))
#acorpus = ''
#for t in ARTCORPUS:
#    if 'tokens' in t.keys():
#        for s in t['tokens']:
#            acorpus+=str(' ')+s