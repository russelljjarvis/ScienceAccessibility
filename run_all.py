#from multiprocessing import Process
#!/usr/bin/env python

"""A basic fork in action"""

import os

def my_fork():
    child_pid = os.fork()
    if child_pid == 0:
        print("Child Process: PID# %s" % os.getpid(),'scrape links and text')
        import sclat

    else:
        print("Parent Process: PID# %s" % os.getpid(),'tAnalysis')
        import t_analysis_purepy


if __name__ == "__main__":
    #my_fork()
    import sclat
    import t_analysis_purepy
    import dask.bag as db
    from t_analysis_purepy import web_iter, map_wrapper
    QUERY_LIST = ['GMO','Genetically_Modified_Organism','Transgenic','Vaccine', 'Neutron', 'Play Dough']
    list_per_links = map_wrapper(web_iter,QUERY_LIST) 
    remove_empty = [i for i in list_per_links if len(i)>0 ]
    unravel = []
    for i in remove_empty:
        unravel+=i
    with open('unraveled_links.p','wb') as handle:
        pickle.dump(unravel,handle)
    #uncomment my fork to do both modules at the same time.
    
