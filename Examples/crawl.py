
## A lot of this code is informed by this multi-threading of web-grabbing example:
# https://github.com/NikolaiT/GoogleScraper/blob/master/Examples/image_search.py
# Probably the parallel architecture sucks, probably dask.bag mapping would be more readable and efficient.
##
#import threading,requests, os, urllib
from bs4 import BeautifulSoup
from natsort import natsorted, ns
import glob
import requests


import selenium
from pyvirtualdisplay import Display
from selenium import webdriver

display = Display(visible=0, size=(1024, 768))
display.start()
driver = webdriver.Firefox()
from fake_useragent import UserAgent
ua = UserAgent()


import pandas as pd
import pycld2 as cld2


import pdfminer
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams
from pdfminer.converter import  TextConverter

import re

from bs4 import BeautifulSoup
import bs4 as bs
import urllib.request

from io import StringIO
import io

rsrcmgr = PDFResourceManager()
retstr = StringIO()
laparams = LAParams()
codec = 'utf-8'
device = TextConverter(rsrcmgr, retstr, codec = codec, laparams = laparams)
interpreter = PDFPageInterpreter(rsrcmgr, device)



def pre_crawl(flat_iter):
    p, fileName, file_contents, index = flat_iter
    urlDat = {}
    _, _, details = cld2.detect(' '.join(file_contents.iloc[index]['snippet']), bestEffort=True)
    detectedLangName, _ = details[0][:2]
    server_status = bool(file_contents.iloc[index]['status']=='successful')
    english = bool(detectedLangName == 'ENGLISH')
    if server_status and english:
        return file_contents


def convert_pdf_to_txt(r):
    pdf = io.BytesIO(r.content)
    parser = PDFParser(pdf)
    document = PDFDocument(parser, password=None) # this fails
    write_text = ''
    for page in PDFPage.create_pages(document):
        interpreter.process_page(page)
        write_text +=  retstr.getvalue()
    # Process all pages in the document
    text = str(write_text)
    return text

def html_to_txt(content):
    soup = BeautifulSoup(content, 'html.parser')
    #strip HTML
    for script in soup(["script", "style"]):
        script.extract()    # rip it out
    text = soup.get_text()
    #organize text
    lines = (line.strip() for line in text.splitlines())  # break into lines and remove leading and trailing space on each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  ")) # break multi-headlines into a line each
    text = '\n'.join(chunk for chunk in chunks if chunk) # drop blank lines
    str_text = str(text)
    return str_text

class FetchResource():

    """Grabs a web resource and stores it in the target directory.

    Args:
        attrs: A directory where to save the resource.
        urls: A bunch of urls to grab

    """
    def __init__(self, url):
        if type(url) is type(str('')):
            self.url = url
            self.query = 'known_corpus'
            self.engine = 'relaxed'
        else:
            self.url = url.iloc[index]['link']
            self.query = url.iloc[index]['query']
            if str('!gs') in self.query:
                self.engine = 'g_scholar'
            else:
                self.engine = url.iloc[index]['search_engine_name']


    def run(self):
        # https://stackoverflow.com/questions/25936072/python-urllib2-httperror-http-error-503-service-unavailable-on-valid-website
        if 'pdf' in self.url:
            pdf_file = requests.get(self.url, stream=True)
            str_text = convert_pdf_to_txt(pdf_file)
        else:
            driver.get(self.url)
            crude_html = driver.page_source
            str_text = html_to_txt(crude_html)
        print('[+] Fetched {}'.format(str_text))
        return str_text


def collect_pubs(scholar_url):
    print(scholar_url)
    html_page = urllib.request.urlopen(scholar_url)
    soup = BeautifulSoup(html_page, 'html.parser')
    links = []
    for link in soup.findAll('a', attrs={'href': re.compile("https://")}):
        check_out = link.get('href')
        #if '/citations?' in check_out:
        links.append(check_out)
    return links
