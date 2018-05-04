
import dask
from utils_and_parameters import search_params, engine_dict_list
SEARCHLIST, WEB, LINKSTOGET = search_params()
se, _ = engine_dict_list()
import utils
from numpy import random
flat_iter = [ (b,category) for category in SEARCHLIST for b in range(0,5) ]

# Traverse web pages randomly to feign human hood.
random.shuffle(flat_iter)
import time
random.shuffle(flat_iter)
random.shuffle(flat_iter)
print(flat_iter)
import utils
import os
from utils import map_wrapper
def scraplandtext(fi):
    b,category = fi
    if b==4:

        exec_string='python run.py --keyword '+'"'+str('!scholar ')+str(category)+'"'+' --search-engines=duckduckgo'+' -p=15 --output-filename '+'"'+str(category)+'_'+str('scholar')+'.csv'+'"'
    else:
        exec_string='python run.py --keyword '+'"'+str(category)+'"'+' --search-engines='+str(se[b])+' -p=15 --output-filename '+'"'+str(category)+'_'+str(se[b])+'.csv'+'"'
    print(exec_string)
    os.system(exec_string)
_ = list(map(scraplandtext,flat_iter))
