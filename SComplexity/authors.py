#import scholar
from SComplexity.scholar_scrape import scholar
def search_author(author):
    # from https://github.com/ckreibich/scholar.py/issues/80                                                                                                                                                                                  
    #se_,index,category,category,buff = get_links
    querier = scholar.ScholarQuerier()
    settings = scholar.ScholarSettings()
    querier.apply_settings(settings)
    query = scholar.SearchScholarQuery()

    query.set_words(str('author:')+author)
    querier.send_query(query)
    print(dir(querier))
    import pdb
    pdb.set_trace()
    #cits = [ a.get_citation_data() for a in querier.articles ]
    #cit = querier.get_citation_data()
    links = [ a.attrs['url'][0] for a in querier.articles if a.attrs['url'][0] is not None ]
    return links


rgerkin,cits = search_author('R Gerkin')
print(rgerkin,cits)
    #links = query.get_url()                                                                                                                                                                                                                  
    #print(links)                                                                                                                                                                                                                             
    #if len(links) > NUM_LINKS: links = links[0:NUM_LINKS]                                                                                                                                                                                    

    #[ process((se_,index,l,category,buff)) for index,l in enumerate(links) ]

