from pytrends.request import TrendReq
import time
from random import randint

google_username = "patrick.mcgurrin@gmail.com"
google_password = "xxx"
path = ""

term = "GMO"

# connect to Google
time.sleep(randint(5, 10))
pytrend = TrendReq(google_username, google_password, custom_useragent='My Pytrends Script')

#trend_payload = {'q': 'GMO, Genetically Modified Organism, Transgenic', 'cat': '0-71'}
trend_payload = {'q': str(term), 'cat': '0-71'}

# trend
trend = pytrend.trend(trend_payload)
print(trend)

#here is the data that is used to generate the google trend line plot
df = pytrend.trend(trend_payload, return_type='dataframe')
print(df)
    
########################################################################
### toprelated
##toprelated = pytrend.related(trend_payload, related_type='top')
##print(toprelated)
##risingrelated = pytrend.related(trend_payload, related_type='rising')
##print(risingrelated)
##
### top30in30
##top30in30 = pytrend.top30in30()
##print(top30in30)

##country_payload = {'geo': 'US'}
### hottrends
##hottrends = pytrend.hottrends(country_payload)
##print(hottrends)
##
### hottrendsdetail
### returns XML data
##hottrendsdetail = pytrend.hottrendsdetail(country_payload)
##print(hottrendsdetail)
##
##payload = {'date': '201601', 'geo': 'US'}
### alltopcharts
##topcharts = pytrend.topcharts(payload)
##print(topcharts)
##
