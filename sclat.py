import requests

def get_tor_session():
    session = requests.session()
    # Tor uses the 9050 port as the default socks port
    session.proxies = {'http':  'socks5://127.0.0.1:9050',
                       'https': 'socks5://127.0.0.1:9050'}
    return session

# Make a request through the Tor connection
# IP visible through Tor
session = get_tor_session()

##set parameters - THESE ARE ALL USER DEFINED
WEB = 5#how many search engines to include (4 possible- google google scholar bing yahoo)
LINKSTOGET= 10 #number of links to pull from each search engine (this can be any value, but more processing with higher number)
SEARCHLIST = ['Play Dough','Neutron','Vaccine','Transgenic','GMO','Genetically Modified Organism']

import sys
import os


fileLocation = os.getcwd()
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
from random import uniform

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
   # This function is not used though it's not depricated either.
   # The method needs debugging

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
       # scholar is  href="/scholar?
       links.append(str(e.get_attribute("href")))

   from urllib.parse import urlparse
   print(strlink)
   baseURLtemp = urlparse(strlink)
   baseURL = str(baseURLtemp[0] + "://" + baseURLtemp[1])
   if strlink in text:
       print('probably links to self')
       print(strlink,text)
   for l in links:
      print('conclusively links to self')
      if str(baseURL) in str(l):
          return True
   return False


import random

def black_string(check_with):
    check="Our systems have detected unusual traffic from your computer network.\\nThis page checks to see if it\'s really you sending the requests, and not a robot.\\nWhy did this happen?\\nThis page appears when Google automatically detects requests coming from your computer network which appear to be in violation of the Terms of Service. The block will expire shortly after those requests stop.\\nIn the meantime, solving the above CAPTCHA will let you continue to use our services.This traffic may have been sent by malicious software, a browser plug in, or a script that sends automated requests.\\nIf you share your network connection, ask your administrator for help  a different computer using the same IP address may be responsible.\\nLearn moreSometimes you may be asked to solve the CAPTCHA if you are using advanced terms that robots are known to use, or sending requests very quickly."
    if len(check_with) == 1145:
        print('suspicious')
        return True
    if check in check_with:
        return True
    check = "\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00"
    if check in check_with:
        return True
    check = "Please click here if you are not redirected within a few seconds."
    if check in check_with:
        return True
    check="DuckDuckGo  Privacy, simplified.\\nAbout DuckDuckGo\\nDuck it!\\nThe search engine that doesn\'t track you.\\nLearn More."
    if check in check_with:
        return True
    return False
MORE = 0.0
def contents_to_file(contents):
   '''
   visit links if the link expands into HTML, convert to string using Beautiful Soup,
   if it expands to a PDF use appropriate tools to extract string from PDF.
   Write files (pickle), with a time stamp when the file was created.
   '''
   incrementor, strlink, searchName = contents
   import time
   import random
   time.sleep(random.uniform(1.0125 + MORE,5.75)) #shor
   if 'pdf' in strlink:
       import urllib
       #try:
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
       #write_text = str_text.encode('ascii','ignore')
       fileName = searchName  + str(incrementor) + ".txt" #create text file save name
       f = open(fileName, 'w')
       f.write(str_text)
       f.close()


       fileName = searchName +str(incrementor) + ".p" #create text file save name
       print(fileName, 'filename')
       print(type(str_text))
       f = open(fileName, 'wb')
       from datetime import datetime
       st = datetime.utcnow().strftime('%Y-%m-%d_%H:%M:%S.%f')[:-3]
       pickle.dump([st, str(write_text)],f)
       #except:
        #   print('bad link',strlinkto)
   else:
      #establish human agent header
      headers = {'User-Agent': str(ua.Firefox)}
      r = requests.get(strlink, headers=headers)
      soup = BeautifulSoup(r.content, 'html.parser')

      #strip HTML
      for script in soup(["script", "style"]):
              script.extract()    # rip it out

      # get text
      text = soup.get_text()
      if len(text) < 1145:
          print('suspicious')
      if black_string(text) == True:
          print('badness')
          print('contents')
          MORE += 1.0
          return 0.0
      else:
          print('goodness')

          #organize text
          lines = (line.strip() for line in text.splitlines())  # break into lines and remove leading and trailing space on each
          chunks = (phrase.strip() for line in lines for phrase in line.split("  ")) # break multi-headlines into a line each
          text = '\n'.join(chunk for chunk in chunks if chunk) # drop blank lines
          str_text = str(text)
          fileName = searchName +str(incrementor) + ".p" #create text file save name
          #write contents to file - individual text file for each URL's scraped text

          write_text = text.encode('ascii','ignore')
          #fileName = searchName  + str(incrementor) + ".txt" #create text file save name
          #
          #f = open(fileName, 'w')
          #f.write(str(write_text))
          #f.close()
          fileName = searchName  + str(incrementor) + ".p" #create text file save name
          #
          print(fileName, 'filename')
          print(type(str_text))

          f = open(fileName, 'wb')
          from datetime import datetime
          st = datetime.utcnow().strftime('%Y-%m-%d_%H:%M:%S.%f')[:-3]
          pickle.dump([st, str(write_text)],f)
          f = None
      return len(str_text)



def scraplandtext(fi):

    os.chdir('/home/jovyan/wcproject')
    b,category = fi
    f = open('last_iterator.p', 'wb')
    pickle.dump(fi,f)
    categoryquery = category.replace(' ',"+")
    #set path for saving, and make the folder to save if it doesn't already exist
    path = fileLocation + '/' +  str(category) +'/'
    os.chdir(path)
    #os.chdir(fileLocation + '/' +  str(category) +'/')


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
        print("Google Scholar")
        driver.get(pagestring)
        continue_link = driver.find_element_by_tag_name('a')
        elem = None
        elem = driver.find_elements_by_xpath("//*[@href]")
        linkChecker = []
        linkChecker = [ e for e in elem if "https://scholar.google.com/scholar?" in str(e.get_attribute("href")) ]
        # scholar is  href="/scholar?

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
        print(' Bing')
        continue_link = driver.find_element_by_tag_name('a')
        elem = None
        elem = driver.find_elements_by_xpath("//*[@href]")
        #href="/search?q=
        linkChecker = [ e for e in elem if "https://www.bing.com/search?q=" in str(e.get_attribute("href")) ]
        linkChecker = [ strlink for strlink in linkChecker if 'r.bat' not in strlink.get_attribute("href") or 'r.msn' \
         not in strlink.get_attribute("href") or'www.bing.com/news/search' not in strlink.get_attribute("href") ]

        strings_to_process = []
        for linko in linkChecker:
            strlink = linko.get_attribute("href")
            strings_to_process.append(strlink)
            print(strlink)
        #print("\nchecking: " + pagestring + "\n")


    elif b == 3:
        searchName = "duckduckgo_" #output name for text file
        #https://duckduckgo.com/?q=  #Vaccine&t=hf&atb=v73-3_q&ia=web
        #https://duckduckgo.com/?q=  #GMO&t=hf&atb=v73-3_q&ia=stock
        linkName =  "https://duckduckgo.com/?q=" #search engine web address
        pagestring = linkName + "&q=" + categoryquery # googles
        print("duckduckgo")
        driver.get(pagestring)
        continue_link = driver.find_element_by_tag_name('a')
        elem = None
        elem = driver.find_elements_by_xpath("//*[@href]")
        #linkChecker = [ e for e in elem if "http://r.search.yahoo.com/_ylt=" in str(e.get_attribute("href")) ]

        strings_to_process = []
        for linko in elem:
            strlink = linko.get_attribute("href")
            strings_to_process.append(strlink)


    if b==4:
        searchName = "yahoo_" #output name for text file
        linkName =  "https://duckduckgo.com/?q="+"!y " #search engine web address
        pagestring = linkName + "&q=" + categoryquery
        from xml.etree import ElementTree
        response = session.get("https://search.yahoo.com/search?p="+str(categoryquery)).text
        tree = ElementTree.fromstring(response.content)
        continue_link = tree.find_element_by_tag_name('a')
        elem = None
        elem = tree.find_elements_by_xpath("//*[@href]")
        linkChecker = [ e for e in elem if "https://r.search.yahoo.com" in str(e.get_attribute("href")) ]
        strings_to_process = []
        for linko in linkChecker:
            strlink = linko.get_attribute("href")
            strings_to_process.append(strlink)
            print(strlink)
        time.sleep(random.uniform(1.0125,5.75)) #shor

    # assert there are less than 5 search engines
    if b >= 5:
        print(b,'gets here bug causing data loss. Check iterator construction below')
        return None
    # only check the first 50 links : [0,49]


    lta = [ (i,j, searchName) for i,j in enumerate(strings_to_process[0:LINKSTOGET]) ]
    # links to analyze
    import dask.bag as db
    lengths_of_texts = list(map(contents_to_file,lta))
    print('lengths_of_texts',lengths_of_texts)
    cnt = 0
    for i in lengths_of_texts:
        if i==0:
            cnt+=1
    old = LINKSTOGET
    old_plus = LINKSTOGET+cnt

    while 0 in lengths_of_texts:
        cnt = 0
        for i in lengths_of_texts:
            if i==0:
                cnt+=1

        lta = [ (i,j, searchName) for i,j in enumerate(strings_to_process[old:int(old_plus)]) ]
        lengths_of_texts = list(map(contents_to_file,lta))
        old = old_plus
        old_plus = old + cnt



    return lta
import dask.bag as db




import pickle
import os


if os.path.isfile('last_iterator.p'):
    #x,b,category = fi
    b,category = pickle.load(open('last_iterator.p', 'rb'))
    flat_iter = [ (b1,SEARCHLIST[x1]) for x1 in range(x,len(SEARCHLIST)) for b1 in range(b,WEB)   ]
    '''
    Idealized syntax would utilize grid.
    grid = {}
    grid['b']=[0,1,2,3,4]
    grid['search_term'] = [ i for i in enumerate(SEARCHLIST) ]
    from sklearn.grid_search import ParameterGrid
    grid = list(ParameterGrid(grid))
    grid = [(dicti['b'],dicti['search_term'][1]) for dicti in grid ]
    '''
else:
    grid = {}
    grid['b']=[0,1,2,3,4]
    grid['search_term'] = [ i for i in enumerate(SEARCHLIST) ]
    from sklearn.grid_search import ParameterGrid
    grid = list(ParameterGrid(grid))
    flat_iter = [ (b,category) for category in SEARCHLIST for b in range(0,WEB) ]
    #import pdb
    #pdb.set_trace()
    #for i, j in enumerate(flat_iter):
    #    print(j,grid[i],i)
    #print(grid)
    print(flat_iter)


def pre_dir(fi):
    # Old expresion: b,x,category = fi
    # New Expression
    b,category = fi
    categoryquery = category.replace(' ',"+")
    path = fileLocation + '/' +  str(category) +'/'

    if os.path.exists(path):
        os.chdir(path)
        os.system('rm *.p')
        print('purging cached data')
    else:
        os.makedirs(path)
        os.chdir(path)
# the idea is that grid and flat iter should be very similar.
# grid is a bit more maintainable and conventional way of building iterators.
ltas = list(map(pre_dir,iter(flat_iter)))#.result()\n",

ltas = list(map(scraplandtext,iter(flat_iter)))#.result()\n",
for i,l in enumerate(ltas):
    if i !=0:
        print(len(l)==0)
        print('yahoo broken')
        #assert len(l)==old
    old = len(l)

driver.close() #close the driver
os.chdir('/home/jovyan/../')
