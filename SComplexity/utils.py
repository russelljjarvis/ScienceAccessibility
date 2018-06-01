# Scientific readability project
# authors: other_authors
# Russell Jarvis
# https://github.com/russelljjarvis/
# rjjarvis@asu.edu

#from .t_analysis import text_proc
#from .crawl import html_to_txt, convert_pdf_to_txt
import os

import pycld2 as cld2
import lzma

def convert_to_text(fileName):
    b = os.path.getsize(fileName)
    urlDat = {}
    if b>250: # this is just to prevent reading in of incomplete data.
        try:
            file = open(fileName)
            if str('.html') in fileName:
                text = html_to_txt(file)
            elif str('.pdf') in fileName:
                text = convert_pdf_to_txt(file)
            else:
                return None
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
