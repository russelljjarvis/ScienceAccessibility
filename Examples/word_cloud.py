
import os

from os import path
from wordcloud import WordCloud
import matplotlib
matplotlib.use('Agg') 
# get data directory (using getcwd() is needed to support running example in generated IPython notebook)
d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()

# Read the whole text.
#text = open(path.join(d, 'constitution.txt')).read()
#references.p  scraped_new.p
import pickle
texts = pickle.load(open('scraped_new.p','rb'))
#import pdb
#pdb.set_trace()
#for t in texts:
pre_science = ''
pre_not_science = ''
for t in texts:
    if t['publication'][0] == False:
        for s in t['tokens']: pre_not_science+=str(' ')+s
    elif t['publication'][0] == True:
        for s in t['tokens']: pre_science+=str(' ')+s

# Generate a word cloud image
wordcloud = WordCloud().generate(pre_science)
print(wordcloud)
# Display the generated image:
# the matplotlib way:
import matplotlib.pyplot as plt

plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")

# lower max_font_size
#wordcloud = WordCloud(max_font_size=40).generate(text)
#plt.figure()
#plt.imshow(wordcloud, interpolation="bilinear")
#plt.axis("off")
plt.savefig('science_cloud.png')# Generate a word cloud image



wordcloud = WordCloud().generate(pre_not_science)

# Display the generated image:
# the matplotlib way:
import matplotlib.pyplot as plt
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")

# lower max_font_size
wordcloud = WordCloud(max_font_size=40).generate(pre_not_science)
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.savefig('not_science_cloud.png')
