
## A lot of this code is informed by this multi-threading of web-grabbing example:
# https://github.com/NikolaiT/GoogleScraper/blob/master/Examples/image_search.py
# Probably the parallel architecture sucks, probably dask.bag mapping would be more readable and efficient.
##
import threading,requests, os, urllib
from bs4 import BeautifulSoup
from natsort import natsorted, ns
import glob
import pandas as pd

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

rsrcmgr = PDFResourceManager()
retstr = StringIO()
laparams = LAParams()
codec = 'utf-8'
device = TextConverter(rsrcmgr, retstr, codec = codec, laparams = laparams)
interpreter = PDFPageInterpreter(rsrcmgr, device)

def crawl(flat_iter):
    # better to rewrite nested for loop as a function to map over.
    p, fileName, file_contents, index = flat_iter
    urlDat = {}
    _, _, details = cld2.detect(' '.join(file_contents.iloc[index]['snippet']), bestEffort=True)
    detectedLangName, _ = details[0][:2]
    server_status = bool(file_contents.iloc[index]['status']=='successful')
    english = bool(detectedLangName == 'ENGLISH')
    if server_status and english:
        return file_contents

class FetchResource(threading.Thread):
    """Grabs a web resource and stores it in the target directory.

    Args:
        attrs: A directory where to save the resource.
        urls: A bunch of urls to grab

    """
    def __init__(self, file_contents):
        super().__init__()
        self.urls = file_contents.iloc[index]['link']
        self.query = file_contents.iloc[index]['query']
        if str('!gs') in self.query:
            self.engine = 'g_scholar'
        else:
            self.engine = file_contents.iloc[index]['search_engine_name']
        print(self.engine)

    def run(self):
        for url in self.urls:
            url = urllib.parse.unquote(url)
            if 'pdf' in url:
               pdf_file = str(urllib.request.urlopen(strlink).read())
               memoryFile = StringIO(pdf_file)
               parser = PDFParser(memoryFile)
               document = PDFDocument(parser)
               # Process all pages in the document
               for page in PDFPage.create_pages(document):
                   interpreter.process_page(page)
                   write_text +=  retstr.getvalue()
               str_text = str(write_text)
           else:
                content = requests.get(url).content
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
            print('[+] Fetched {}'.format(url))
            return # for readibility only

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
print(flat_iter)
import pdb
pdb.set_trace()
resource_urls = list(map(crawl,flat_iter))
import threading,requests, os, urllib

# fire up 100 threads to get the images
num_threads = 100
threads = [FetchResource([]) for i in range(num_threads)]
while resource_urls:
    for t in threads:
        try:
            t.urls.append(resource_urls.pop())
        except IndexError as e:
            break
threads = [t for t in threads if t.urls]
for t in threads:
    t.start()
for t in threads:
    t.join()
