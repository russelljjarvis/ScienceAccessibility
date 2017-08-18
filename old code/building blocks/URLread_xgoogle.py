import time, random
from xgoogle.search import GoogleSearch, SearchError

f = open('a.txt','wb')

for i in range(0,2):
    wt = random.uniform(2, 5)
    gs = GoogleSearch("GMO")
    gs.results_per_page = 10
    gs.page = i
    results = gs.get_results()

    #Try not to annnoy Google, with a random short wait
    time.sleep(wt)
    print 'This is the %dth iteration and waited %f seconds' % (i, wt)
    for res in results:
        f.write(res.url.encode("utf8"))
        f.write("\n")

print "Done"
f.close()

######

from xgoogle.search import GoogleSearch, SearchError
try:
  gs = GoogleSearch("quick and dirty")
  gs.results_per_page = 50
  results = gs.get_results()
  for res in results:
    print res.title.encode("utf8")
    print res.desc.encode("utf8")
    print res.url.encode("utf8")
    print
except SearchError, e:
  print "Search failed: %s" % e
