##set parameters - THESE ARE ALL USER DEFINED
web = 4 #how many search engines to include (4 possible- google google scholar bing yahoo)
linkstoget = 50 #number of links to pull from each search engine (this can be any value, but more processing with higher number)

#search terms of interest
searchList = ['GMO','Genetically_Modified_Organism','Vaccine','Transgenic']
import sys
import os


fileLocation = os.getcwd()#+str('/')
#if you're switchign computers you can use this to indicate a second location to use if the first doesn't exist
import os
#if not os.path.exists(FileLocation):
#import web driver file to access chrome and establish a user-agent code
import selenium

from pyvirtualdisplay import Display
from selenium import webdriver
import os
import pickle
import time
import datetime

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

def check_for_self_referencing(list_of_links):
   from urllib.parse import urlparse
   print(list_of_links[0])
   print(list_of_links[0].get_attribute("href"))

   baseURLtemp= urlparse(list_of_links[0].get_attribute("href"))
   #  baseURL = str(baseURLtemp[0] + "://" + baseURLtemp[1])
   baseURL = str(baseURLtemp[0] + "://" + baseURLtemp[1])
   for i in list_of_links[1:-1]:
       if baseURL in i:
           print(baseURL,i)
           print('internal link')
       if baseURL not in i:
           print(baseURL,i)
           print('external link')
   return list_of_links

def contents_to_file(strlink):
   #import pdb; pdb.set_trace()

   if 'pdf' in strlink:
       pdf_file = str(urllib.request.urlopen(strlink).read())
       assert type(pdf_file) is type(str)
       memoryFile = StringIO(pdf_file)
       parser = PDFParser(memoryFile)
       document = PDFDocument(parser)

       # Process all pages in the document
       for page in PDFPage.create_pages(document):
           interpreter.process_page(page)
           write_text +=  retstr.getvalue()


       str_text = str(write_text)
       fileName = searchName + ".p" #create text file save name
       print(fileName, 'filename')
       #try:
       print(type(str_text))
       f = open(fileName, 'wb')
      # ts = datetime.now()
       #d = datetime.now()
       #st = str(d.strftime('%m/%d/%Y_%H:%M:%S'))
       from datetime import datetime
       st = datetime.utcnow().strftime('%Y-%m-%d_%H:%M:%S.%f')[:-3]

       pickle.dump([st, str_text],f)

   else:
      #establish human agent header
      headers = {'User-Agent': str(ua.chrome)}
      #try:
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

      fileName = searchName + ".p" #create text file save name
      print(fileName, 'filename')
      #try:
      print(type(str_text))

      f = open(fileName, 'wb')
      #d = datetime.now()
      from datetime import datetime
      st = datetime.utcnow().strftime('%Y-%m-%d_%H:%M:%S.%f')[:-3]
      #st = str(d.strftime('%m/%d/%Y_%H:%M:%S'))
      pickle.dump([st, str_text],f)
   return None



for x, category in enumerate(searchList):
    #define the search term
    #category = sl
    print(" "); print("###############################################")
    print(" "); print(category);  print(" "); print("###############################################")
    categoryquery = category.replace(' ',"+")
    #set path for saving, and make the folder to save if it doesn't already exist
    path = fileLocation + '/' +  str(category) +'/'
    if not os.path.exists(path):
        os.makedirs(path)
    os.chdir(fileLocation + '/' +  str(category) +'/')
    '''
    if not os.path.exists(str(fileLocation) + '/' + str(value) +'/'):
        os.makedirs(str(fileLocation) + '/' + str(value) +'/')
    os.chdir(fileLocation +str('/') + str(value) +'/')
    '''
    for b in range(0,web):
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
                strings_to_process.append(strlink)
                print(strlink)
            #print("\nchecking: " + pagestring + "\n")


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
                strings_to_process.append(strlink)
                print(strlink)
            #print("\nchecking: " + pagestring + "\n")
            print("Google Scholar")



        elif b == 2:

            searchName = "bing_" #output name for text file
            linkName = "https://www.bing.com/search?num=100&filter=0&first=" #search engine web address
            pagestring = linkName + "&q=" + categoryquery # googles
            #print("Google")
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
                strings_to_process.append(strlink)
                print(strlink)
            #print("\nchecking: " + pagestring + "\n")
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
                strings_to_process.append(strlink)
                print(strlink)

        null = list(map(contents_to_file,strings_to_process))

driver.close() #close the driver
