import requests
import os
from bs4 import BeautifulSoup
import numpy as np
import scipy.io as sio
import re

os.chdir('/Users/PMcG/Dropbox (ASU)/AAB_files/Pat-files/WCP/code/Data Files/testFiles/')
fileName = "googleTest1.txt"        
fileHandle = open(fileName, 'rU');

#read text file
url_text = fileHandle.read()
fileHandle.close()

url = "http://www.webpagefx.com/tools/read-able/check.php"
payload = {'directInput':url_text, 'tab': 'Test by Direct Link'}
r = requests.post(url, data=payload)
#print r.text

soup = BeautifulSoup(r.content, 'html.parser')

#strip HTML scripting and style
for script in soup(["script", "style"]):
        script.extract()    # rip it out
        
text = soup.get_text()
# break into lines and remove leading and trailing space on each
lines = (line.strip() for line in text.splitlines())
# break multi-headlines into a line each
chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
# drop blank lines
text = '\n'.join(chunk for chunk in chunks if chunk)

text =  text.split('\n')
text = text[9:37]
print text

temp = text[0].rsplit('.'); temp = temp[0]

Read = {}
Read[1,1] = "grade level"; Read[1,2] = [re.findall(r'\d', temp)[:2]]
Read[2,1] = text[2]; Read[2,2] = text[3]
Read[3,1] = text[4]; Read[3,2] = text[5]
Read[4,1] = text[6]; Read[4,2] = text[7]
Read[5,1] = text[8]; Read[5,2] = text[9]
Read[6,1] = text[10]; Read[6,2] = text[11]
Read[7,1] = text[12]; Read[7,2] = text[13]
Read[8,1] = text[15]; Read[8,2] = text[16]
Read[9,1] = text[17]; Read[9,2] = text[18]
Read[10,1] = text[19]; Read[10,2] = text[20]
Read[11,1] = text[21]; Read[11,2] = text[22]
Read[12,1] = "average words for sentence"; Read[12,2] = text[25]
Read[13,1] = text[26]; Read[13,2] = text[27]

print Read

#Read = Read.items();
#obj_arr = np.array([Read], dtype=object)
#sio.savemat('Readable.mat', {'obj_arr':obj_arr})
            
