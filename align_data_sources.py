
import nltk
try:
    from nltk.corpus import stopwords
    stop_words = stopwords.words('english')
except:
    nltk.download('punkt')
    nltk.download('stopwords')

if not(os.path.exists('traingDats.p?dl=0') or os.path.exists('data/traingDats.p')):

    os.system('wget https://www.dropbox.com/s/3h12l5y2pn49c80/traingDats.p?dl=0')
    os.system('wget https://www.dropbox.com/s/x66zf52himmp5ox/benchmarks.p?dl=0')

if os.path.exists("traingDats.p?dl=0") and not os.path.exists("data/traingDats.p"):
    os.system('mv traingDats.p?dl=0 data/traingDats.p')
    os.system('mv benchmarks.p?dl=0 data/benchmarks.p')
