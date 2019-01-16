# author Russell Jarvis rjjarvis@asu.edu

FROM jupyter/scipy-notebook
# FROM python:3.7


USER root
# https://github.com/joyzoursky/docker-python-chromedriver/blob/master/py3/py3.6-xvfb-selenium/Dockerfile
RUN apt-get update && apt-get install -y gnupg

# RUN apt-get install -y gnupg
# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# install chromedriver

RUN apt-get install -yqq unzip curl
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# install xvfb
RUN apt-get install -yqq xvfb

# set display port and dbus env to avoid hanging
ENV DISPLAY=:99
ENV DBUS_SESSION_BUS_ADDRESS=/dev/null

# install selenium
RUN pip install selenium==3.8.0

RUN apt-get update
RUN apt-get -y install apt-transport-https ca-certificates
RUN apt-get -y install apt-transport-https curl
RUN apt-get -y install wget curl
RUN pip install --upgrade pip

ADD test.py .
RUN python test.py

# Upgrade to version 2.0
RUN conda install -y matplotlib
# Make sure every Python file belongs to jovyan
RUN find /opt/conda ! -user $NB_USER -print0 | xargs -0 -I {} chown -h $NB_USER {}
# Remove dangling symlinks
RUN find -L /opt/conda -type l -delete
# Make sure every Python file is writable
RUN find /opt/conda ! -writable -print0 | xargs -0 -I {} chmod 744 {}

ENV NB_USER jovyan
RUN chown -R $NB_USER $HOME
#RUN rm -rf /var/lib/apt/lists/*
RUN echo "${NB_USER} ALL=NOPASSWD: ALL" >> /etc/sudoers


RUN /opt/conda/bin/pip install nltk
RUN python -c "import nltk; nltk.download('punkt');from nltk import word_tokenize,sent_tokenize"
RUN python -c "import nltk; nltk.download('averaged_perceptron_tagger')"
RUN /opt/conda/bin/pip install textstat
RUN /opt/conda/bin/pip install tabulate
RUN /opt/conda/bin/pip install textblob
RUN /opt/conda/bin/pip install selenium
# pycld2 seems to be the most accurate english text classifier of the python packages.
RUN /opt/conda/bin/pip install fake_useragent bokeh natsort pycld2 pylzma

USER $NB_USER

RUN sudo apt-get update
RUN sudo apt-get install -y python3-software-properties
RUN sudo apt-get install -y software-properties-common

##
# TODO consider installing phantom-js browser instead, it's probably the most suited to scraping.
# https://stackoverflow.com/questions/39451134/installing-phantomjs-with-node-in-docker
##


# set dbus env to avoid hanging
ENV DISPLAY=:99
ENV DBUS_SESSION_BUS_ADDRESS=/dev/null
RUN sudo /opt/conda/bin/pip install --upgrade selenium

##
# Programatic Firefox driver that can bind with selenium/gecko.
##
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.23.0/geckodriver-v0.23.0-linux64.tar.gz
RUN sudo tar -xvzf geckodriver-v0.23.0-linux64.tar.gz


RUN sudo chown -R jovyan $HOME


RUN sudo sh -c 'tar -x geckodriver -zf geckodriver-v0.23.0-linux64.tar.gz -O > /usr/bin/geckodriver'
RUN sudo chmod +x /usr/bin/geckodriver
RUN rm geckodriver-v0.23.0-linux64.tar.gz
RUN sudo apt-get update
RUN sudo apt-get upgrade -y firefox
RUN sudo chown -R jovyan /home/jovyan
RUN sudo cp geckodriver /usr/local/bin/

RUN sudo /opt/conda/bin/pip install -U selenium


RUN sudo /opt/conda/bin/pip install pyvirtualdisplay

RUN sudo apt-get update
RUN sudo apt-get install --fix-missing
# A lot of academic text is still in PDF, so better get some tools to deal with that.
RUN sudo /opt/conda/bin/pip install git+https://github.com/pdfminer/pdfminer.six.git

# https://github.com/GoogleScraper.git
RUN sudo /opt/conda/bin/pip install git+https://github.com/NikolaiT/GoogleScraper
WORKDIR $HOME
RUN python -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger')"
RUN sudo chown -R jovyan $HOME

RUN sudo /opt/conda/bin/pip install -U natsort
RUN sudo /opt/conda/bin/pip install -U radon

RUN sudo /opt/conda/bin/pip install -U pycld2
RUN sudo /opt/conda/bin/pip install -U beautifulsoup4
RUN sudo /opt/conda/bin/pip install -U git+https://github.com/nuncjo/Delver
RUN python -c "import bs4"
RUN python -c "import delver"
RUN timeout 2s python
RUN sudo apt-get update

RUN sudo apt-get update \
    && sudo apt-get install -y --no-install-recommends \
        ca-certificates \
        bzip2 \
        libfontconfig \
    && sudo apt-get clean

ENV MOZ_HEADLESS = 1
RUN python - c "from selenium import webdriver;\
from selenium.webdriver.firefox.options import Options; \
options = Options(); \
options.headless = True; \
driver = webdriver.Firefox(options=options) ;\
driver.get('http://google.com/') ;\
print('Headless Firefox Initialized') ;\
driver.quit();"

RUN python - c "from selenium import webdriver;\
from selenium.webdriver.firefox.options import Options; \
options = Options(); \
options.headless = True; \
driver = webdriver.Chrome(options=options) ;\
driver.get('http://google.com/') ;\
print('Headless Chrome Initialized') ;\
driver.quit();"


RUN sudo /opt/conda/bin/pip install PyPDF2 pdfminer3k
RUN sudo apt-get install -y libpulse-dev
RUN sudo apt-get install -y python-dev libxml2-dev libxslt1-dev antiword unrtf poppler-utils pstotext tesseract-ocr \
flac ffmpeg lame libmad0 libsox-fmt-mp3 sox libjpeg-dev swig
RUN sudo apt-get install -y xvfb
RUN sudo /opt/conda/bin/pip install xvfbwrapper
RUN sudo /opt/conda/bin/pip install textract

ADD . .
RUN sudo chown -R jovyan .
RUN python -c "import SComplexity"
RUN python -c "from SComplexity import t_analysis, utils, scrape"
WORKDIR $HOME

RUN sudo /opt/conda/bin/pip install habanero
RUN sudo /opt/conda/bin/pip install -e .


# set display port to avoid crash
ENV DISPLAY=:99


ENV PATH /usr/local/bin/chromedriver:$PATH


ENTRYPOINT /bin/bash
