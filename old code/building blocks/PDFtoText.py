from StringIO import StringIO
import urllib2
from urllib2 import Request

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams
from pdfminer.converter import  TextConverter # , XMLConverter, HTMLConverter

# Define parameters to the PDF device objet 
rsrcmgr = PDFResourceManager()
retstr = StringIO()
laparams = LAParams()
codec = 'utf-8'
device = TextConverter(rsrcmgr, retstr, codec = codec, laparams = laparams)
interpreter = PDFPageInterpreter(rsrcmgr, device)

###################
strlink = 'http://sttheresechurch.ca/pdf/notice/201308FCR.pdf'

##pdf_file = requests.get(strlink)
pdf_file = urllib2.urlopen(Request(strlink)).read()
memoryFile = StringIO(pdf_file)
parser = PDFParser(memoryFile)
document = PDFDocument(parser)

# Process all pages in the document
for page in PDFPage.create_pages(document):
    interpreter.process_page(page)
    data =  retstr.getvalue()
