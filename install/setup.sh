#!/bin/bash
# https://gist.github.com/mikesmullin/2636776
#
# download and install latest geckodriver for linux or mac.
# required for selenium to drive a firefox browser.
sudo apt-get update
#sudo apt-get install jq wget chromium-chromedriver firefox


sudo python3 -m pip install -r requirements.txt
sudo python3 -c "import nltk; nltk.download('punkt')"
sudo python3 -c "import nltk; nltk.download('stopwords')"
#sudo conda install -c plotly plotly=4.8.1
#git clone https://github.com/ckreibich/scholar.py.git

wget https://www.dropbox.com/s/3h12l5y2pn49c80/traingDats.p?dl=0
wget https://www.dropbox.com/s/crarli3772rf3lj/more_authors_results.p?dl=0
wget https://www.dropbox.com/s/x66zf52himmp5ox/benchmarks.p?dl=0
# sudo apt-get install -y firefox
#wget https://ftp.mozilla.org/pub/firefox/releases/45.0.2/linux-x86_64/en-GB/firefox-45.0.2.tar.bz2

sudo python3 install/align_data_sources.py
sudo python3 setup.py install

mkdir -p ~/.streamlit/
echo "\
[general]\n\
email = \"rjjarvis@asu.edu\"\n\
" > ~/.streamlit/credentials.toml
echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml


