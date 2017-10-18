# author Russell Jarvis rjjarvis@asu.edu

FROM jupyter/scipy-notebook

USER root
RUN chown -R $NB_USER $HOME

#Get a whole lot of GNU core development tools

RUN apt-get update
RUN apt-get -y install apt-transport-https ca-certificates
RUN apt-get -y install apt-transport-https curl
RUN apt-get -y install wget

RUN pip install --upgrade pip

# Upgrade to version 2.0
RUN conda install -y matplotlib
RUN conda install plotly seaborn
# Make sure every Python file belongs to jovyan
RUN find /opt/conda ! -user $NB_USER -print0 | xargs -0 -I {} chown -h $NB_USER {}
# Remove dangling symlinks
RUN find -L /opt/conda -type l -delete
# Make sure every Python file is writable
RUN find /opt/conda ! -writable -print0 | xargs -0 -I {} chmod 744 {}

RUN chown -R $NB_USER $HOME
RUN rm -rf /var/lib/apt/lists/*
RUN echo "${NB_USER} ALL=NOPASSWD: ALL" >> /etc/sudoers


RUN sudo /opt/conda/bin/pip install nltk
RUN python -c "import nltk; nltk.download('punkt');from nltk import word_tokenize,sent_tokenize"
RUN python -c "import nltk; nltk.download('averaged_perceptron_tagger')"
RUN sudo /opt/conda/bin/pip install textstat
RUN sudo /opt/conda/bin/pip install tabulate
RUN sudo /opt/conda/bin/pip install textblob
RUN sudo /opt/conda/bin/pip install ipyparallel
RUN sudo /opt/conda/bin/pip install selenium


###
## A file that is expected to be available after a volume is mounted
## cannot be executed by using the entrypoint command, since
## Entry point acts on files that already exist
## Instead write a BASH script
## That merely assumes this path will
## become available at start up
## and execute it from its expected path on the mounted volume
## After building this file
## docker build autoload -t scidash/autoload
## I launch docker with the alias al given below:
## alias al='cd ~/scratch;sudo docker run -e DISPLAY=$DISPLAY -it -v `pwd`:/home/mnt -v ${HOME}/git/.git \
##                                                                        -v /tmp/.X11-unix:/tmp/.X11-unix \
##                                                    scidash/autoload'
###

USER $NB_USER
ENV WORK_HOME $HOME/work
WORKDIR $WORK_HOME

RUN sudo apt-get update
RUN sudo apt-get install -y python3-software-properties
RUN sudo apt-get install -y software-properties-common


#RUN sudo apt-add-repository ppa:octave/stable
#RUN sudo apt-get update
#RUN sudo apt-get install -y libfftw3-dev libfltk1.3-dev texinfooctave
#RUN octave-cli


RUN sudo chown -R jovyan ~/
#RUN sudo apt-get -y install octave
RUN echo "cd /home/mnt" >> start.sh
RUN echo "ipython -i ScrapeLinksandText_v4.py" >> start.sh
#RUN echo "ipcluster start -n 8 --profile=default & sleep 5 && ipython -i tAnalysis_v3.py" >> start.sh

#ENTRYPOINT /bin/bash start.sh


ENV DEBIAN_FRONTEND noninteractive
ENV DEBCONF_NONINTERACTIVE_SEEN true

# Set timezone
USER root

RUN dpkg-reconfigure --frontend noninteractive tzdata

# Update the repositories
# Install utilities
# Install XVFB and TinyWM
# Install fonts
# Install Python
RUN apt-get -yqq update && \
    apt-get -yqq install curl unzip && \
    apt-get -yqq install xvfb tinywm && \
    rm -rf /var/lib/apt/lists/*


# Install Chrome WebDriver
RUN CHROMEDRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE` && \
    mkdir -p /opt/chromedriver-$CHROMEDRIVER_VERSION && \
    curl -sS -o /tmp/chromedriver_linux64.zip http://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip && \
    unzip -qq /tmp/chromedriver_linux64.zip -d /opt/chromedriver-$CHROMEDRIVER_VERSION && \
    rm /tmp/chromedriver_linux64.zip && \
    chmod +x /opt/chromedriver-$CHROMEDRIVER_VERSION/chromedriver && \
    ln -fs /opt/chromedriver-$CHROMEDRIVER_VERSION/chromedriver /usr/local/bin/chromedriver

# Install Google Chrome
RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list && \
    apt-get -yqq update && \
    apt-get -yqq install google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# Default configuration
ENV DISPLAY :20.0
ENV SCREEN_GEOMETRY "1440x900x24"
ENV CHROMEDRIVER_PORT 4444
ENV CHROMEDRIVER_WHITELISTED_IPS "127.0.0.1"
ENV CHROMEDRIVER_URL_BASE ''
ENV DISPLAY 0.0
USER jovyan
WORKDIR $HOME
RUN sudo apt-get update

RUN sudo apt-get -y install google-chrome-stable


#RUN google-chrome --no-sandbox &
#RUN ng e2e --serve true --port 4200 --watch true
#RUN curl -X POST -H "Content-Type: application/json; charset=utf-8" -d "{\"desiredCapabilities\":{\"platform\":\"ANY\",\"browserName\":\"chrome\",\"chromeOptions\":{\"args\":[],\"extensions\":[]},\"version\":\"\",\"chrome.switches\":[]}}" localhost:12495/session
#RUN python -c "from selenium import webdriver; browser = webdriver.Chrome(); browser.get('http://google.com/')"
RUN sudo wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
#RUN sudo echo "deb http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google.list
RUN sudo apt-get update -y
RUN sudo apt-get install -y -q software-properties-common wget
RUN sudo add-apt-repository -y ppa:mozillateam/firefox-next
RUN sudo apt-get update
RUN sudo apt-get install -y -q firefox google-chrome-beta
RUN sudo apt-get upgrade
#RUN sudo echo "deb http://ppa.launchpad.net/mozillateam/firefox-next/ubuntu trusty main" > /etc/apt/sources.list.d//mozillateam-firefox-next-trusty.list
RUN sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys CE49EC21
RUN sudo apt-get update
RUN sudo apt-get install -y firefox xvfb
#RUN pip install selenium
RUN mkdir -p /root/selenium_wd_tests
# ADD sel_wd_new_user.py /root/selenium_wd_tests
# ADD xvfb.init /etc/init.d/xvfb
RUN sudo chmod +x /etc/init.d/xvfb
RUN sudo update-rc.d xvfb defaults
RUN sudo service xvfb start; export DISPLAY=:10)
EXPOSE 4444 5999
ENTRYPOINT (sudo service xvfb start; export DISPLAY=:10)
#; python /root/selenium_wd_tests/sel_wd_new_user.py)
