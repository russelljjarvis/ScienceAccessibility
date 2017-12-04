##set parameters - THESE ARE ALL USER DEFINED
web = 2 #how many search engines to include (4 possible- google google scholar bing yahoo)
linkstoget = 50 #number of links to pull from each search engine (this can be any value, but more processing with higher number)

#search terms of interest
searchList = ['GMO','Genetically Modified Organism','Vaccine','Transgenic']
#searchList = ['GMO','Genetically Modified Organism'] #set to whatever, but broken up as to not overload the search
#searchList  = ['Vaccine','Transgenic'] #set to whatever, but broken up as to not overload the search
import sys
import os


#filepath for creating/saving the text files
FileLocation = 'AAB_files/Pat-files/WCP/code/Data Files/'

#if you're switchign computers you can use this to indicate a second location to use if the first doesn't exist
import os
if not os.path.exists(FileLocation):
   FileLocaton = 'RESEARCH/Pat_Projects/textAnalyze/'

#import web driver file to access chrome and establish a user-agent code
import selenium
from selenium import webdriver


from pyvirtualdisplay import Display
from selenium import webdriver

display = Display(visible=0, size=(1024, 768))
display.start()

driver = webdriver.Firefox()
driver.get('http://www.ubuntu.com/')


#assumptions made in the code
#1. any website that returns less than 20 words will not be counted
#2. all website text is in an html or PDF format. Other text will not be counted (haven't found any cases where a third type is present, but do note the constraint here)
#3. all text is encoded to ascii, so any text unreadable by this format is removed

##once the above is set you can run the code!
#if any errors arise it may be due to:
#if you experience an error using driver.get() below make sure chromedriver is up to date
#if you experience an error using any of the installed functions/packages they likely need updated
#if you receive a message that the code was terminated by peer, it likely means you've crawled too much in a short time. Wait a few hours and re-run code

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

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

try:
   import urllib3
   from urllib3 import Request
except ImportError:
   import urllib3.request

try:
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
except ImportError:
   pass

from textstat.textstat import textstat
##########################################################################
##########################################################################
#start code


for x,category in enumerate(searchList):

    #define the search term
    #category = searchList[x]
    print(" "); print("###############################################")
    print(" "); print(category);  print(" "); print("###############################################")

    categoryquery = category.replace(' ',"+")

    #set path for saving, and make the folder to save if it doesn't already exist
    path = FileLocation + str(category) +'/'
    if not os.path.exists(path):
        os.makedirs(path)

    os.chdir(FileLocation + str(category) +'/')
    web = ["google_","gScholar_","bing_","yahoo_"]

    flattening = [ (b,searchName) for b, searchName in enumerate(web)  ]

    for b, searchName in flattening:
        print(" ")
        if b == 0:
            #searchName = "google_" #output name for text file
            linkName = "https://www.google.com/search?num=100&filter=0&start=" #search engine web address
            linkCheck1 = "//div[@class='srg']/div[@class='g']/div[@class='rc']/h3[@class='r']/a" #HTML syntax where links are stored
            linkCheck2 = "//div[@id='rso']/div[@class='g']/div[@class='rc']/h3[@class='r']/a" #HTML syntax where links are stored
            print("Google")

        elif b == 1:
            #searchName = "gScholar_" #output name for text file
            linkName = "https://www.scholar.google.com/scholar?num=100&filter=0&start=" #search engine web address
            linkCheck1 = "//div[@class='gs_r']/div[@class='gs_ri']/h3[@class='gs_rt']/a" #HTML syntax where links are stored
            linkCheck2 = "//div[@class='gs_r']/div[@class='gs_ri']/h3[@class='gs_rt']/a" #HTML syntax where links are stored
            print("Google Scholar")

        elif b == 2:
            #searchName = "bing_" #output name for text file
            linkName = "https://www.bing.com/search?num=100&filter=0&first=" #search engine web address
            linkCheck1 = "//h2/a" #HTML syntax where links are stored
            linkCheck2 = "//h2/a" #HTML syntax where links are stored
            print("Bing")

        elif b == 3:
            #searchName = "yahoo_" #output name for text file
            linkName =  "https://search.yahoo.com/search?p=" #search engine web address
            linkCheck1 = "//a[@class=' ac-algo ac-21th lh-24']" #HTML syntax where links are stored
            linkCheck2 = "//a[@class=' ac-algo ac-21th lh-24']" #HTML syntax where links are stored
            print("Yahoo")

        print ("--------------------")
        #create a text file with Search term name and open the text file
        ofilename = searchName + category + '.txt' #text file name that will list and save all URLs
        outfile = open(ofilename, 'w')

        linkcount = 0
        checkflag = 1
        prevlinkcount= -1

        while linkcount < linkstoget and checkflag:
            time.sleep(randint(1,2)) #short (random) wait to prevent google from blocking the call

            #finish each web address link in the correct way depending on the search engine
            if b == 2:
                pagestring = linkName + str(linkcount + 1) + "&q=" + categoryquery #bing
            elif b == 3:
                pagestring = linkName + categoryquery + "&pstart=" + str(linkcount + 1) #yahoo
            else:
                pagestring = linkName + str(linkcount + 1) + "&q=" + categoryquery # googles

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
                        strlink = linko.get_attribute("href")
                    except:
                        print("fail")

                #sometimes bing pulls in weird ads with the href tag. this ignores those and doesn't count them against the link count
                if 'r.bat' in strlink or 'r.msn' in strlink or 'www.bing.com/news/search' in strlink:
                   linkcount +=0

                    else:
                       #if  URL directs to a PDF it requires special coding to pull characters
                       try:
                          pdf_file = urllib3.urlopen(Request(strlink)).read()
                          memoryFile = StringIO(pdf_file)
                          parser = PDFParser(memoryFile)
                          document = PDFDocument(parser)

                          #Process all pages in the document
                          for page in PDFPage.create_pages(document):
                             interpreter.process_page(page)
                             write_text =  retstr.getvalue()

                   #if not a PDF link try fails the exception treats it like a non-PDF document
                   except:
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
                      write_text = text.encode('ascii','ignore')


                       else:
                          #if there is text, print the URL & save the URL/text to file for further analysis
                          linkcount += 1
                         #print the link to the command window
                          print (str(linkcount) + ". " + str(strlink)) #this is the actual link

                          #write the link to the text file containing all URLs
                          outfile.write("%s\n" % (strlink))

                          #write contents to individual textfile
                          fileName = searchName  + str(linkcount) + ".txt"
                          f = open(fileName, 'w')
                          f.write(str(write_text))
                          f.close()
            except:
                None
            if prevlinkcount == linkcount:
                checkflag = 0
            else:
                prevlinkcount = linkcount

        outfile.close() #close the text file containing list of URLs per search engine
    driver.quit() # Quit the driver and close every associated window.
    display.stop()

#close chrome after looping through the various search engines
driver.close() #close the driver
