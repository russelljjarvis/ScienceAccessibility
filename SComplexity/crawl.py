
## A lot of this code is informed by this multi-threading of web-grabbing example:
# https://github.com/NikolaiT/GoogleScraper/blob/master/Examples/image_search.py
# Probably the parallel architecture sucks, probably dask.bag mapping would be more readable and efficient.
##
#import threading,requests, os, urllib
from bs4 import BeautifulSoup
from natsort import natsorted, ns
import glob
import requests
import os

import selenium
from pyvirtualdisplay import Display
from selenium import webdriver

from fake_useragent import UserAgent

display = Display(visible=0, size=(1024, 768))
display.start()

from fake_useragent import UserAgent
useragent = UserAgent()
profile = webdriver.FirefoxProfile()
profile.set_preference("general.useragent.override", useragent.random)
profile.set_preference("javascript.enabled", True)
driver = webdriver.Firefox(firefox_profile=profile)

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

from delver import Crawler
C = Crawler()


rsrcmgr = PDFResourceManager()
retstr = StringIO()
laparams = LAParams()
codec = 'utf-8'
device = TextConverter(rsrcmgr, retstr, codec = codec, laparams = laparams)
interpreter = PDFPageInterpreter(rsrcmgr, device)



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



def denver_to_text(url):
    fileName = C.download(local_path=os.getcwd(),url=url,name=url)
    file = open(fileName)
    if str('.html') in fileName:
        text = html_to_txt(file)
    else:
        text = convert_pdf_to_txt(file)
    file.close()
    return text


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
            # of denver versus, selenium. Both are good clothes.
            # which one works best will depend on how much exposure the servers queried have already had
            # with your client.
            try:
                driver.get(self.url)
                crude_html = driver.page_source
            except:
                crude_html = denver_to_text(self.url)

            str_text = html_to_txt(crude_html)
        print('[+] Fetched {}'.format(str_text))
        #driver.quit()
        return str_text



def collect_pubs(scholar_url):
    print(scholar_url)
    try:
        crude_html = denver_to_text(scholar_url)
    except:
        driver.get(self.scholar_url)
        crude_html = driver.page_source
    soup = BeautifulSoup(crude_html, 'html.parser')
    links = []
    for link in soup.findAll('a', attrs={'href': re.compile("https://")}):
        check_out = link.get('href')
        #if '/citations?' in check_out:
        links.append(check_out)
    return links
