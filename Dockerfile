# author Russell Jarvis rjjarvis@asu.edu

FROM jupyter/scipy-notebook
USER root
RUN apt-get update
RUN apt-get -y install apt-transport-https ca-certificates
RUN apt-get -y install apt-transport-https curl
RUN apt-get -y install wget
RUN pip install --upgrade pip

# Upgrade to version 2.0
RUN conda install -y matplotlib
# Make sure every Python file belongs to jovyan
RUN find /opt/conda ! -user $NB_USER -print0 | xargs -0 -I {} chown -h $NB_USER {}
# Remove dangling symlinks
RUN find -L /opt/conda -type l -delete
# Make sure every Python file is writable
RUN find /opt/conda ! -writable -print0 | xargs -0 -I {} chmod 744 {}

RUN chown -R $NB_USER $HOME
RUN rm -rf /var/lib/apt/lists/*
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

##
# Only firefox is used, delete chrome driver to save space.
##
# RUN wget https://chromedriver.storage.googleapis.com/2.31/chromedriver_linux64.zip
# RUN unzip chromedriver_linux64.zip
# RUN sudo chown -R jovyan ~/
# install google chrome
# RUN sudo apt-get -y update
# RUN sudo apt-get install -yqq unzip libxss1 libappindicator1 libindicator7 gconf-service libasound2 \
# libgconf-2-4 libnspr4 libnss3 libpango1.0-0 libxtst6 fonts-liberation xdg-utils
# RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
# RUN sudo dpkg -i google-chrome*.deb
# install chromedriver
# RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
# RUN sudo unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/


# install xvfb
RUN sudo apt-get install -yqq xvfb

# set dbus env to avoid hanging
ENV DISPLAY=:99
ENV DBUS_SESSION_BUS_ADDRESS=/dev/null


##
# Programatic Firefox driver that can bind with selenium/gecko.
## 

RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.18.0/geckodriver-v0.18.0-linux64.tar.gz
RUN sudo tar -xvzf geckodriver-v0.18.0-linux64.tar.gz
# RUN tar -xvzf geckodriver*
# RUN chmod +x geckodriver

RUN sudo chown -R $NB_USER $HOME

## Geckodriver
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.16.1/geckodriver-v0.16.1-linux64.tar.gz
RUN sudo sh -c 'tar -x geckodriver -zf geckodriver-v0.16.1-linux64.tar.gz -O > /usr/bin/geckodriver'
RUN sudo chmod +x /usr/bin/geckodriver
RUN rm geckodriver-v0.16.1-linux64.tar.gz
RUN sudo apt-get update
RUN sudo apt-get upgrade -y firefox
RUN sudo chown -R jovyan /home/jovyan

RUN sudo /opt/conda/bin/pip install pyvirtualdisplay
RUN sudo apt-get update
RUN sudo apt-get install --fix-missing
# A lot of academic text is still in PDF, so better get some tools to deal with that.
RUN sudo /opt/conda/bin/pip install git+https://github.com/pdfminer/pdfminer.six.git

# The only difference to the official version, is download throttling. Self throttling actually speeds up execution, 
# as it prevents getting booted off by SE servers, which can mean restarting scrape. Thankfuly GoogleScraper has good awareness
# of what it has already done.
RUN sudo /opt/conda/bin/pip install git+https://github.com/russelljjarvis/GoogleScraper.git
WORKDIR $HOME
RUN python -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger')"
RUN sudo chown -R $NB_USER $HOME

WORKDIR $HOME
# Probably the reason doing this here is ineffective, is just a execution path problem.
# If this doesn't work maybe do it post hoc in an interactive shell.
# RUN python -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger')"
ADD run_post_docker_build.sh .
ENTRYPOINT /bin/bash run_post_docker_build.sh && /bin/bash