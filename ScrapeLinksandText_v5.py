##set parameters - THESE ARE ALL USER DEFINED
web = 4 #how many search engines to include (4 possible- google google scholar bing yahoo)
linkstoget = 50 #number of links to pull from each search engine (this can be any value, but more processing with higher number)

#search terms of interest
searchList = ['GMO','Genetically Modified Organism','Vaccine','Transgenic']
#searchList = ['GMO','Genetically Modified Organism'] #set to whatever, but broken up as to not overload the search
#searchList  = ['Vaccine','Transgenic'] #set to whatever, but broken up as to not overload the search
import sys
import os


#filepath for creating/saving the text files
#FileLocation = '/Users/PMcG/Dropbox (ASU)/AAB_files/Pat-files/WCP/code/Data Files/'
FileLocation = os.getcwd()+str('/')
#if you're switchign computers you can use this to indicate a second location to use if the first doesn't exist
import os
#if not os.path.exists(FileLocation):
#   FileLocaton = 'D:/Dropbox (ASU)/RESEARCH/Pat_Projects/textAnalyze/'

#import web driver file to access chrome and establish a user-agent code
import selenium
#from selenium import webdriver

from pyvirtualdisplay import Display
from selenium import webdriver
import os
import pickle
#import time
import datetime


#driver = webdriver.Chrome(os.getcwd())#'/Users/PMcG/Documents/python packages/chromedriver')
#download driver here: https://sites.google.com/a/chromium.org/chromedriver/downloads
#if you experience an error using driver.get() below make sure chromedriver is up to date

display = Display(visible=0, size=(1024, 768))
display.start()

driver = webdriver.Firefox()
#driver.get('http://www.ubuntu.com/')
#driver.quit()

#assumptions made in the code
#1. any website that returns less than 20 words will not be counted
#2. all website text is in an html or PDF format. Other text will not be counted (haven't found any cases where a third type is present, but do note the constraint here)
#3. all text is encoded to ascii, so any text unreadable by this format is removed

##once the above is set you can run the code!

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

def contents_to_file(strlink):
   if 'pdf' in strlink:
       pdf_file = str(urllib.request.urlopen(strlink).read())
       assert type(pdf_file) is type(str)
       memoryFile = StringIO(pdf_file)
       parser = PDFParser(memoryFile)
       document = PDFDocument(parser)

       # Process all pages in the document
       for page in PDFPage.create_pages(document):
           interpreter.process_page(page)
           write_text =  retstr.getvalue()
       #except:
        #   print('give up on pdf')
   #if not a PDF link
   else:
      #establish human agent header
      headers = {'User-Agent': str(ua.chrome)}
      try:
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
          str_text = str(text)
      except:
          print('reaches exception one')

      #write_text = text.encode('ascii','ignore')
      #try:
      #write contents to file - individual text file for each URL's scraped text
      fileName = searchName  + str(linkcount) + ".p" #create text file save name
      print(fileName, 'filename')
      try:
           print(type(str_text))

           f = open(fileName, 'wb')
           st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
           pickle.dump([st, str_text],f)
      except:
          print('reaches exception two')


for x in range(0,len(searchList)) :
    #define the search term
    category = searchList[x]
    print(" "); print("###############################################")
    print(" "); print(category);  print(" "); print("###############################################")
    categoryquery = category.replace(' ',"+")
    #set path for saving, and make the folder to save if it doesn't already exist
    path = FileLocation + str(category) +'/'
    if not os.path.exists(path):
        os.makedirs(path)
    os.chdir(FileLocation + str(category) +'/')
    for b in range(0,web) :
        time.sleep(randint(1,2)) #shor

        print(" ")
        if b == 0:

            searchName = "google_" #output name for text file
            linkName = "https://www.google.com/search?num=100&filter=0&start=" #search engine web address
            pagestring = linkName + "&q=" + categoryquery # googles
            print("Google")
            driver.get(pagestring)
            continue_link = driver.find_element_by_tag_name('a')
            elem = None
            elem = driver.find_elements_by_xpath("//*[@href]")
            #print(elem)
            linkChecker = [ e for e in elem if "https://www.google.com/search?" in str(e.get_attribute("href")) ]

            strings_to_process = []
            for linko in linkChecker:
                strlink = linko.get_attribute("href")
                strings_to_process.append(linko)
                print(strlink)
            print("\nchecking: " + pagestring + "\n")


        elif b == 1:

            searchName = "gScholar_" #output name for text file
            linkName = "https://scholar.google.com/scholar?hl=en&as_sdt=0%2C3&q="

            pagestring = linkName + "&q=" + categoryquery # googles
            print("Google")
            driver.get(pagestring)
            continue_link = driver.find_element_by_tag_name('a')
            elem = None
            elem = driver.find_elements_by_xpath("//*[@href]")
            linkChecker = []
            linkChecker = [ e for e in elem if "https://scholar.google.com/scholar?" in str(e.get_attribute("href")) ]

            strings_to_process = []
            for linko in linkChecker:
                strlink = linko.get_attribute("href")
                strings_to_process.append(linko)
                print(strlink)
            print("\nchecking: " + pagestring + "\n")
            print("Google Scholar")



        elif b == 2:

            searchName = "bing_" #output name for text file
            linkName = "https://www.bing.com/search?num=100&filter=0&first=" #search engine web address
            pagestring = linkName + "&q=" + categoryquery # googles
            print("Google")
            driver.get(pagestring)
            continue_link = driver.find_element_by_tag_name('a')
            elem = None
            elem = driver.find_elements_by_xpath("//*[@href]")
            linkChecker = [ e for e in elem if "https://www.bing.com/search?q=" in str(e.get_attribute("href")) ]
            #linkChecker = []
            linkChecker = [ strlink for strlink in linkChecker if 'r.bat' not in strlink.get_attribute("href") or 'r.msn' \
             not in strlink.get_attribute("href") or'www.bing.com/news/search' not in strlink.get_attribute("href") ]

            strings_to_process = []
            for linko in linkChecker:
                strlink = linko.get_attribute("href")
                strings_to_process.append(linko)
                print(strlink)
            print("\nchecking: " + pagestring + "\n")
            print("Bing")


        elif b == 3:
            searchName = "yahoo_" #output name for text file
            linkName =  "https://search.yahoo.com/search?p=" #search engine web address
            pagestring = linkName + "&q=" + categoryquery # googles
            print("Google")
            driver.get(pagestring)
            continue_link = driver.find_element_by_tag_name('a')
            elem = None
            elem = driver.find_elements_by_xpath("//*[@href]")
            linkChecker = [ e for e in elem if "http://r.search.yahoo.com/_ylt=" in str(e.get_attribute("href")) ]

            strings_to_process = []
            for linko in linkChecker:
                strlink = linko.get_attribute("href")
                strings_to_process.append(linko)
                print(strlink)
            print("\nchecking: " + pagestring + "\n")

        map(contents_to_file,strings_to_process)

driver.close() #close the driver





'''
while linkcount < linkstoget and checkflag:
    time.sleep(randint(1,2)) #short (random) wait to prevent google from blocking the call

    #finish each web address link in the correct way depending on the search engine




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
               linkcount += 1
               print(str(linkcount) + ". " + str(strlink)) #this is the actual link

               #write the link to the text file containing all URLs
               outfile.write("%s\n" % (strlink))
               import urllib.request

               #if the URL directs to a PDF it requires special coding to pull characters
               if 'pdf' in strlink:
                   ##pdf_file = requests.get(strlink)
                   #pdf_file = urllib2.urlopen(Request(strlink)).read()

                   #  try:
                   pdf_file = str(urllib.request.urlopen(strlink).read())
                   #print(pdf_file)
                   #import pdb; pdb.set_trace()
                   assert type(pdf_file) is type(str)
                   memoryFile = StringIO(pdf_file)
                   parser = PDFParser(memoryFile)
                   document = PDFDocument(parser)

                   # Process all pages in the document
                   for page in PDFPage.create_pages(document):
                       interpreter.process_page(page)
                       write_text =  retstr.getvalue()
                   #except:
                    #   print('give up on pdf')
               #if not a PDF link
               else:
                  #establish human agent header
                  headers = {'User-Agent': str(ua.chrome)}
                  try:
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
                      str_text = str(text)
                  except:
                      print(None)

                  #write_text = text.encode('ascii','ignore')
                  #try:
                  #write contents to file - individual text file for each URL's scraped text
                  fileName = searchName  + str(linkcount) + ".p" #create text file save name
                  print(fileName, 'filename')
                  try:
                       print(type(str_text))

                       f = open(fileName, 'wb')
                       #f.write(str(write_text))
                       pickle.dump(str_text,f)
                  except:
                       print(None)
                   #f.close()
                   #f = None

    if prevlinkcount == linkcount:
        checkflag = 0
    else:
        prevlinkcount = linkcount

outfile.close() #close the text file containing list of URLs per search engine
'''
#close chrome after looping through the various search engines
