#human parameters to set
searchList = ['GMO'] #,'Genetically Modified Organism','Transgenic','Vaccine']
web = 1 #number of search websites being implemented (google, google scholar, bing, yahoo)
numURLs = 1 #number of URLs per search website (number determined by 1.scrape code)

#crawler input
linkstoget = 20 #number of links to crawl through per URL - be careful with this number

#make sure you set the filepath below to set data location

#########################################################################
#########################################################################
#load in required python functions
from bs4 import BeautifulSoup
import requests
from random import randint
import os
import numpy
import numpy as np
import scipy.io as sio
from fake_useragent import UserAgent

ua = UserAgent()
#########################################################################
#########################################################################
#start code
for s in range(0,len(searchList)) :

    #define the search term
    category = searchList[s]

    print " "; print "###############################################"
    print " "; print category;  print " "; print "###############################################"
    
    #set path for saving, and make the folder to save if it doesn't already exist
    os.chdir('/Users/PMcG/Dropbox (ASU)/AAB_files/Pat-files/WCP/code/Data Files/'+ str(category) +'/')
    
    for b in range(0,web) :
        #set scrape parameters
        print " "
        if b == 0:
            searchName = "google_" #ouput name for text file
            print "Google"
            
        elif b == 1:
            searchName = "gScholar_" #ouput name for text file
            print "Google Scholar"
            
        elif b == 2:
            searchName = "bing_" #ouput name for text file
            print "Bing"

        elif b == 3:
            searchName = "yahoo_" #ouput name for text file
            print "Yahoo"          

        print "--------------------"

        #open text file
        filename = searchName + category + '.txt' #text file name that will list and save all URLs
        infile = open(filename, 'r')
        URL = infile.readlines()

        for u in range(0,numURLs) :
            url = URL[u]
            #url = 'http://www.pmcgurrin.com/popularscience/'

            r  = requests.get(url)
            data = r.text
            soup = BeautifulSoup(data, 'html.parser')

            linkcount = 0
            pageURLs = {}
            LinkLocation = {}

            for link in soup.find_all('a'):
                if linkcount < linkstoget:
                    pageURLs[linkcount+1] = link.get('href')

                    if pageURLs[linkcount+1] is None or str(pageURLs[linkcount+1]) == '/':
                        continue
                        
                    elif 'http' in pageURLs[linkcount+1]:
                        print pageURLs[linkcount+1] + ': external link'
                        LinkLocation[linkcount+1]  = 1
                        linkcount += 1
                    else:
                        print pageURLs[linkcount+1] + ': internal link'
                        LinkLocation[linkcount+1]  = 0
                        linkcount += 1

            ##        #establish human agent header
            ##        time.sleep(randint(1,2)) #short (random) wait to prevent google from blocking the call
            ##        headers = {'User-Agent': str(ua.chrome)}
            ##
            ##        #request website data using beautiful soup
            ##        r = requests.get(strlink, headers=headers)
            ##        soup = BeautifulSoup(r.content, 'html.parser')
            ##
            ##        #strip HTML 
            ##        for script in soup(["script", "style"]):
            ##                script.extract()    # rip it out
            ##
            ##        # get text
            ##        text = soup.get_text()
            ##
            ##        #organize text
            ##        lines = (line.strip() for line in text.splitlines())  # break into lines and remove leading and trailing space on each
            ##        chunks = (phrase.strip() for line in lines for phrase in line.split("  ")) # break multi-headlines into a line each
            ##        text = '\n'.join(chunk for chunk in chunks if chunk) # drop blank lines
            ##        url_text = text.replace("-", " ")
            ##
            ##        urlDat = {}
            ##        #perform a subset of the text analysis
            ##        urlDat[6,2]  = textstat.flesch_kincaid_grade(str(url_text))        
            ##        urlDat[7,2] = textstat.flesch_reading_ease(str(url_text))
            ##        urlDat[8,2]  = textstat.smog_index(str(url_text))    
            ##        urlDat[9,2]  = textstat.coleman_liau_index(str(url_text))
            ##        urlDat[10,2]  = textstat.automated_readability_index(str(url_text))
            ##        urlDat[11,2] = textstat.gunning_fog(str(url_text))
            ##
            ##        urlDat[12,2]  = textstat.dale_chall_readability_score(str(url_text))
            ##        urlDat[13,2]  = textstat.difficult_words(str(url_text))
            ##        urlDat[14,2]  = textstat.linsear_write_formula(str(url_text)) 
            ##        urlDat[15,2]  = textstat.text_standard(str(url_text))
            ##
            ##        urlDat = urlDat.items()
            ##
            ##        ##generate a .mat file for further analysis in matlab
            ##        if b == 0 and p == 0:
            ##            obj_arr = np.array([urlDat,WperS, sentSyl, fM, PS, fAll], dtype=object)
            ##        else:
            ##            obj_arr_add = np.array([urlDat,WperS, sentSyl, fM, PS, fAll], dtype=object)
            ##            obj_arr = np.vstack( [obj_arr, obj_arr_add] )
            ##
            ##    #after the full code runs export to a .mat file so I know what the heck I'm doing for analysis
            ##    try:
            ##        os.chdir('/Users/PMcG/Dropbox (ASU)/AAB_files/Pat-files/WCP/code/Data Files/')
            ##    except:
            ##        os.chdir('D:/Dropbox (ASU)/RESEARCH/Pat_Projects/textAnalyze/')
            ##
            ##    #save
            ##    sio.savemat('crawlData_' + str(searchList[s]) + '.mat', {'obj_arr':obj_arr})
                    
            

