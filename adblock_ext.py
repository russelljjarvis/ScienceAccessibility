#https://github.com/scrapinghub/adblockparser
!pip install adblockparser
!pip install git+https://github.com/axiak/pyre2.git#egg=re2

!wget https://easylist-downloads.adblockplus.org/easylist.txt
!raw_rules = open('easylist.txt','r');
from adblockparser import AdblockRules;
rules = AdblockRules(raw_rules.readlines())"
