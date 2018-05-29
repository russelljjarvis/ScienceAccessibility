# Scientific readability project
# authors: other_authors
# Russell Jarvis
# https://github.com/russelljjarvis/
# rjjarvis@asu.edu
import pycld2 as cld2
import lzma
from crawl import html_to_txt, convert_pdf_to_txt
import os
def convert_to_text(fileName):
    b = os.path.getsize(fileName)
    urlDat = {}
    if b>250: # this is just to prevent reading in of incomplete data.
        try:
            file = open(fileName)
            if str('.html') in fileName:
                text = html_to_txt(file)
            else:
                text = convert_pdf_to_txt(file)
            #file.close()
            urlDat = {'link':fileName}
            urlDat = text_proc(text,urlDat)
            print(urlDat)
        except:
            pass
    return urlDat


def comp_ratio(test_string):
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

def print_best_text(fileName):
    file = open(fileName)
    if str('.html') in fileName:
        text = html_to_txt(file)
    else:
        text = convert_pdf_to_txt(file)
    file.close()
    return text


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
    #print(check_with)
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

'''
depreciated
def purge(fi,filter_string=''):

    If filter string is not defined, the method will probably delete all data.
    Delete caches if suspect that full of rubbish
    This will create a lot of non fatal errors, since I was too lazy to write this function properly

    import os
    b,category = fi
    categoryquery = category.replace(' ',"+")
    path = os.getcwd() + '/' +  str(category) +'/'

    if os.path.exists(path):
        os.chdir(path)
        os.system('rm '+filter+'*.csv')
        print('purging cached data')
    else:
        os.makedirs(path)
        os.chdir(path)

def mkdirs(fi,filter_string=''):

    If filter string is not defined, the method will probably delete all data.
    Delete caches if suspect that full of rubbish
    This will create a lot of non fatal errors, since I was too lazy to write this function properly

    import os
    b,category = fi
    categoryquery = category.replace(' ',"+")
    path = os.getcwd() + '/' +  str(category) +'/'

    if os.path.exists(path):
        pass
    else:
        os.makedirs(path)

def compute_authors(author_results):
    for author,links in authors.items():
        for r in links:
            fr = FetchResource(r)
            corpus = fr.run()
            if corpus is not None and not black_string(corpus):
                urlDat = {'link':r}
                urlDat = text_proc(corpus,urlDat,WORD_LIM = 100)
                if str(r) not in author_results.keys():
                    author_results[author][str(r)] = urlDat
                else:
                    author_results[author][str(r)] = urlDat
        print(author_results)
    return author_results
'''
