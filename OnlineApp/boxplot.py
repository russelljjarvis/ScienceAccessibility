
# coding: utf-8

# # Markdown Cell Example 
# markdown can be readibly interleaved and dispersed between code in notebooks 
# ## Explanation of code below
# The histogram (x-axis) binned readability score, (y-axis) counts of papers that occupy that readability score. 
# 
# The histogram is initially populated exclusively by the ART corpus, but the idea was every time a new author got scraped from scholar, it would be added in, such that with each persons new search our big picture of science readability would be better informed.
# 
# So the histogram changes a little modestly perceptible amount with the author scrape, but three dots pertaining to the authors easiest read, hardest read, and mean read where added.
# 
# These used to be ```[mean-standard dev, mean, mean+standard dev]``` but there was a flaw implementing that. It could just be that the plot looked way too busy around the mean, and it was harder to look at.
# 
# There is an issue with getting the dots to appear in the centre of histogram bins. I was working under the assumption, that if I knew the ```[min,mean,max]```, readability scores for Rick Gerkin, I could add to them half the bin width, and dot's would be centred. That is almost correct. I forgot that these calculations are not performed on pre binned data, so the x-coordinates of ```[min,mean,max]``` need to be slightly shifted to the nearest histogram bin start first.
# 
# Think of it as a bit like snapping something to a grid in photoshop.

# It should be easy to hack this code to run off a local machine, using sudo.
# Set up the Environment. This is now done in requirements, and the postBuild script.
# ```python
# !pip install matplotlib
# !pip install pandas
# !pip install seaborn
# 
# if os.path.exists('traingDats.p?dl=0'):
#     pass
# 
# else:
#     !wget https://www.dropbox.com/s/3h12l5y2pn49c80/traingDats.p?dl=0
#     !wget https://www.dropbox.com/s/crarli3772rf3lj/more_authors_results.p?dl=0
#     !wget https://www.dropbox.com/s/x66zf52himmp5ox/benchmarks.p?dl=0
# ```

# In[25]:


import warnings
warnings.filterwarnings("ignore")
import pickle
import copy
import matplotlib as mpl
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
#import plotly as py

import glob
files = glob.glob("*.p")
discontents = pickle.load(open("_author_specificS S Phatak.p","rb"))
type(discontents[0])
df = discontents[0]
#print(type())


# In[26]:


try:
    with open('scraped_new.p?dl=0','rb') as f:
        texts = pickle.load(f) 
except:
    get_ipython().system('wget https://www.dropbox.com/s/1kc7alp79h701hx/scraped_new.p?dl=0')
    with open('scraped_new.p?dl=0','rb') as f:
        texts = pickle.load(f) 

queries = set([t['query'] for t in texts ])
temp = [t for t in texts if 'standard' in t.keys() and 'wikipedia' in t['link']]
science = ['cancer','Vaccines','evolution','climate change','Transgenic','photosysnthesis','evolution','GMO']
res = [t['standard'] for t in temp if t['query'] in science]
#res = [t['standard'] for t in temp]# if t['query'] in science]

mwp = np.mean(res)  
abstract_wiki = {'standard':mwp}


# In[27]:


#!pip install matplotlib
#!pip install pandas
#!pip install seaborn

if os.path.exists('traingDats.p?dl=0'):
    pass

else:
    get_ipython().system('wget https://www.dropbox.com/s/3h12l5y2pn49c80/traingDats.p?dl=0')
    get_ipython().system('wget https://www.dropbox.com/s/crarli3772rf3lj/more_authors_results.p?dl=0')
    get_ipython().system('wget https://www.dropbox.com/s/x66zf52himmp5ox/benchmarks.p?dl=0')
with open('traingDats.p?dl=0','rb') as f:
        trainingDats = pickle.load(f) 

bmark = pickle.load(open('benchmarks.p?dl=0','rb'))

ar = discontents[2]
np.mean(df['standard'])
NAME = "Sayali S. Phatak"
trainingDats.extend(bmark)


# In[28]:


print([b['standard'] for b in bmark])


# In[29]:



def get_heights(stats_items,histogram_content,x_sub_set):
    vertical_postions_indexs = []
    for i in stats_items:
        vertical_postions_indexs.append(find_nearest(histogram_content, i))
    bin_width_offset = (xys[1][0] - xys[0][0])/2.0
    x_sub_set = [ i+bin_width_offset for i in x_sub_set ]


    heights = []
    for i in vertical_postions_indexs:
        heights.append(xys[i][1])
    return heights, bin_width_offset


def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

def snap_to_grid(author_stats,bin_centers):
    author_stats_grid = []
    for as_ in author_stats:
        as_ = find_nearest(bin_centers,as_)
        author_stats_grid.append(bin_centers[as_])
    return author_stats_grid


# In[30]:


max_ART = np.max([ t['standard'] for t in trainingDats ])
publication = [ t['publication'] for t in trainingDats if t['standard'] == max_ART ]
keys = [ t.keys() for t in trainingDats if t['standard'] == max_ART ]

fname = [ t['file_name'] for t in trainingDats if t['standard'] == max_ART ]
bmark_max_art = {'standard':max_ART}
#max_ART


# In[31]:


get_ipython().run_cell_magic('capture', '', 'plt.ioff()\n\nstandard_sci = [ t[\'standard\'] for t in trainingDats ]\nar = [ t for t in ar if type(t) is type({})]\nar = [ t for t in ar if \'standard\' in t.keys()]\nxys = [ (h.get_x(),h.get_height()) for h in sns.distplot(standard_sci).patches ]\n\nx_grid = [ h.get_x() for h in sns.distplot(standard_sci).patches ]\noffset = float((x_grid[1] - x_grid[0])/2.0)\nbin_centers = [gr+offset for gr in x_grid]\n# this plot not used yet.\n\nfig = plt.figure(figsize=(10, 8), dpi=80)\nax1 = fig.add_subplot(111)#)\nmean_ = np.mean([a[\'standard\'] for a in ar])\nmin_ = np.min([a[\'standard\'] for a in ar])\nmax_ = np.max([a[\'standard\'] for a in ar])\nstd_ = np.std([a[\'standard\'] for a in ar])\nstats_items = [mean_,min_,max_]\n\ng = sns.distplot(standard_sci, label="Readability Index")\n\n\nhistogram_content = [x[0] for x in xys]\nheight_content = np.array([x[1] for x in xys])\n\nhc = np.array(histogram_content)\n\nx_sub_set=histogram_content\n\n\nother_name=str(\'Phytochromobilin C15-Z,syn - C15-E,anti isomerization: concerted or stepwise?\')\nworst_height,_ = get_heights([max_ART],hc,x_sub_set)\nmwp_height,_ = get_heights([mwp],hc,x_sub_set)\n\n#bmark_max_art\nworst_height = worst_height[0]\n#bmark_stats_items_grid = snap_to_grid(bmark_stats_items,bin_centers)\n\n#worst_distamnce = snap_to_grid(max_ART,bin_centers)\nworst_distance = snap_to_grid([max_ART],bin_centers)\nmwp_distance = snap_to_grid([mwp],bin_centers)\nx,y,z = (mwp_distance[0],mwp_height[0],str(\'mean wikipedia\'))\n\n#print(bmark)\nbmark_stats_items = list(set([ b[\'standard\'] for b in bmark ]))\nbmark_stats_items.append(x)\n#bmark_stats_items.append(max_ART)\nbmark_heights, _ = get_heights(bmark_stats_items,histogram_content,x_sub_set)\nheights, bwo = get_heights(stats_items,histogram_content,x_sub_set)\n#bmark_heights.append(worst_height)\nbmark_stats_items = [i+bwo for i in bmark_stats_items]\nmean_a = mean_\nmin_a = min_ \nmax_a = max_ \nxticks = list(range(0,45,5))\n\n#print(xticks)\nbmark_stats_items\nbox_content = [a[\'standard\'] for a in ar]')


# In[32]:



bmark_stats_items_grid = snap_to_grid(bmark_stats_items,bin_centers)
author_stats =[i for i in [mean_,min_,max_]]
author_stats_grid = snap_to_grid(author_stats,bin_centers)
mean_a_grid = snap_to_grid([mean_a],bin_centers)
x_sub_set_grid = snap_to_grid(x_sub_set,bin_centers)

print(bmark_stats_items_grid)
#print(x)
#bmark_stats_items_grid.append(x)
#bmark_stats_items_grid
#bmark


# In[33]:


categories = [ "Readibility of Science Declining Over Time", "Post Modern Essay Generator","upgoer 5","Science of Writing","Mean Wikipedia"]#"Mean Wikipedia"]#,other_name]# "wikipedia science"]
bmark_stats_items_grid


# In[34]:


recalibrate_heights,b = get_heights(author_stats_grid,hc,x_sub_set)

heights[0] = np.max(recalibrate_heights)
heights[2] = recalibrate_heights[2]


# In[35]:


np.max(height_content)
heights


# In[36]:


bmark_heights
print(len(bmark_heights))
print(len(bin_centers))
print(len(bmark_stats_items))


# In[37]:


print(len(bmark_stats_items_grid))


# In[14]:


ar = np.array(ar)


# In[17]:


from pylab import *


# In[18]:


bmark_stats_items


# In[19]:


#categories
#categories.insert(3,'Mean Wikipedia Science')


# In[20]:


#xinterval
x1,y1,z1 = (mwp_distance[0],mwp_height[0],str('mean wikipedia'))
x1
#bmark_heights[3]=y1


# In[21]:


set(bmark_stats_items_grid)
import copy
#del bmark_stats_items_grid[-2]
#del bmark_stats_items_grid[-1]
xinterval1 = copy.copy(bmark_stats_items_grid)
#xinterval1.insert(3,x1)
#xinterval1
#del bmark_heights[-1]
bmark_heights
print(len(bmark_heights))
print(len(bmark_stats_items_grid))

benchmarks = pd.DataFrame({
'benchmarks': bmark_stats_items_grid,
    'CDF': bmark_heights
    })


# In[22]:


get_ipython().run_line_magic('matplotlib', 'inline')

import numpy as np
import scipy
import pandas as pd
from scipy.stats import norm
import matplotlib.pyplot as plt

fig, axes = plt.subplots(figsize=(10, 10),nrows=2, ncols=1, sharex=True, dpi=100)


g = sns.distplot(standard_sci, label="Readability Index")


if str('data0') not in locals():
    data0 = pd.DataFrame({
    'mean, min, maximum': author_stats_grid,
        'CDF': heights
        })


    data2 = pd.DataFrame({
    'Standard Reading Level': mean_a_grid,
        'CDF': np.max(height_content)
        })




legend_properties = {'weight':'bold','size':8}
ax = sns.regplot(data=benchmarks, x="benchmarks", y="CDF", fit_reg=False, marker="o", color="green")
ax = sns.regplot(data=data2, x="Standard Reading Level", y="CDF", fit_reg=False, marker="o", color="red")
legendMain=ax.legend(labels=[str("std deviation")], prop=legend_properties,loc='upper right')
legendSide0=ax.legend(labels=[NAME],prop=legend_properties,loc='center right')
legendSide1=ax.legend(labels=[str('Number of Documents: '+str(len(ar)))],prop=legend_properties,loc='upper left')
legendMain=ax.legend(labels=[str("Google scholar author relative to ART Corpus distribution. Total docs: ")+str(len(trainingDats))], prop=legend_properties,loc='upper left')
#
print(categories)
x,y,z = (worst_distance[0],worst_height,other_name)
data3 = pd.DataFrame({
'Standard Reading Level': [x1],
    'CDF': [y1]
    })
ax = sns.regplot(data=data3, x='Standard Reading Level', y="CDF", fit_reg=False, marker="o", color="green")


axes[1] = ax = sns.regplot(data=benchmarks, x="benchmarks", y="CDF", fit_reg=False, marker="o", color="green")

ax2 = plt.twiny()
xticks = list(range(0,45,5))
ax2.set_xticks(xticks)

axes[1].set_xticks(xinterval1)
axes[1].set_xticklabels(categories, minor=False, rotation=90)

axes[1].axvline(np.mean(standard_sci), color='red', alpha=.7, linewidth=1.5)
axes[1].set_ylabel('Probability of Document Reading Level')
axes[1].set_xlabel('Reading Grade Level')
bp_dict = axes[0].boxplot(box_content, 0, 'gD', vert=False)


for line in bp_dict['medians']:
    x, y = line.get_xydata()[1] # top of median line

for line in bp_dict['boxes']:
    x0, y = line.get_xydata()[0] # bottom of left line
    axes[0].text(x0,y, str(NAME)+' Q1 ',horizontalalignment='center',verticalalignment='top',rotation=90)

    x1, y = line.get_xydata()[3] # bottom of right line
    axes[0]. text(x1,y, str(NAME)+' Q3 ',horizontalalignment='center',verticalalignment='top',rotation=90)

    axes[0]. text(np.abs(x1+x0)/2,y, str(NAME)+' $\mu$ ',horizontalalignment='center',verticalalignment='top',rotation=90)
    x2, y = line.get_xydata()[1] # bottom of right line
axes[0].axvline(np.mean(standard_sci), color='red', alpha=.7, linewidth=1.5)

    


# In[23]:


categories


# In[24]:


bmark_stats_items_grid

