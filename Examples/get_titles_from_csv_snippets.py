import os
import csv
import glob
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

import numpy as np
import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans
from sklearn import datasets
import seaborn as sns; sns.set()  # for plot styling

import pickle
from SComplexity.analysis import Analysis
import pandas as pd

from habanero import Crossref
cr = Crossref()
#from habanero import Crossref
#[ z['DOI'] for z in x['message']['items'] ]
#[ z['issn'] for z in x['message']['items'] ]


#cr = Crossref()
##
# This file can be used to show, that K-Means clustering
# a type of unsupervised classifier, can predict if something is a wikipedia article
# or not pretty well.
# It's my opinion that, the classifier could probably predict mainstream science or psuedo science too,
# given enough dimensions to seperate the clustered data points over.
##

FILES = natsorted(glob.glob(str(os.getcwd())+'/*.csv'))
contents = []
titles = {}
for csvfile in FILES:
     with open(csvfile, 'rt') as csvfile:
         #spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
         contents.append(csv.reader(csvfile))
         for row in contents[-1]:
              
              #if 'title' in row:
              print(row[-2])
              titles[row[-2]] = row[-2]
         #print(contents[-1])
