from selenium import webdriver
import os
##set parameters - THESE ARE ALL USER DEFINED
web = 3 #how many search engines to include (4 possible- google google scholar bing yahoo)
linkstoget = 15 #number of links to pull from each search engine (this can be any value, but more processing with higher number)

#search terms of interest
searchList = ['GMO'] #,'Genetically Modified Organism','Transgenic','Vaccine'] #set to whatever

#filepath for creating/saving the text files
FileLocation = '/Users/PMcG/Dropbox (ASU)/AAB_files/Pat-files/WCP/code/Data Files/'

#if you're switchign computers you can use this to indicate a second location to use if the first doesn't exist
if not os.path.exists(FileLocation):
   FileLocaton = 'D:/Dropbox (ASU)/RESEARCH/Pat_Projects/textAnalyze/'

#import web driver file to access chrome and establish a user-agent code
driver = webdriver.Chrome('/Users/PMcG/Documents/python packages/chromedriver')
#download driver here: https://sites.google.com/a/chromium.org/chromedriver/downloads
#if you experience an error using driver.get() below make sure chromedriver is up to date

##########################################################################
##########################################################################
#import necessary python packages
from bs4 import BeautifulSoup
import time
import shutil
import requests
from random import randint

from fake_useragent import UserAgent
ua = UserAgent()
##########################################################################
##########################################################################
#start code
for x in range(0,len(searchList)) :

    #define the search term
    category = searchList[x]
    print " "; print "###############################################"
    print " "; print category;  print " "; print "###############################################"
    
    categoryquery = category.replace(' ',"+")

    #set path for saving, and make the folder to save if it doesn't already exist
    path = FileLocation + str(category) +'/'
    if not os.path.exists(path):
        os.makedirs(path)

    os.chdir(FileLocation + str(category) +'/')
    
    for b in range(0,web) :
        #set scrape parameters
        print " "
        if b == 0:
            searchName = "google_" #output name for text file
            linkName = "https://www.google.com/search?num=100&filter=0&start=" #search engine web address
            linkCheck1 = "//div[@class='srg']/div[@class='g']/div[@class='rc']/h3[@class='r']/a" #HTML syntax where links are stored
            linkCheck2 = "//div[@id='rso']/div[@class='g']/div[@class='rc']/h3[@class='r']/a" #HTML syntax where links are stored
            print "Google"
            
        elif b == 1:
            searchName = "gScholar_" #output name for text file
            linkName = "https://www.scholar.google.com/scholar?num=100&filter=0&start=" #search engine web address
            linkCheck1 = "//div[@class='gs_r']/div[@class='gs_ri']/h3[@class='gs_rt']/a" #HTML syntax where links are stored
            linkCheck2 = "//div[@class='gs_r']/div[@class='gs_ri']/h3[@class='gs_rt']/a" #HTML syntax where links are stored
            print "Google Scholar"
            
        elif b == 2:
            searchName = "bing_" #output name for text file
            linkName = "https://www.bing.com/search?num=100&filter=0&start=" #search engine web address
            linkCheck1 = "//h2/a" #HTML syntax where links are stored
            linkCheck2 = "//h2/a" #HTML syntax where links are stored
            print "Bing"

        elif b == 3:
            searchName = "yahoo_" #output name for text file
            linkName =  "http://search.yahoo.com/search?p=" #search engine web address
            linkCheck1 = "//a[@class=' ac-algo ac-21th lh-24']" #HTML syntax where links are stored
            linkCheck2 = "//a[@class=' ac-algo ac-21th lh-24']" #HTML syntax where links are stored
            print "Yahoo"          

        print "--------------------"
        #create a text file with Search term name and open the text file 
        ofilename = searchName + category + '.txt' #text file name that will list and save all URLs
        outfile = open(ofilename, 'w')

        linkcount = 0
        checkflag = 1
        prevlinkcount= -1

        while linkcount < linkstoget and checkflag:
            
            time.sleep(randint(1,2)) #short (random) wait to prevent google from blocking the call
            if b == 3:
                pagestring = linkName + categoryquery #yahoo
            else:
                pagestring = linkName + str(linkcount + 1) + "&q=" + categoryquery #all other engines

            #print "\nchecking: " + pagestring + "\n"               
            driver.get(pagestring)

            #print driver.page_source
            searchresults = {}
            linkChecker = list()

            #locate URLs within specific search engine HTML syntax
            linkChecker1 = driver.find_elements_by_xpath(linkCheck1)
            linkChecker2 = driver.find_elements_by_xpath(linkCheck2)

            for l in linkChecker1:
                linkChecker.append(l)
            for l in linkChecker2:
                linkChecker.append(l)

            for linko in linkChecker:
                if linkcount < linkstoget:
                    strlink = ""
                    try:
                        # print link to text
                        linkcount += 1
                        strlink = linko.get_attribute("href")
                    except:
                        print "fail"
 
                    print str(linkcount) + ". " + str(strlink) #this is the actual link

                    #write the link to the text file containing all URLs
                    outfile.write("%s\n" % (strlink)) 

                    #establish human agent header
                    headers = {'User-Agent': str(ua.chrome)}

                    #request website data using beautiful soup
                    r = requests.get(strlink, headers=headers)
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

                    #write contents to file - individual text file for each URL's scraped text
                    write_text = text.encode('ascii','ignore')
                    fileName = searchName  + str(linkcount) + ".txt" #create text file save name
                    f = open(fileName, 'w')
                    f.write(write_text)
                    f.close()

            if prevlinkcount == linkcount:
                checkflag = 0
            else:
                prevlinkcount = linkcount
      
        outfile.close() #close the text file containing list of URLs per search engine

#close chrome after looping through the various search engines
driver.close() #close the driver
