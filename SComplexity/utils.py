# Scientific readability project
# authors: other_authors
# Russell Jarvis
# https://github.com/russelljjarvis/
# rjjarvis@asu.edu

# Patrick McGurrin
# patrick.mcgurrin@gmail.com

import os

import pycld2 as cld2
import lzma


def comp_ratio(test_string):
    # If we are agnostic about what the symbols are, and we just observe the relative frequency of each symbol.
    # The distribution of frequencies would make some texts harder to compress, even if we don't know what the symbols mean.
    # http://www.beamreach.org/data/101/Science/processing/Nora/Papers/Information%20entropy%20o%20fjumpback%20whale%20songs.pdf

    c = lzma.LZMACompressor()
    bytes_in = bytes(test_string,'utf-8')
    bytes_out = c.compress(bytes_in)
    return len(bytes_out)/len(bytes_in)

def english_check(corpus):

    # It's not that we are cultural imperialists, but the people at textstat, and nltk may have been,
    # so we are also forced into this tacit agreement.
    # Japanese characters massively distort information theory estimates, as they are potentially very concise.
    _, _, details = cld2.detect(' '.join(corpus), bestEffort=True)
    detectedLangName, _ = details[0][:2]
    return bool(detectedLangName == 'ENGLISH')

def engine_dict_list():
    se = {0:"google",1:"yahoo",2:"duckduckgo",3:"wikipedia",4:"scholar",5:"bing"}
    return se, list(se.values())

def search_params():
    SEARCHLIST = ["autosomes","respiration", "bacteriophage",'Neutron','Vaccine','Transgenic','GMO','Genetically Modified Organism','neuromorphic hardware', 'mustang unicorn', 'scrook rgerkin neuron', 'prancercise philosophy', 'play dough delicious deserts']
    _, ses = engine_dict_list()
    WEB = len(ses) #how many search engines to include (many possible- google google scholar bing yahoo)
    LINKSTOGET= 10 #number of links to pull from each search engine (this can be any value, but more processing with higher number)
    return SEARCHLIST, WEB, LINKSTOGET

def search_known_corpus():
    SEARCHLIST = []
    LINKSTOGET = []
    SEARCHLIST = [str('rcgerkin'),str('smcrook'), str('s jarvis optogenetics'), str('Patrick mcgurrin ASU'), str('Melanie jarvis neonate')]
    LINKSTOGET = []
    LINKSTOGET.append(str('https://academic.oup.com/beheco/article-abstract/29/1/264/4677340'))
    LINKSTOGET.append(str('http://splasho.com/upgoer5/library.php'))
    LINKSTOGET.append(str('https://elifesciences.org/download/aHR0cHM6Ly9jZG4uZWxpZmVzY2llbmNlcy5vcmcvYXJ0aWNsZXMvMjc3MjUvZWxpZmUtMjc3MjUtdjIucGRm/elife-27725-v2.pdf?_hash=WA%2Fey48HnQ4FpVd6bc0xCTZPXjE5ralhFP2TaMBMp1c%3D'))
    LINKSTOGET.append(str('https://scholar.google.com/scholar?hl=en&as_sdt=0%2C3&q=Patrick+mcgurrin+ASU&btnG='))
    LINKSTOGET.append(str('https://scholar.google.com/citations?user=GzG5kRAAAAAJ&hl=en&oi=sra'))
    LINKSTOGET.append(str('https://scholar.google.com/citations?user=xnsDhO4AAAAJ&hl=en&oe=ASCII&oi=sra'))
    LINKSTOGET.append(str('https://scholar.google.com/citations?user=2agHNksAAAAJ&hl=en&oi=sra'))
    #_, ses = engine_dict_list()
    WEB = 1
    #WEB = len(ses) #how many search engines to include (many possible- google google scholar bing yahoo)
    LINKSTOGET= 10 #number of links to pull from each search engine (this can be any value, but more processing with higher number)
    return SEARCHLIST, WEB, LINKSTOGET


def convert_and_score(fileName):
    b = os.path.getsize(fileName)
    text = None
    try: # this is just to prevent reading in of incomplete data.
        file = open(fileName)
        print(file)
        if str('.html') in fileName:
            text = html_to_txt(file)
        elif str('.pdf') in fileName:
            text = convert_pdf_to_txt(file)
        else:
            print('other')
        file.close()
        urlDat = {'link':fileName}
        urlDat = text_proc(text,urlDat)
        print(urlDat)
    except:
        urlDat = {'link':fileName}
    return urlDat




def science_string(check_with):
    # check_with should be lower cse now
    checks=[str("abstract"),str("methods"),str("results")]
    assume_false = False
    for check in checks:
        if check in check_with:
            assume_false = True
        else:
            return False
    return assume_false

def black_string(check_with):
    if len(check_with) == 1145:
        return True
    check="Our systems have detected unusual traffic from your computer network.\\nThis page checks to see if it\'s really you sending the requests, and not a robot.\\nWhy did this happen?\\nThis page appears when Google automatically detects requests coming from your computer network which appear to be in violation of the Terms of Service. The block will expire shortly after those requests stop.\\nIn the meantime, solving the above CAPTCHA will let you continue to use our services.This traffic may have been sent by malicious software, a browser plug in, or a script that sends automated requests.\\nIf you share your network connection, ask your administrator for help  a different computer using the same IP address may be responsible.\\nLearn moreSometimes you may be asked to solve the CAPTCHA if you are using advanced terms that robots are known to use, or sending requests very quickly."
    if check in check_with:
        return True
    check="Google ScholarLoading...The system can't perform the operation now."
    if check in check_with:
        return True
    check="Please show you're not a robotSorry, we can't verify that you're not a robot when"
    if check in check_with:
        return True
    check=" JavaScript is turned off.Please enable JavaScript in your browser and reload this page.HelpPrivacyTerms"
    if check in check_with:
        return True
    if check in check_with:
        return True
    check = "\\x00\\x00\\x00\\x00"
    if check in check_with:
        return True
    check = "Please click here if you are not redirected within a few seconds."
    if check in check_with:
        return True
    check="DuckDuckGo  Privacy, simplified.\\nAbout DuckDuckGo\\nDuck it!\\nThe search engine that doesn\'t track you.\\nLearn More."
    if check in check_with:
        return True
    return False


###
# Duplicate for complexity measures only
###

def slat_(self,config):
    try:
        search = scrape_with_config(config)

        links = []
        for serp in search.serps:
            print(serp)
            links.extend([link.link for link in serp.links])
        # This code block jumps over gate two
        # The (possibly private, or hosted server as a gatekeeper).
        if len(links) > self.NUM_LINKS: links = links[0:self.NUM_LINKS]
        if len(links) > 0:
            buffer = None
            get_links = ((se_,index,link,category,buffer) for index, link in enumerate(links) )
            # map over the function in parallel since it's 2018
            b = db.from_sequence(get_links,npartitions=8)
            _ = list(db.map(process,b).compute())

    except GoogleSearchError as e:
        print(e)
        return None
    print('done scraping')

###
# Duplicate for complexity measures only
###


def scrapelandtext(self,fi):
    se_,category = fi
    config = {}
    driver = rotate_profiles()
	# This code block, jumps over gate one (the search engine as a gatekeeper)
    # google scholar or wikipedia is not supported by google scraper
    # duckduckgo bang expansion can be used as to access engines that GS does not support.
    # for example twitter etc

    config['keyword'] = str(category)

    if str('scholar') in se_: config['keyword'] = '!scholar {0}'.format(category)
    if str('wiki') in se_ : config['keyword'] = '!wiki {0}'.format(category)
    if str('scholar') in se_ or str('wiki') in se_:
        config['search_engines'] = 'duckduckgo'
    else:
        config['search_engines'] = se_

    config['scrape_method'] = 'selenium'
    config['num_pages_for_keyword'] = 1
    config['use_own_ip'] = True
    config['sel_browser'] = 'firefox'
    config['do_caching'] = False # bloat warning.

    # Google scrap + selenium implements a lot of human centric browser masquarading tools.
    # Search Engine: 'who are you?' code: 'I am an honest human centric browser, and certainly note a robot surfing in the nude'. Search Engine: 'good, here are some pages'.
    # Time elapses and the reality is exposed just like in 'the Emperors New Clothes'.
    # The file crawl.py contains methods for crawling the scrapped links.
    # For this reason, a subsequent action, c.download (crawl download ) is ncessary.

    config['output_filename'] = '{0}_{1}.csv'.format(category,se_)

    self.slat_(config)
    return
