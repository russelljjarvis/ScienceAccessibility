import requests
from bs4 import BeautifulSoup

url = "http://search.yahoo.com/search?p=%s"
query = "gmo"
r = requests.get(url % query)

soup = BeautifulSoup(r.text)
#soup.find_all(attrs={"class": "yschttl"})

#for link in soup.find_all(attrs={"class": "yschttl"}):
#    print "%s (%s)" %(link.text, link.get('href'))

links = soup.find_all("div")

print links

##old google search stuff
#g_data = soup.find_all("div", {"class"})

#for item in g_data:
#    print item.contents.find_all("cite", {"class": "_Rm"})


#https://www.youtube.com/watch?v=3xQTJi2tqgk

#<cite class="_Rm">responsibletechnology.org/<b>gmo</b>-education/</cite>
