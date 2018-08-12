

if TOURNAMENT:
    SEARCHLIST, se_, LINKSTOGET = search_known_corpus()
    flat_iter = [ category for category in SEARCHLIST ]
    # traverse this list randomly as hierarchial traversal may be a bot give away.
    random.shuffle(flat_iter)
    # flat_iter = [ (se[4],f) for f in flat_iter ]
    flat_iter = iter( (se[4],f) for f in flat_iter )


if TOURNAMENT:
    # naturally sort a list of files, as machine sorted is not the desired file list hierarchy.
    rick = natsorted(glob.glob(str(os.getcwd())+'/*rcgerkin*.html'))
    rick.extend(natsorted(glob.glob(str(os.getcwd())+'/*rcgerkin*.pdf')))
    sharon = natsorted(glob.glob(str(os.getcwd())+'/*scrook**.html'))
    sharon.extend(natsorted(glob.glob(str(os.getcwd())+'/*scrook*.pdf')))
    sarah = natsorted(glob.glob(str(os.getcwd())+'/*jarvis**.html'))
    sarah.extend(natsorted(glob.glob(str(os.getcwd())+'/*jarvis*.pdf')))

    print(sarah)
    grid0 = db.from_sequence(rick)
    grid1 = db.from_sequence(sharon)
    grid2 = db.from_sequence(sarah)
    rick = list(db.map(convert_to_text,grid0).compute())
    sharon = list(db.map(convert_to_text,grid1).compute())
    sarah = list(db.map(convert_to_text,grid2).compute())
    competition = [ (str('rcgerkin'),rick),(str('smcrook'),sharon) ] #,sarah]
    for author_name,author_texts in competition:
        for text in author_texts:
            if author_name in text:
                pdb.set_trace()
    print(sarah)

    with open('tournment.p','wb') as handle:
        pickle.dump([sarah,rick,sharon,benchmarks],handle)

    urlDats.extend(sharon)
    urlDats.extend(rick)
    urlDats.extend(sarah)

    urlDats = list(filter(lambda url: len(list(url))>3, urlDats))
    urlDats = list(filter(lambda url: len(list(url.keys()))>3, urlDats))
    urlDats = list(filter(lambda url: str('gf') in url.keys(), urlDats))

    ranked = sorted(urlDats, key=lambda w: w['penalty'])   # sort by age
    sharon_mean = np.mean([r['gf'] for r in ranked if 'scrook' in r['link']])
    rick_mean = np.mean([r['gf'] for r in ranked if 'rcgerkin' in r['link']])
    sarah_mean = np.mean([r['gf'] for r in ranked if 'jarvis' in r['link']])
