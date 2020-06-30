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


def isPassive(sentence):
    # https://github.com/flycrane01/nltk-passive-voice-detector-for-English/blob/master/Passive-voice.py
    beforms = ['am', 'is', 'are', 'been', 'was', 'were', 'be', 'being']               # all forms of "be"
    aux = ['do', 'did', 'does', 'have', 'has', 'had']                                  # NLTK tags "do" and "have" as verbs, which can be misleading in the following section.
    words = nltk.word_tokenize(sentence)
    tokens = nltk.pos_tag(words)
    tags = [i[1] for i in tokens]
    if tags.count('VBN') == 0:                                                            # no PP, no passive voice.
        return False
    elif tags.count('VBN') == 1 and 'been' in words:                                    # one PP "been", still no passive voice.
        return False
    else:
        pos = [i for i in range(len(tags)) if tags[i] == 'VBN' and words[i] != 'been']  # gather all the PPs that are not "been".
        for end in pos:
            chunk = tags[:end]
            start = 0
            for i in range(len(chunk), 0, -1):
                last = chunk.pop()
                if last == 'NN' or last == 'PRP':
                    start = i                                                             # get the chunk between PP and the previous NN or PRP (which in most cases are subjects)
                    break
            sentchunk = words[start:end]
            tagschunk = tags[start:end]
            verbspos = [i for i in range(len(tagschunk)) if tagschunk[i].startswith('V')] # get all the verbs in between
            if verbspos != []:                                                            # if there are no verbs in between, it's not passive
                for i in verbspos:
                    if sentchunk[i].lower() not in beforms and sentchunk[i].lower() not in aux:  # check if they are all forms of "be" or auxiliaries such as "do" or "have".
                        break
                else:
                    return True
    return False




def argument_density(sentence0,sentence1):
    # https://github.com/flycrane01/nltk-passive-voice-detector-for-English/blob/master/Passive-voice.py
    CLAIMS = ['I think that', 'I believe that']               # all forms of "be"
    CAUSAL = ['because','so','thus','therefore','since']                                  # NLTK tags "do" and "have" as verbs, which can be misleading in the following section.
    terms = nltk.word_tokenize(sentence1)
    #tokens = nltk.pos_tag(terms)
    befores = []
    for t in terms:
        if t in CAUSAL:
            befores.append(sentence0)
    return befores



        #for C in CAUSAL:
        #    if

    '''
    tags = [i[1] for i in tokens]
    if tags.count('VBN') == 0:                                                            # no PP, no passive voice.
        return False
    elif tags.count('VBN') == 1:                                    # one PP "been", still no passive voice.
        return False
    else:
        pos = [i for i in range(len(tags)) if tags[i] == 'VBN' and words[i] != 'been']  # gather all the PPs that are not "been".
        for end in pos:
            chunk = tags[:end]
            start = 0
            for i in range(len(chunk), 0, -1):
                last = chunk.pop()
                if last == 'NN' or last == 'PRP':
                    start = i                                                             # get the chunk between PP and the previous NN or PRP (which in most cases are subjects)
                    break
            sentchunk = words[start:end]
            tagschunk = tags[start:end]
            verbspos = [i for i in range(len(tagschunk)) if tagschunk[i].startswith('V')] # get all the verbs in between
            if verbspos != []:                                                            # if there are no verbs in between, it's not passive
                for i in verbspos:
                    if sentchunk[i].lower() not in beforms and sentchunk[i].lower() not in aux:  # check if they are all forms of "be" or auxiliaries such as "do" or "have".
                        break
                else:
                    return True
    return False
    '''

def convert_pdf_to_txt(content):
    pdf = io.BytesIO(content.content)
    parser = PDFParser(pdf)
    document = PDFDocument(parser, password=None) # this fails
    write_text = ''
    for page in PDFPage.create_pages(document):
        interpreter.process_page(page)
        write_text +=  retstr.getvalue()
        #write_text = write_text.join(retstr.getvalue())
    # Process all pages in the document
    text = str(write_text)
    return text

def html_to_txt(content):
    soup = BeautifulSoup(content, 'html.parser')
    #strip HTML
    for script in soup(["script", "style"]):
        script.extract()    # rip it out
    text = soup.get_text()
    #organize text
    lines = (line.strip() for line in text.splitlines())  # break into lines and remove leading and trailing space on each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  ")) # break multi-headlines into a line each
    text = '\n'.join(chunk for chunk in chunks if chunk) # drop blank lines
    str_text = str(text)
    return str_text

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
    '''
    hardcoded links to get. journal seek is a data base of known academic journals.
    '''
    LINKSTOGET = []
    PUBLISHERS = str('https://journalseek.net/publishers.htm')
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
    return PUBLISHERS, WEB, LINKSTOGET





def clue_links(check_with):
    '''
    The goal of this function/string comparison
    is just to give a clue, about whether the text is
    an official scientific publication, or a blog, or psuedo science publication
    It is not meant to act as a definitive classifier.
    '''
    # TODO query with pyhthon crossref api

    # https://pypi.org/project/crossrefapi/1.0.7/
    CHECKS = [str('.fda'),str('.epa'),str('.gov'),str('.org'),str('.nih'),str('.nasa'),str('.pdf')]
    assume_false = []
    for check in CHECKS:
        if check in check_with:
            assume_false.append(check)
    if len(assume_false) == 1:
        return (True, assume_false)
    else:
        return (False, assume_false)


def publication_check(wt):
    '''
    The goal of this function/string comparison
    is just to give a clue, about whether the text is
    an official scientific publication, or a blog, or psuedo science publication
    It is not meant to act as a definitive classifier.
    '''
    publication = {}
    if 'issn' in wt:
        publication['issn'] = wt.split("issn",1)[1]
    if 'isbn' in wt:
        publication['isbn'] = wt.split("isbn",1)[1]
    if 'pmid' in wt:
        publication['pmid'] = wt.split("pmid",1)[1]
    for k,v in publication.items():
        publication[k] = v[0:15]

    if len(publication) >= 1:
        return (True, publication)
    else:
        return (False, publication)


def clue_words(check_with):
    '''
    The goal of this function/string comparison
    is just to give a clue, about whether the text is an official scientific publication, or a blog, or psuedo science publication
    It is not meant to act as a definitive classifier.
    To get ISSN (for any format) there is a national center in each country.
    It may be National Library in some cases. List of National ISSN centers are listed in issn website.
    For DOI, there are representatives in western countries, also you can apply to doi.org or crossref.org.
    How are the e-ISSN Number, DOI and abbreviation provided for a new journal ?.
    Available from: https://www.researchgate.net/post/How_are_the_e-ISSN_Number_DOI_and_abbreviation_provided_for_a_new_journal [accessed Apr 7, 2015].
    '''
    #TODO query with pyhthon crossref api
    # https://pypi.org/project/crossrefapi/1.0.7/
    # check_with should be lower cse now

    CHECKS = [str('isbn'),str("issn"),str("doi"),str('volume'),str('issue'), \
    str("journal of"),str("abstract"),str("materials and methods"),str("nature"), \
    str("conflict of interest"), str("objectives"), str("significance"), \
    str("published"), str("references"), str("acknowledgements"), str("authors"), str("hypothesis"), \
    str("nih"),str('article'),str('affiliations'),str('et al')]
    assume_false = []
    for check in CHECKS:
        if check in check_with:
            assume_false.append(check)
    if len(assume_false) >= 6:
        return (True, assume_false)
    else:
        return (False, assume_false)


def argument_density(check_with):
    density_histogram = {}
    # https://github.com/flycrane01/nltk-passive-voice-detector-for-English/blob/master/Passive-voice.py
    CLAIMS = ['I think that', 'I believe that']               # all forms of "be"
    CAUSAL = ['because','so','thus','therefore','since']                                  # NLTK tags "do" and "have" as verbs, which can be misleading in the following section.
    for c in CLAIMS:
        if c in check_with:
            density_histogram[c] += 1
    for c in CAUSAL:
        if c in check_with:
            density_histogram[c] += 1
    return density_histogram



def black_string(check_with):
    if len(check_with) == 1145:
        return True
    #check="Privacy_policy"
    #if check in check_with:
    #    return True
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
