FILES = natsorted(glob.glob(str(os.getcwd())+'*.p'))
sci1 = pickle.load(open('author_results.p','rb'))
sci2 = pickle.load(open('traingDats.p','rb'))
science = []
science.extend(sci1)
science.extend(sci2)
mixture = []
mix1 = pickle.load(open('scraped_new.p','rb'))
mix2 = pickle.load(open('reference.p','rb'))
mix3 = pickle.load(open('benchmarks.p','rb'))
mixture.extend(mix1)
mixture.extend(mix2)
mixture.extend(mix3)
