
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
#from pyvirtualdisplay import Display
from selenium import webdriver



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
import numpy as np


from bs4 import BeautifulSoup
import bs4 as bs
import urllib.request

from delver import Crawler
C = Crawler()
CWD = os.getcwd()

from io import StringIO
import io


rsrcmgr = PDFResourceManager()
retstr = StringIO()
laparams = LAParams()
codec = 'utf-8'
device = TextConverter(rsrcmgr, retstr, laparams = laparams)
interpreter = PDFPageInterpreter(rsrcmgr, device)



def convert_pdf_to_txt(content):
    try:
        pdf = io.BytesIO(content.content)
    except:
        pdf = io.BytesIO(content)
    parser = PDFParser(pdf)
    document = PDFDocument(parser, password=None) # this fails
    write_text = ''
    for page in PDFPage.create_pages(document):
        interpreter.process_page(page)
        write_text +=  retstr.getvalue()
        #write_text = write_text.join(retstr.getvalue())
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

def print_best_text(fileName):
    file = open(fileName)

    return text

def denver_to_text(url):
    fileName = C.download(local_path=CWD, url=url, name='temp_file')
    file = open(fileName)
    if str('.html') in fileName:
        text = html_to_txt(file)
    else:
        text = convert_pdf_to_txt(file)
    file.close()
    return text

def collect_hosted_files(url):
    '''
    Used for scholar
    '''
    #print(url)
    try:
        crude_html = denver_to_text(url)
    except:
        driver.get(url)
        crude_html = driver.page_source
    #soup0 = BeautifulSoup(crude_html, 'html.parser')
    soup = BeautifulSoup(crude_html, 'lxml')
    links = []
    print(soup)
    for link in soup.findAll('a'):check_out = link.get('href');links.append(check_out)
        #print(link)
    for link in soup.findAll('a', attrs={'href': re.compile("https://")}):
        check_out = link.get('href')
        #if '/citations?' in check_out:
        links.append(check_out)
    for link in soup.findAll('a', attrs={'href': re.compile("http://")}):
        check_out = link.get('href')
        #if '/citations?' in check_out:
        links.append(check_out)

    return links

if 'DYNO' in os.environ:
    heroku = True
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
else:
    heroku = False
from selenium.common.exceptions import NoSuchElementException
import os
from selenium import webdriver

def get_driver():
    if 'DYNO' in os.environ:
        heroku = True
    else:
        heroku = False
    from selenium.webdriver.firefox.options import Options

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    try:
        driver = webdriver.Firefox(options=options)
    except:
        try:
            options.binary_location = "/app/vendor/firefox/firefox"
            driver = webdriver.Firefox(options=options)
            GECKODRIVER_PATH=str(os.getcwd())+str("/geckodriver")
            driver = webdriver.Firefox(options=options,executable_path=GECKODRIVER_PATH)
        except:
            try:
                chrome_options = webdriver.ChromeOptions()
                chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
                chrome_options.add_argument("--headless")
                chrome_options.add_argument("--disable-dev-shm-usage")
                chrome_options.add_argument("--no-sandbox")
                driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
            except:
                try:
                    GECKODRIVER_PATH=str(os.getcwd())+str("/geckodriver")
                    options.binary_location = str('./firefox')
                    driver = webdriver.Firefox(options=options,executable_path=GECKODRIVER_PATH)
                except:
                    os.system("wget wget https://ftp.mozilla.org/pub/firefox/releases/45.0.2/linux-x86_64/en-GB/firefox-45.0.2.tar.bz2")
                    os.system("wget https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz")
                    os.system("tar -xf geckodriver-v0.26.0-linux64.tar.gz")
                    os.system("tar xvf firefox-45.0.2.tar.bz2")
                    GECKODRIVER_PATH=str(os.getcwd())+str("/geckodriver")
                    options.binary_location = str('./firefox')
                    driver = webdriver.Firefox(options=options,executable_path=GECKODRIVER_PATH)
    return driver
from time import sleep
import numpy as np


def collect_pubs(url):
    '''
    Used for scholar which is only html
    '''
    # import needs to be inside function  to protect scope.

    driver = get_driver()
    if heroku:
        sleep(np.random.uniform(1,3))

        #wait = WebDriverWait(driver, 10)
        #wait.until(EC.url_changes(url))
        driver.get(url)
    else:
        driver.get(url)
    crude_html = driver.page_source

    soup = BeautifulSoup(crude_html, 'html.parser')
    links = []
    for link in soup.findAll('a', attrs={'href': re.compile("https://")}):
        check_out = link.get('href')
        #if '/citations?' in check_out:
        links.append(check_out)
    for link in soup.findAll('a', attrs={'href': re.compile("http://")}):
        check_out = link.get('href')
        #if '/citations?' in check_out:
        links.append(check_out)
    driver.close()
    driver.quit() 
    driver = None
    del driver
    return links
