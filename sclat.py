import requests

#print(requests.get(url, proxies=proxies).text)
##set parameters - THESE ARE ALL USER DEFINED
WEB = 6#how many search engines to include (4 possible- google google scholar bing yahoo)
LINKSTOGET= 50 #number of links to pull from each search engine (this can be any value, but more processing with higher number)
SEARCHLIST = ['Play Dough','Neutron','Vaccine','Transgenic','GMO','Genetically Modified Organism']
import sys
import os
#os.system('pip install python-twitter')

import selenium
from pyvirtualdisplay import Display
from selenium import webdriver

display = Display(visible=0, size=(1024, 768))
display.start()
driver = webdriver.Firefox()
from fake_useragent import UserAgent
ua = UserAgent()

fileLocation = os.getcwd()
#if you're switchign computers you can use this to indicate a second location to use if the first doesn't exist
import os
#if not os.path.exists(FileLocation):
#import web driver file to access chrome and establish a user-agent code
import os
import pickle
import time
import datetime


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
    #print(check_with)
    check="Our systems have detected unusual traffic from your computer network.\\nThis page checks to see if it\'s really you sending the requests, and not a robot.\\nWhy did this happen?\\nThis page appears when Google automatically detects requests coming from your computer network which appear to be in violation of the Terms of Service. The block will expire shortly after those requests stop.\\nIn the meantime, solving the above CAPTCHA will let you continue to use our services.This traffic may have been sent by malicious software, a browser plug in, or a script that sends automated requests.\\nIf you share your network connection, ask your administrator for help  a different computer using the same IP address may be responsible.\\nLearn moreSometimes you may be asked to solve the CAPTCHA if you are using advanced terms that robots are known to use, or sending requests very quickly."
    if len(check_with) == 1145:
        print('suspicious')
        #print(check_with)
        return True
    if check in check_with:
        return True
    check = "\\x00\\x00\\x00\\x00"
    if check in check_with:
        return True
    check = "Please click here if you are not redirected within a few seconds."
    if check in check_with:
        return True
    check="DuckDuckGo  Privacy, simplified.\\nAbout DuckDuckGo\\nDuck it!\\nThe search engine that doesn\'t track you.\\nLearn More."
    if check in check_with:
        return True
    return False

def referal_check(check_with):
    '''
    this is effective at finding when a click forward would help
    '''
    check = "DuckDuckGoYou are being redirected to the non-JavaScript site.Click here if it doesn't happen automatically."
    if check in check_with:
        #print(check_with)
        return True
    else:
        return False

def referal_trick():
    '''
    This only half works
    '''
    crude_html = driver.page_source
    #print(crude_html)
    driver.find_element_by_partial_link_text("Click here if it doesn't happen automatically").click()
    crude_html = driver.page_source
    soup = BeautifulSoup(crude_html, 'html.parser')
    for script in soup(["script", "style"]):
        script.extract()    # rip it out
    text = soup.get_text()
    return text


def contents_to_file(contents):
   '''
   visit links if the link expands into HTML, convert to string using Beautiful Soup,
   if it expands to a PDF use appropriate tools to extract string from PDF.
   Write files (pickle), with a time stamp when the file was created.
   '''
   incrementor, strlink, searchName = contents
   import time
   import random

   extra = 0.0
   if searchName == '_google':
       extra = 10.0
       print('extra time')
   sleepy = random.uniform(extra+4.0125,extra+11.75)
   print('time to sleep',sleepy)
   time.sleep(sleepy) #shor
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
       print(type(str_text),'stuck c')
       f = open(fileName, 'wb')
       from datetime import datetime
       st = datetime.utcnow().strftime('%Y-%m-%d_%H:%M:%S.%f')[:-3]
       pickle.dump([st, str(write_text),strlink],f)
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

      text = soup.get_text()


      if black_string(text) == True:
          print('badness')
          return 0.0
      else:
          if len(text) < 1000:
              print('suspicious')
              print(text)
              if referal_check(text) == True:
                  return 0.0
          print('goodness')

          #organize text
          lines = (line.strip() for line in text.splitlines())  # break into lines and remove leading and trailing space on each
          chunks = (phrase.strip() for line in lines for phrase in line.split("  ")) # break multi-headlines into a line each
          text = '\n'.join(chunk for chunk in chunks if chunk) # drop blank lines
          str_text = str(text)
          fileName = searchName +str(incrementor) + ".p" #create text file save name
          #write contents to file - individual text file for each URL's scraped text

          write_text = text.encode('ascii','ignore')
          fileName = searchName  + str(incrementor) + ".p" #create text file save name
          #
          print(fileName, 'filename')
          #print(type(str_text),'stuck d')

          f = open(fileName, 'wb')
          from datetime import datetime
          st = datetime.utcnow().strftime('%Y-%m-%d_%H:%M:%S.%f')[:-3]
          pickle.dump([st, str(write_text),strlink],f)
          f = None
      return len(str_text)



def lc(linkChecker):
    '''
    Reformat html elements containing links to lists of strings.
    '''
    strings_to_process = []
    for linko in linkChecker:
        strlink = linko.get_attribute("href")
        strings_to_process.append(strlink)
        print(strlink)
    return strings_to_process

import requests
from bs4 import BeautifulSoup

headers_Get = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }


def google(q):
    s = requests.Session()
    q = '+'.join(q.split())
    url = 'https://www.google.com/search?q=' + q + '&ie=utf-8&oe=utf-8'
    r = s.get(url, headers=headers_Get)

    soup = BeautifulSoup(r.text, "html.parser")
    output = []
    for searchWrapper in soup.find_all('h3', {'class':'r'}): #this line may change in future based on google's web page structure
        url = searchWrapper.find('a')["href"]
        text = searchWrapper.find('a').text.strip()
        #result = {'text': text, 'url': url}
        output.append(url)
    return output


def preview_links(b,categoryquery):

    if b == 0:
        strings_to_process = google(categoryquery)


        # probably toggle between above mode and this commented out mode, such as to diversify requests sent to google
        # under principle that diversified request sources are more human and less bot like.

        '''
        searchName = "google_" #output name for text file
        linkName = "https://www.google.com/search?q=" #search engine web address

        pagestring = linkName + categoryquery # googles
        driver.get(pagestring)
        continue_link = driver.find_element_by_tag_name('a')
        elem = None
        elem = driver.find_elements_by_xpath("//*[@href]")
        linkChecker = []
        linkChecker = [ e for e in elem if "https://www.google.com/search?q=" in str(e.get_attribute("href")) ]
        strings_to_process = lc(linkChecker)
        '''



    if b == 1:

        searchName = "gScholar_" #output name for text file
        linkName = "https://scholar.google.com/scholar?hl=en&as_sdt=0%2C3&q="

        pagestring = linkName + "&q=" + categoryquery # googles
        print("Google Scholar")
        driver.get(pagestring)
        continue_link = driver.find_element_by_tag_name('a')
        elem = None
        elem = driver.find_elements_by_xpath("//*[@href]")
        linkChecker = []
        linkChecker = [ e for e in elem if "https://scholar.google.com/scholar?q=" in str(e.get_attribute("href")) ]
        # scholar is  href="/scholar?
        strings_to_process = lc(linkChecker)
        print("Google Scholar")


    if b == 2:

        searchName = "bing_" #output name for text file
        linkName = "https://www.bing.com/search?num=100&filter=0&first=" #search engine web address
        pagestring = linkName + "&q=" + categoryquery # googles
        driver.get(pagestring)
        print(' Bing')
        continue_link = driver.find_element_by_tag_name('a')
        elem = None
        elem = driver.find_elements_by_xpath("//*[@href]")
        #href="/search?q=
        linkChecker = [ e for e in elem if "https://www.bing.com/search?" in str(e.get_attribute("href")) ]
        linkChecker = [ strlink for strlink in linkChecker if 'r.bat' not in strlink.get_attribute("href") or 'r.msn' \
         not in strlink.get_attribute("href") or'www.bing.com/news/search' not in strlink.get_attribute("href") ]

        strings_to_process = lc(linkChecker)

        #strings_to_process = []

        #print("\nchecking: " + pagestring + "\n")
    if b == 3:
        strings_to_process = []

    '''
    if b == 3:
        searchName = "twitter_" #output name for text file
        linkName =  "https://twitter.com/search?q=" #search engine web address
        pagestring = linkName + categoryquery +str('%50&result_type=recent&since=2014-07-19&count=100')
        print("yahoo")
        driver.get(pagestring)
        #results = api.GetSearch(raw_query="q="+categoryquery+"%50&result_type=recent&since=2014-07-19&count=100")
        #from xml.etree import ElementTree
        #response = session.get("https://search.yahoo.com/search?p="+str(categoryquery)).text
        #tree = ElementTree.fromstring(response.content)
        continue_link = driver.find_element_by_tag_name('a')
        elem = None
        elem = driver.find_elements_by_xpath("//*[@href]")
        linkChecker = [ e for e in elem if "https://twitter.com" in str(e.get_attribute("href")) ]
        strings_to_process = lc(linkChecker)
    '''

    if b == 4:
        searchName = "yahoo_" #output name for text file
        linkName =  "https://search.yahoo.com/search?p=" #search engine web address
        pagestring = linkName + categoryquery
        print("yahoo")
        driver.get(pagestring)
        continue_link = driver.find_element_by_tag_name('a')
        elem = None
        elem = driver.find_elements_by_xpath("//*[@href]")
        linkChecker = [ e for e in elem if "https://search.yahoo.com" in str(e.get_attribute("href")) ]
        strings_to_process = lc(linkChecker)


    elif b == 5:
        searchName = "duckduckgo_" #output name for text file
        #https://duckduckgo.com/?q=  #Vaccine&t=hf&atb=v73-3_q&ia=web
        #https://duckduckgo.com/?q=  #GMO&t=hf&atb=v73-3_q&ia=stock
        linkName =  "https://duckduckgo.com/html/?q=" #search engine web address
        pagestring = linkName + categoryquery # googles
        print("duckduckgo")
        #pagestring = str('https://api.duckduckgo.com/?q=')+categoryquery+
        driver.get(pagestring)
        continue_link = driver.find_element_by_tag_name('a')
        elem = None
        elem = driver.find_elements_by_xpath("//*[@href]")
        linkChecker = [ e for e in elem if "https://duckduckgo.com/?q=" in str(e.get_attribute("href")) ]
        strings_to_process = lc(linkChecker)
    return strings_to_process




def scraplandtext(fi):
    #from fake_useragent import UserAgent
    #ua = UserAgent()

    os.chdir('/home/jovyan')
    b,category = fi
    f = open('last_iterator.p', 'ab')
    pickle.dump(fi,f)
    categoryquery = category.replace(' ',"+")
    #set path for saving, and make the folder to save if it doesn't already exist
    path = fileLocation + '/' +  str(category) +'/'
    os.chdir(path)

    strings_to_process = preview_links(b,categoryquery)
    print(strings_to_process)
    assert type(strings_to_process) is type([0,0])
    import utils
    se, _ = utils.engine_dict_list()

    lta = [ (i,j, se[b]) for i,j in enumerate(strings_to_process[0:LINKSTOGET]) ]
    import dask.bag as db
    # shuffle
    # random traversal of an otherwides hierachical traversal of link rank to
    # principle that random traversal feigns humanhood

    random.shuffle(lta)
    random.shuffle(lta)
    random.shuffle(lta)

    lengths_of_texts = list(map(contents_to_file,lta))
    lengths_of_texts_old = list(filter(lambda x: x != 0, lengths_of_texts))
    old_delta = LINKSTOGET - len(lengths_of_texts_old)
    print('delta',LINKSTOGET - len(lengths_of_texts_old) )
    print(lengths_of_texts_old)
    #return lta

    old = LINKSTOGET + 1
    while len(lengths_of_texts_old) < LINKSTOGET:
        # if links searched was less than 50
        # assume the first links searched were good and the rest were bad
        # therefore want to make up the difference between links explored and 50 if possible
        # but only if the server isn't outright rejecting requests
        # comparing 50 versus number of valid search returns twice, gives an indication of whether exploring
        # further down the page rank helps. If it doesn't quit outright.

        new_delta = LINKSTOGET - len(lengths_of_texts_old)
        if old_delta == new_delta:
            return
        print('delta',new_delta)
        old_plus = LINKSTOGET + LINKSTOGET - len(lengths_of_texts_old)
        lta = [ (i,j, searchName) for i,j in enumerate(strings_to_process[old:int(old_plus)]) ]
        random.shuffle(lta)
        random.shuffle(lta)
        lengths_of_texts_new = list(map(contents_to_file,lta))
        lengths_of_texts_new = list(filter(lambda x: x != 0, lengths_of_texts_new))
        lengths_of_texts_new.extend(lengths_of_texts_old)
        lengths_of_texts_old = lengths_of_texts_new
        old = old_plus
        old_delta = new_delta

    return # required for readability only




import pickle
import os


if os.path.isfile('last_iterator.p'):
    try:
        contents = pickle.load(open('last_iterator.p', 'rb'))
        flat_iter = contents[0]
        b,category = contents[-1]
    except:
        flat_iter = [ (b,category) for category in SEARCHLIST for b in range(0,WEB) ]
        f = open('last_iterator.p', 'wb')
        pickle.dump(flat_iter,f)
        random.shuffle(flat_iter)
        from utils import purge

# the idea is that grid and flat iter should be very similar.
# grid is a bit more maintainable and conventional way of building iterators.

#ltas = list(map(purge,iter(flat_iter)))
##
# Randomly shuffle the list, instead of going through the list in logical sequence.
# Humans are erratic, bots are not. Feign humanhood by adopting erratic behavior.
##


ltas = list(map(scraplandtext,iter(flat_iter)))

driver.close() #close the driver
os.chdir('/home/jovyan/')
