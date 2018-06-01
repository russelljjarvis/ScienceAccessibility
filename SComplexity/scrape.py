# Scientific readability project
# authors: other authors,
# ...,
# Russell Jarvis
# https://github.com/russelljjarvis/
# rjjarvis@asu.edu
import selenium
from pyvirtualdisplay import Display
from selenium import webdriver
from fake_useragent import UserAgent
from numpy import random
import os
from delver import Crawler
from GoogleScraper import scrape_with_config, GoogleSearchError



from SComplexity.utils_and_paramaters import search_params, engine_dict_list, search_known_corpus

C = Crawler()
CWD = os.getcwd()

display = Display(visible=0, size=(1024, 768))
display.start()


useragent = UserAgent()
# Rotate through random user profiles.
profile = webdriver.FirefoxProfile()

def rotate_profiles():
    driver = None
    profile.set_preference("general.useragent.override", useragent.random)
    profile.set_preference("javascript.enabled", True)
    driver = webdriver.Firefox(firefox_profile=profile)
    return driver
driver = rotate_profiles()

def url_to_file(link_tuple):
    se_b,index,link,category = link_tuple
    print(link_tuple)
    fname = '{0}_{1}_{2}'.format(category,se_b,index)
    # Bulk download wht is scrapped by GS.
    if str('pdf') in link:
        fname = fname.join(str('.pdf'))
    if str('html') in link:
        fname = fname.join(str('.html'))
    # note it's possible that downloaded link is neither html, nor pdf (ie jpg). Incorrectly assigning extensions to such resources will cause
    # problems further down the road.
    local_file_path = C.download(local_path = CWD, url = link, name = fname)
    os.path.isfile(local_file_path)
    plm = { fname:link}
    return plm

def scrapelandtext(fi):
    se_, b,category = fi
     #= se[b]

    config = {}
    driver = rotate_profiles()
	# This code block, jumps over fence one (the search engine as a gatekeeper)
    # google scholar or wikipedia is not supported by google scraper
    # duckduckgo bang expansion can be used as to access engines that GS does not support.
    # for example twitter etc

    config['keyword'] = str(category)
    if b==4: config['keyword'] = '!scholar {0}'.format(category)
    if b==3: config['keyword'] = '!wiki {0}'.format(category)
    config['search_engine'] = str(se_)
    config['scrape_method'] = 'selenium'
    config['num_pages_for_keyword'] = 10
    config['use_own_ip'] = True
    config['sel_browser'] = 'firefox'
    config['do_caching'] = False # bloat warning.

    # Google scrap + selenium implements a lot of human centric browser masquarading tools.
    # Search Engine: 'who are you?' code: 'I am an honest human centric browser, and certainly note a robot surfing in the nude'. Search Engine: 'good, here are some pages'.
    # Time elapses and the reality is exposed just like in 'the Emperors New Clothes'.
    # The file crawl.py contains methods for crawling the scrapped links.
    # For this reason, a subsequent action, c.download (crawl download ) is ncessary.

    config['output_filename'] = '{0}_{1}.csv'.format(category,se_)
    plm = {}
    search = scrape_with_config(config)

    try:
        search = scrape_with_config(config)

        links = []
        for serp in search.serps:
            links.extend([link.link for link in serp.links])
	# This code block jumps over gate two
        # The (possibly private, or hosted server as a gatekeeper).
        try:
            get_links = [(se_,index,link,category) for index, link in enumerate(links)]
            plms = list(map(url_to_file,get_links))
            for p in plms:
                plm.update(p)
                print(p)
        except:
           plm = None

    except GoogleSearchError as e:
        print(e)
    return plm

# Use this variable to later reconcile file names with urls
# As there was no, quick and dirty way to bind the two togethor here, without complicating things later.
COMPETITION = False
se, _ = engine_dict_list()

if COMPETITION:
    SEARCHLIST, WEB, LINKSTOGET = search_known_corpus()
    flat_iter = [ category for category in SEARCHLIST ]
    # traverse this list randomly as hierarchial traversal may be a bot give away.
    random.shuffle(flat_iter)
    flat_iter = [ (4,f) for f in flat_iter ]

else:
    SEARCHLIST, WEB, LINKSTOGET = search_params()
    flat_iter = [ (b,category) for category in SEARCHLIST for b in range(0,4) ]
    # traverse this list randomly as hierarchial traversal may be a bot give away.
    random.shuffle(flat_iter)
    #flat_iter = iter(flat_iter)

path_link_maps = list(map(scrapelandtext,flat_iter))
with open('path_link_maps.p','wb') as f: pickle.dump(path_link_maps,f)
