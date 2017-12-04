#set parameters- THESE ARE ALL USER DEFINED
searchList = ['GMO'] #'Genetically Modified Organism','Transgenic','Vaccine']
web = 2 #number of search websites being implemented (google, google scholar, bing, yahoo)
numURLs = 2 #number of URLs per search website (number determined by 1.scrape code)

#crawler input
linkstoget = 3 #number of links to crawl through per URL - be careful with this number, as it greatly increases computation time
#searchList = ['GMO','Genetically Modified Organism','Transgenic','Vaccine']

#set filePath below to specify where the text Data is located on your machine
fileLocation = 'AAB_files/Pat-files/WCP/code/Data Files/'

#if you're switchign computers you can use this to indicate a second location to use if the first doesn't exist
import os
if not os.path.exists(FileLocation):
   fileLocaton = 'RESEARCH/Pat_Projects/textAnalyze/'

##once the above is set you can run the code!


#########################################################################
#########################################################################
#load in required python functions
from bs4 import BeautifulSoup
import requests
from random import randint
import numpy
import numpy as np
import scipy.io as sio
from urllib.parse import urlparse
#from urlparse import urlparse
from urllib.request import Request
import time
from textstat.textstat import textstat
import urllib

from io import StringIO

#from urllib import Request
#from StringIO import StringIO
from fake_useragent import UserAgent
ua = UserAgent()

import pdfminer
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams
from pdfminer.converter import  TextConverter
rsrcmgr = PDFResourceManager()
retstr = StringIO()
laparams = LAParams()
codec = 'utf-8'
device = TextConverter(rsrcmgr, retstr, codec = codec, laparams = laparams)
interpreter = PDFPageInterpreter(rsrcmgr, device)
#########################################################################
#########################################################################
#start code
#for s in range(0,len(searchList)) :

#import os
for s,category in enumerate(searchList):


    #define the search term
    category = searchList[s]

    print (" "); print ("###############################################")
    print (" "); print(category);  print (" "); print ("######(#########################################")

    #set path for saving, and make the folder to save if it doesn't already exist
    os.chdir(fileLocation + str(category) +'/')
    #if not os.path.exists(directory):
    #    os.makedirs(directory)
    print(os.getcwd())


    web = ["bing_","yahoo_","google_","gScholar_"]
    for b, searchName in enumerate(web):
        #set scrape parameters
        print(searchName)
        '''
        #set scrape parameters
        print " "
        if b == 0:
        searchName = "google_" #input name for text file
        print ("Google")

        elif b == 1:
        searchName = "gScholar_" #input name for text file
        print ("Google Scholar")

        elif b == 2:
        searchName = "bing_" #input name for text file
        print ("Bing")

        elif b == 3:
        searchName = "yahoo_" #input name for text file
        print ("Yahoo")
        '''
        #open text file
        filename = searchName + category + '.txt' #text file name that will list and save all URLs
        infile = open(filename, 'r')
        URL = infile.readlines()

        for u in range(0,numURLs) :

            url = URL[u]
            print( ""); print "-------------"; print ("URL " + str(u+1) + " of " + str(numURLs));
            print ("Link to crawl: " + url); print ("");  print ("Linked crawled:)"

            #request content from URL
            headers = {'User-Agent': str(ua.chrome)}
            r  = requests.get(url, headers=headers)
            data = r.text
            soup = BeautifulSoup(data, 'html.parser')

            #initialize some vars
            linkcount = 0
            pageURLs = {}
            baseURLtemp = {}
            baseURL = {}
            #retrieve base URL for use below in concatenating internal links
            baseURLtemp= urlparse(url)
            baseURL = str(baseURLtemp[0] + "://" + baseURLtemp[1])


            #initialize dataArray
            urlDat = {}
            urlDat[1,1] = 'Link location' #internal or external
            urlDat[2,1] = "Number of Words"
            urlDat[3,1] = "Grade level"
            urlDat[4,1] = "Flesch Reading Ease"
            urlDat[5,1] = "SMOG Index"
            urlDat[6,1] = "Coleman Liau"
            urlDat[7,1] = "Automated Readability Index"
            urlDat[8,1] = "Gunning Fog"
            urlDat[9,1] = "Dale Chall Readability Score"
            urlDat[10,1] = "Difficult Words"
            urlDat[11,1] = "Linsear Write Formula"
            urlDat[12,1] = "Text Standard"
            urlDat[13,1] = "Link scraped"

            #crawl through n number of links for each URL
            for linkcount, link in enumerate(soup.find_all('a')):
                if linkcount < linkstoget:
                    time.sleep(randint(1,2)) #short (random) wait to prevent overloading a website or having the call blocked

                    pageURLs[linkcount+1] = link.get('href')

                    if pageURLs[linkcount+1] is None or str(pageURLs[linkcount+1]) == '/' or str(pageURLs[linkcount+1]).startswith('#') or 'ad.doubleclick' in pageURLs[linkcount+1]:
                        continue

                    #external link and no correction needed
                    elif 'http' in pageURLs[linkcount+1] and baseURL not in pageURLs[linkcount+1] :
                        print (pageURLs[linkcount+1] + " --- External link")
                        urlDat[1,linkcount+2] = 1
                        urlDat[13,linkcount+2] = pageURLs[linkcount+1]

                    #internal link that doesn't need correction
                    elif baseURL in pageURLs[linkcount+1]:
                        print (pageURLs[linkcount+1] + " --- Internal link")
                        urlDat[1,linkcount+2]  = 0
                        urlDat[13,linkcount+2] = pageURLs[linkcount+1]

                    #internal link that is missing the baseURL info - link is corrected
                    else:
                        linkFix = baseURL + pageURLs[linkcount+1]
                        print (pageURLs[linkcount+1] + " --- Internal link, corrected: " + linkFix)
                        urlDat[1,linkcount+2]  = 0
                        urlDat[13,linkcount+2] = linkFix

                    #get that text!
                   #if the URL directs to a PDF it requires special coding to pull characters
                    try:
                        ##pdf_file = requests.get(strlink)
                        pdf_file = urllib2.urlopen(Request(urlDat[13,linkcount+2])).read()
                        memoryFile = StringIO(pdf_file)
                        parser = PDFParser(memoryFile)
                        document = PDFDocument(parser)

                        # Process all pages in the document
                        for page in PDFPage.create_pages(document):
                            interpreter.process_page(page)
                            url_text =  retstr.getvalue()

                    #if not a PDF link
                    except:
                       #establish human agent header
                       headers = {'User-Agent': str(ua.chrome)}

                       #request website data using beautiful soup
                       r = requests.get(urlDat[13,linkcount+2], headers=headers)
                       soup = BeautifulSoup(r.content, 'html.parser')

                       #strip HTML
                       for script in soup(["script", "style"]):
                               script.extract()    # rip it out

                       # get text
                       text = soup.get_text()

                       #organize text
                       lines = (line.strip() for line in text.splitlines())  # break into lines and remove leading and trailing space on each
                       chunks = (phrase.strip() for line in lines for phrase in line.split("  ")) # break multi-headlines into a line each
                       text = '\n'.join(chunk for chunk in chunks if chunk) # drop blank lines
                       url_text = text.encode('ascii','ignore')

                    #perform a subset of the text analysis
                    urlDat[2,linkcount+2] = textstat.lexicon_count(str(url_text))
                    urlDat[3,linkcount+2]  = textstat.flesch_kincaid_grade(str(url_text))
                    urlDat[4,linkcount+2] = textstat.flesch_reading_ease(str(url_text))
                    urlDat[5,linkcount+2]  = textstat.smog_index(str(url_text))
                    urlDat[6,linkcount+2]  = textstat.coleman_liau_index(str(url_text))
                    urlDat[7,linkcount+2]  = textstat.automated_readability_index(str(url_text))
                    urlDat[8,linkcount+2] = textstat.gunning_fog(str(url_text))
                    urlDat[9,linkcount+2]  = textstat.dale_chall_readability_score(str(url_text))
                    urlDat[10,linkcount+2]  = textstat.difficult_words(str(url_text))
                    urlDat[11,linkcount+2]  = textstat.linsear_write_formula(str(url_text))
                    urlDat[12,linkcount+2]  = textstat.text_standard(str(url_text))

                    #linkcount += 1

            ##generate a .mat file for further analysis in matlab
			#
			# Bug fix
			#
			urlDat = list(urlDat.items())
            if b == 0 and u == 0:
               obj_arr = np.array([urlDat], dtype=object)
            else:
               obj_arr_add = np.array([urlDat], dtype=object)
               obj_arr = np.vstack( [obj_arr, obj_arr_add])

    #after the full code runs export to a .mat file so I know what the heck I'm doing for analysis
    os.chdir(FileLocation)

    #save
    sio.savemat('crawlData_' + str(searchList[s]) + '.mat', {'obj_arr':obj_arr})
