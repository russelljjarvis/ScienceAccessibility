
sudo apt-get update
sudo apt-get install --fix-missing
sudo /opt/conda/bin/pip install git+https://github.com/pdfminer/pdfminer.six.git

sudo /opt/conda/bin/pip install -U natsort
sudo /opt/conda/bin/pip install -U radon

sudo /opt/conda/bin/pip install -U pycld2
sudo /opt/conda/bin/pip install -U beautifulsoup4
sudo /opt/conda/bin/pip install -U git+https://github.com/nuncjo/Delver
/opt/conda/bin/pip install nltk
python -c "import nltk; nltk.download('punkt');from nltk import word_tokenize,sent_tokenize"
python -c "import nltk; nltk.download('averaged_perceptron_tagger')"
/opt/conda/bin/pip install textstat
/opt/conda/bin/pip install tabulate
/opt/conda/bin/pip install textblob/opt/conda/bin/pip install selenium wordcloud

python -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger')"
