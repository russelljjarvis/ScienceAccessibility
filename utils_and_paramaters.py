

def map_wrapper(function_item,list_items):
    from dask.distributed import Client
    import dask.bag as db
    c = Client()
    NCORES = len(c.ncores().values())
    b0 = db.from_sequence(list_items, npartitions=NCORES)
    list_items = list(db.map(function_item,b0).compute())
    return list_items

def engine_dict_list():
    se = {0:"google",1:"yahoo",2:"duckduckgo",3:"ask",4:"scholar"}

    return se, list(se.values())

def search_params():
    SEARCHLIST = ["autosomes","respiration", "bacteriophage",'Neutron','Vaccine','Transgenic','GMO','Genetically Modified Organism','neuromorphic hardware']
    WEB = 6#how many search engines to include (4 possible- google google scholar bing yahoo)
    LINKSTOGET= 10 #number of links to pull from each search engine (this can be any value, but more processing with higher number)
    return SEARCHLIST, WEB, LINKSTOGET

def black_string(check_with):
    #print(check_with)
    if len(check_with) == 1145:
        print('suspicious')
        #print(check_with)
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


def purge(fi,filter_string=''):
    '''
    If filter string is not defined, the method will probably delete all data.
    Delete caches if suspect that full of rubbish
    This will create a lot of non fatal errors, since I was too lazy to write this function properly
    '''
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
    '''
    If filter string is not defined, the method will probably delete all data.
    Delete caches if suspect that full of rubbish
    This will create a lot of non fatal errors, since I was too lazy to write this function properly
    '''
    import os
    b,category = fi
    categoryquery = category.replace(' ',"+")
    path = os.getcwd() + '/' +  str(category) +'/'

    if os.path.exists(path):
        pass
    else:
        os.makedirs(path)

    # the idea is that grid and flat iter should be very similar.
    # grid is a bit more maintainable and conventional way of building iterators.
