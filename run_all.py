#from multiprocessing import Process
#!/usr/bin/env python

"""A basic fork in action"""

import os

def my_fork():
    child_pid = os.fork()
    if child_pid == 0:
        print("Child Process: PID# %s" % os.getpid(),'scrape links and text')
        import sclata

    else:
        print("Parent Process: PID# %s" % os.getpid(),'tAnalysis')
        import t_analysis


if __name__ == "__main__":
    import sclat
    import t_analysis

    #uncomment my fork to do both modules at the same time.
    #my_fork()
