#call in necessary packages that code requires to operate and define additional vars
import requests
from bs4 import BeautifulSoup
import openpyxl
import os
import re

##################################################
##################################################

#define number of loop iterations (i.e. how many links to analyze)
num = 26 #how many links + 1

#load working directory for file saving of files containing the URL text
#os.chdir('D:/Dropbox (ASU)/RESEARCH/Pat_Projects/textAnalyze/'+ str(term) +'/')
os.chdir('/Users/PMcG/Dropbox (ASU)/AAB_files/Pat-files/WCP/code/Data Files/'+ str(term) +'/')

searchList = 'SearchTerms.txt' #list of terms to search
linkstoget = 2 #number of links to pull from search
web = 2 #how many search engines to include

##################################################
for b in range(0,web) :

    if b == 0:
        textName = "google_"
        print "Google"
        
    elif b == 1:
        textName = "gScholar_"
        print "Google Scholar"
        
    elif b == 2:
        textName = "bing_"
        print "Bing"

for x in range (1,num):

    urlReady =   

    #verify URL is correct and ready to be accessed via web server
    print x
    print urlReady

    bing.cell(row = x, column = 2).value = urlReady
       
    #access web server and retrieve web content
    url = urlReady
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    #strip HTML scripting and style
    for script in soup(["script", "style"]):
            script.extract()    # rip it out

    #clean up the text
    # get text
    text = soup.get_text()
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)

    #write contents to file
    write_text = text.encode('ascii','ignore')

    fileName = "bing_"  + str(x) + ".txt"
    f = open(fileName, 'w');

    f.write(write_text)
    f.close()



