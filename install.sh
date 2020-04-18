# https://gist.github.com/mikesmullin/2636776
# 
#!/bin/bash
# download and install latest geckodriver for linux or mac.
# required for selenium to drive a firefox browser.

install_dir="/usr/local/bin"
json=$(curl -s https://api.github.com/repos/mozilla/geckodriver/releases/latest)
if [[ $(uname) == "Darwin" ]]; then
    url=$(echo "$json" | jq -r '.assets[].browser_download_url | select(contains("macos"))')
elif [[ $(uname) == "Linux" ]]; then
    url=$(echo "$json" | jq -r '.assets[].browser_download_url | select(contains("linux64"))')
else
    echo "can't determine OS"
    exit 1
fi
curl -s -L "$url" | tar -xz
chmod +x geckodriver
sudo mv geckodriver "$install_dir"
echo "installed geckodriver binary in $install_dir"


#!/bin/bash
# download and install latest chromedriver for linux or mac.
# required for selenium to drive a Chrome browser.

install_dir="/usr/local/bin"
version=$(curl -s -L -qO- https://chromedriver.storage.googleapis.com/LATEST_RELEASE)
if [[ $(uname) == "Darwin" ]]; then
    url=http://chromedriver.storage.googleapis.com/$version/chromedriver_mac32.zip
    curl -s -L "$url" | tar -xz 
    #url=https://chromedriver.storage.googleapis.com/$version/chromedriver_mac64.zip
#elif [[ $(uname) == "Linux" ]]; then
#    url=https://chromedriver.storage.googleapis.com/$version/chromedriver_linux64.zip
#else
#    echo "can't determine OS"
#    exit 1
#fi
curl -s -L "$url" | tar -xz
chmod +x chromedriver
sudo mv chromedriver "$install_dir"
echo "installed chromedriver binary in $install_dir"
sudo pip install PyPDF2
sudo pip install pycld2
sudo pip install nltk
sudo pip install selenium
sudo pip install delver
sudo pip install pdfminer
sudo pip install pyvirtualdisplay
sudo pip install textstat
sudo pip install fsspec>=0.3.3
sudo pip install textblob
sudo pip install twython
python3 -c "import nltk;nltk.download('punkt')"
python3 -c "nltk.download('stopwords')"
