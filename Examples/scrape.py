# Scientific readability project
# authors: other authors,
# ...,
# Russell Jarvis
# https://github.com/russelljjarvis/
# rjjarvis@asu.edu


# for some reason the docker build does not properly install the fake user_agent, oh well do it again here
# NB move this to the Docker container

import selenium
from pyvirtualdisplay import Display
from selenium import webdriver
from fake_useragent import UserAgent

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

from GoogleScraper import scrape_with_config, GoogleSearchError

from SComplexity.utils_and_paramaters import search_params, engine_dict_list, search_known_corpus
from numpy import random
import os
from delver import Crawler
c = Crawler()

COMPETITION = False
if COMPETITION:
    SEARCHLIST, WEB, LINKSTOGET = search_known_corpus()
    se, _ = engine_dict_list()
    flat_iter = [ category for category in SEARCHLIST ]
    # traverse this list randomly as hierarchial traversal may be a bot give away.
    random.shuffle(flat_iter)
    flat_iter = [(4,f) for f in flat_iter ]

else:
    SEARCHLIST, WEB, LINKSTOGET = search_params()
    se, _ = engine_dict_list()
    flat_iter = [ (b,category) for category in SEARCHLIST for b in range(0,4) ]
    # traverse this list randomly as hierarchial traversal may be a bot give away.
    random.shuffle(flat_iter)

def scrapelandtext(fi):
    b,category = fi
    config = {}
    driver = rotate_profiles()
	# This code block, jumps over fence one (the search engine as a gatekeeper)
    # google scholar or wikipedia is not supported by google scraper
    # duckduckgo bang expansion can be used as to access engines that GS does not support.
    # for example twitter etc

    config['keyword'] = str(category)
    if b==4: config['keyword'] = str('!scholar ')+str(category)
    if b==3: config['keyword'] = str('!wiki ')+str(category)

    config['search_engine'] = str(se[b])
    config['scrape_method'] = str('selenium')
    config['num_pages_for_keyword'] = 10
    config['use_own_ip'] = True
    config['sel_browser'] = str('firefox')
    config['do_caching'] = False # bloat warning.

    # Search Engine: 'who are you?' code: 'I am an honest human centric browser, and certainly note a robot surfing in the nude'. Search Engine: 'good, here are some pages'.
    # Time elapses and the truth is revealed just like in 'the Emperors New Clothes'.

    # The file crawl.py contains methods for crawling the scrapped links.
    # For this reason, a subsequent action, c.download (crawl download ) is ncessary.

    config['output_filename'] = str(category)+str(' ')+str(se[b])+str('.csv')
    path_link_map ={}
    try:
        search = scrape_with_config(config)
        links = []
        for serp in search.serps:
            links.extend([link.link for link in serp.links])
		# This code block jumps over fench two
        # The (possibly private, or hosted server as a gatekeeper).
        try:
            for index, link in enumerate(links):
                # Bulk download wht is scrapped by GS.
                if str('pdf') in link:
                    local_file_path = c.download(local_path=os.getcwd(),url=link,name=str(category)+str(se[b])+str(index)+str('.pdf'))
                else:
                    local_file_path = c.download(local_path=os.getcwd(),url=link,name=str(category)+str(se[b])+str(index)+str('.html'))
                path_link_map[str(link)] = local_file_path
                os.path.isfile(local_file_path)
        except:
            pass

    except GoogleSearchError as e:
        print(e)
    return path_link_map

# Use this variable to later reconcile file names with urls
# As there was no, quick and dirty way to bind the two togethor here, without complicating things later.
path_link_maps = list(map(scrapelandtext,flat_iter))
with open('path_link_maps.p','wb') as f: pickle.dump(path_link_maps,f)
