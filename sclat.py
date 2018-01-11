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

def csr(text,strlink):
   '''
   # This method compares a new link with an old link. We want to know when websites reference themselves (self reference).
   # One way of doing this is to see if a substring constituted by the referal website (URL basename) can be found in the link string.
   # inputs: text on referal website (including links):
   # strlink links to external websites (projections)
   # outputs boolean flag
   '''
   driver.get(strlink)
   continue_link = driver.find_element_by_tag_name('a')
   links_from_external_projection = None
   links_from_external_projection = driver.find_elements_by_xpath("//*[@href]")
   links = []
   for e in links_from_external_projection:
       links.append(str(e.get_attribute("href")))

   from urllib.parse import urlparse
   print(strlink)
   baseURLtemp = urlparse(strlink)
   baseURL = str(baseURLtemp[0] + "://" + baseURLtemp[1])
   if strlink in text:
       print('probably links to self')
       print(strlink,text)
   for l in links:
       if str(baseURL) in str(l):
           return True
   return False



def contents_to_file(contents):
   '''
   visit links if the link expands into HTML, convert to string using Beautiful Soup,
   if it expands to a PDF use appropriate tools to extract string from PDF.
   Write files (pickle), with a time stamp when the file was created.
   '''
   incrementor, strlink, searchName = contents
   print(strlink,incrementor, ' pacifier')


   # uncommonet lines below to test out code for removing self referencing websites.
   # if csr(strlink,str_text) is True:
   #    return None


   if 'pdf' in strlink:
       try:
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

           fileName = searchName +str(incrementor) + ".p" #create text file save name
           print(fileName, 'filename')
           print(type(str_text))
           f = open(fileName, 'wb')
           from datetime import datetime
           st = datetime.utcnow().strftime('%Y-%m-%d_%H:%M:%S.%f')[:-3]
           pickle.dump([st, str_text],f)
       except:
           print('bad link',strlinkto)
   else:
      #establish human agent header
      headers = {'User-Agent': str(ua.Firefox)}
      #try:
      #request website data using beautiful soup
      try:

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
          fileName = searchName +str(incrementor) + ".p" #create text file save name

          print(fileName, 'filename')
          print(type(str_text))

          f = open(fileName, 'wb')
          from datetime import datetime
          st = datetime.utcnow().strftime('%Y-%m-%d_%H:%M:%S.%f')[:-3]
          pickle.dump([st, str_text],f)

      except:
          print('bad link',strlink)

   f = None
   return None


flat_iter = [ (b,x,category) for x, category in enumerate(searchList) for b in range(0,web) ]

def scraplandtext(fi):
    import pickle
    f = open('last_state.p', 'wb')
    #from datetime import datetime
    #st = datetime.utcnow().strftime('%Y-%m-%d_%H:%M:%S.%f')[:-3]
    pickle.dump(fi,f)
    #pickle.dump()
    b,x,category = fi
    print(" "); print("###############################################")
    print(" "); print(category);  print(" "); print("###############################################")
    categoryquery = category.replace(' ',"+")
    #set path for saving, and make the folder to save if it doesn't already exist
    path = fileLocation + '/' +  str(category) +'/'
    if not os.path.exists(path):
        os.makedirs(path)
    os.chdir(fileLocation + '/' +  str(category) +'/')
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
        linkChecker = [ e for e in elem if "https://www.google.com/search?" in str(e.get_attribute("href")) ]

        strings_to_process = []
        for linko in linkChecker:
            strlink = linko.get_attribute("href")
            strings_to_process.append(strlink)
            print(strlink)


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
        print("Google Scholar")



    elif b == 2:

        searchName = "bing_" #output name for text file
        linkName = "https://www.bing.com/search?num=100&filter=0&first=" #search engine web address
        pagestring = linkName + "&q=" + categoryquery # googles
        driver.get(pagestring)
        continue_link = driver.find_element_by_tag_name('a')
        elem = None
        elem = driver.find_elements_by_xpath("//*[@href]")
        linkChecker = [ e for e in elem if "https://www.bing.com/search?q=" in str(e.get_attribute("href")) ]
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
            #print(strlink)

    # only check the first 50 links : [0,49]

    # This code is here, to start up where left off, if HTTP requests are denied, because exceeded
    # crawling qouta policies.
    try:

        stp = [ (i,j, searchName) for i,j in enumerate(strings_to_process[0:49]) ]
        f = open('../last_state.p', 'rb')
        last_state = pickle.load(f)
        marker = None
        for i, temp in enumerate(stp):
            if str(last_state) == str(marker):
                marker = i
                break
        if type(marker) is not type(None):
            stp = [ (i,j, searchName) for i,j in enumerate(stp[marker+1:49]) ]
        _ = list(map(contents_to_file,stp))
    except:
        #print('file doesn\'t exist yet')
        #if type(strings_to_process) is not type(None):
        _ = list(map(contents_to_file,stp))
    return None
#flat_iter =[ (b,x,category) for b in range(0,web): for x, category in enumerate(searchList) ]
    #define the search term
_ = list(map(scraplandtext,flat_iter))
driver.close() #close the driver
exit()
