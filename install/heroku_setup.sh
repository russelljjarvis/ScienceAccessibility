#!/bin/bash
# https://gist.github.com/mikesmullin/2636776
#
# download and install latest geckodriver for linux or mac.
# required for selenium to drive a firefox browser.
sudo apt-get update
sudo apt-get install jq wget chromium-chromedriver

# firefox

#json=$(curl -s https://api.github.com/repos/mozilla/geckodriver/releases/latest)
#url=$(echo "$json" | jq -r '.assets[].browser_download_url | select(contains("linux64"))')
#curl -s -L "$url" | tar -xz
#chmod +x geckodriver
#sudo cp geckodriver .
#sudo cp geckodriver ./app
#export PATH=$PATH:$pwd/geckodriver
#echo PATH


sudo python3 -m pip install -r requirements.txt
sudo python3 -m pip install seaborn 
sudo python3 -m pip install bs4
sudo python3 -m pip install natsort dask plotly
sudo python3 -c "import nltk; nltk.download('punkt')"
sudo python3 -c "import nltk; nltk.download('stopwords')"

#git clone https://github.com/ckreibich/scholar.py.git

wget https://www.dropbox.com/s/3h12l5y2pn49c80/traingDats.p?dl=0
wget https://www.dropbox.com/s/crarli3772rf3lj/more_authors_results.p?dl=0
wget https://www.dropbox.com/s/x66zf52himmp5ox/benchmarks.p?dl=0
# sudo apt-get install -y firefox
#wget https://ftp.mozilla.org/pub/firefox/releases/45.0.2/linux-x86_64/en-GB/firefox-45.0.2.tar.bz2
#tar xvf firefox-45.0.2.tar.bz2
#
#sudo mv /usr/bin/firefox /usr/bin/firefox-backup
#rm /usr/bin/firefox
#sudo mv firefox/ /usr/lib/firefox
#sudo ln -s /usr/lib/firefox /usr/bin/firefox



#which firefox

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


