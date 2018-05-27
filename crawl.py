


## A lot of this code is informed by this multi-threading of web-grabbing example:
# https://github.com/NikolaiT/GoogleScraper/blob/master/Examples/image_search.py
# Probably the parallel architecture sucks, probably dask.bag mapping would be more readable and efficient.
##
import threading,requests, os, urllib
from bs4 import BeautifulSoup
from natsort import natsorted, ns
import glob
#import pandas as pd

import pandas as pd
import pycld2 as cld2
import urllib


import pdfminer
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams
from pdfminer.converter import  TextConverter


from io import StringIO
import io

rsrcmgr = PDFResourceManager()
retstr = StringIO()
laparams = LAParams()
codec = 'utf-8'
device = TextConverter(rsrcmgr, retstr, codec = codec, laparams = laparams)
interpreter = PDFPageInterpreter(rsrcmgr, device)


from bs4 import BeautifulSoup
import bs4 as bs
import urllib.request

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
    soup = BeautifulSoup(content.read(), 'html.parser')
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
        url = urllib.parse.unquote(self.url)
        if 'pdf' in url:
            r = requests.get(url)
            str_text = convert_pdf_to_txt(r)
        else:
            content = urllib.request.urlopen(url)
            str_text = html_to_txt(content)
        print('[+] Fetched {}'.format(str_text))
        return str_text

flat_iter = []
# naturally sort a list of files, as machine sorted is not the desired file list hierarchy.
lo_query_links = natsorted(glob.glob(str(os.getcwd())+'/*.csv'))
print(lo_query_links)
#lo_query_links = lo_query_links[0:5]
list_per_links = []
for p,fileName in enumerate(lo_query_links):
    b = os.path.getsize(fileName)
    if b>250: # this is just to prevent reading in of incomplete data.
        file_contents = pd.read_csv(fileName)
        for index in range(0,len(file_contents)):
            flat_iter.append((p,fileName,file_contents,index))
#print(flat_iter)
resource_urls = list(map(pre_crawl,flat_iter))


# Especially this one it was written with upgoer5
# These texts should be pretty good:
# http://splasho.com/upgoer5/library.php

resource_urls = ['http://splasho.com/upgoer5/library.php','https://academic.oup.com/beheco/article-abstract/29/1/264/4677340', \
'https://elifesciences.org/download/aHR0cHM6Ly9jZG4uZWxpZmVzY2llbmNlcy5vcmcvYXJ0aWNsZXMvMjc3MjUvZWxpZmUtMjc3MjUtdjIucGRm/elife-27725-v2.pdf?_hash=WA%2Fey48HnQ4FpVd6bc0xCTZPXjE5ralhFP2TaMBMp1c%3D',\
]
texts = []
for r in resource_urls:
    fr = FetchResource(r)
    texts.append(fr.run())
print(texts)
