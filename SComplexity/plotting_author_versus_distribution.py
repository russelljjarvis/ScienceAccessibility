import pickle
import copy
import matplotlib as mpl
import numpy as np
import pandas as pd
mpl.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns


def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

NAME,ar = pickle.load(open('more_authors_results.p','rb'))
print(ar)

with open('traingDats.p','rb') as f:
    trainingDats = pickle.load(f)

def other_files():
    NAME = str('J. Bryan Henderson')

    brian = pickle.load(open('ben_results.p','rb'))
    ar1 = brian.T.to_dict().values()

    arp = pickle.load(open('author_results_processed.p','rb'))
    arp.pop('rgerkin',None)

    #import pdb; pdb.set_trace()
    for NAME in arp.keys():
        ar = []
        for i in range(0,len(arp[NAME].values())):
            ar.append(list(arp[NAME].values())[i])
            traingDats.extend(ar)

standard_sci = [ t['standard'] for t in trainingDats ]
ar = [ t for t in ar if type(t) is type({})]
ar = [ t for t in ar if 'standard' in t.keys()]
print(ar)
xys = [ (h.get_x(),h.get_height()) for h in sns.distplot(standard_sci).patches ]
# this plot not used yet.

fig = plt.figure()
ax1 = fig.add_subplot(111)
print(ar)
mean_ = np.mean([a['standard'] for a in ar])
min_ = np.min([a['standard'] for a in ar])
max_ = np.max([a['standard'] for a in ar])
std_ = np.std([a['standard'] for a in ar])
stats_items = [mean_,min_,max_]

#import pdb
#pdb.set_trace()
g = sns.distplot(standard_sci, label="Readability Index")


histogram_content = [x[0] for x in xys]
height_content = np.array([x[1] for x in xys])

hc = np.array(histogram_content)

# code for plotting std deviation.
sub_set = np.where((histogram_content>=mean_-std_) & (histogram_content<=mean_+std_))
x_sub_set = np.array(histogram_content)[sub_set]

std_plot_ind = height_content[sub_set]
sub_set = sub_set[0].tolist()

assert len(sub_set) < len(histogram_content)

#vertical_postions = map()
vertical_postions_indexs = []
for i in stats_items:
    vertical_postions_indexs.append(find_nearest(histogram_content, i))
bin_width_offset = (xys[1][0] - xys[0][0])/2.0
x_sub_set = [ i+bin_width_offset for i in x_sub_set ]


heights = []
for i in vertical_postions_indexs:
    heights.append(xys[i][1])
print(heights)
mean_a = mean_# + bin_width_offset
min_a = min_ #+ bin_width_offset
max_a = max_ #+ bin_width_offset
#std_a = mean_ + bin_width_offset
index = find_nearest(histogram_content, mean_)
#mean_link = histogram_content[index]['link']
index = find_nearest(histogram_content, min_)
#min_link = histogram_content[index]['link']
index = find_nearest(histogram_content, max_)
#max_link = histogram_content[index]['link']


data0 = pd.DataFrame({
'mean, min, maximum': [mean_,min_,max_],
    'CDF': heights
    })


data2 = pd.DataFrame({
'Standard Reading Level': [mean_a],
    'CDF': [heights[0]]
    })


data1 = pd.DataFrame({
'Standard Reading Level': x_sub_set,
    'CDF': std_plot_ind
    })

legend_properties = {'weight':'bold','size':8}


ax = sns.regplot(data=data0, x="mean, min, maximum", y="CDF", fit_reg=False, marker="o", color="blue")

#ax = sns.regplot(x='Standard Reading Level', y='CDF',data=data1, fit_reg=False, marker="o", color="green")#, data=fmri)
ax = sns.regplot(data=data2, x="Standard Reading Level", y="CDF", fit_reg=False, marker="o", color="red")

legendMain=ax.legend(labels=[str("std deviation")], prop=legend_properties,loc='upper right')

legendSide0=ax.legend(labels=[NAME],prop=legend_properties,loc='center right')
legendSide1=ax.legend(labels=[str('Number of Documents: '+str(len(ar)))],prop=legend_properties,loc='upper left')
print(len(ar))


legendMain=ax.legend(labels=[str("ART Corpus+ other scholar authors")], prop=legend_properties,loc='upper right')
ax.add_artist(legendMain)
ax.add_artist(legendSide0)
ax.add_artist(legendSide1)
#g=sns.clustermap(corrmat, vmax=.8, square=True)
print(ax.get_xticklabels())
rotation = 90
#for i, ax in enumerate(legendMain.fig.axes):   ## getting all axes of the fig object
#     ax.set_xticklabels([a['link'] for a in ar], rotation = rotation)


#g.fig.show()


locs, labels = plt.xticks()
plt.setp(labels, rotation=45)
plt.savefig(str(NAME[9:15])+'author_readability.png')
