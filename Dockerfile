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

RUN sudo chown -R jovyan $HOME

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
RUN sudo chown -R jovyan $HOME

WORKDIR $HOME
# Probably the reason doing this here is ineffective, is just a execution path problem.
# If this doesn't work maybe do it post hoc in an interactive shell.
# RUN python -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger')"

RUN sudo /opt/conda/bin/pip install -U natsort
RUN sudo /opt/conda/bin/pip install -U pycld2
RUN sudo /opt/conda/bin/pip install -U beautifulsoup4
RUN sudo /opt/conda/bin/pip install -U git+https://github.com/nuncjo/Delver
RUN python -c "import bs4"
RUN python -c "import delver"
RUN timeout 2s python

ADD . .
RUN sudo chown -R jovyan .
RUN pip install -e .
RUN python -c "import SComplexity"
RUN python -c "from SComplexity import t_analysis, utils"
WORKDIR $HOME

RUN touch user_input.sh
RUN echo "#!/bin/bash" >> user_input.sh
RUN echo "read -n1 -p 'Run WC (r) or Develop the code, interactive Docker shell (s) ? [r,s]' doit
RUN echo "case $doit in" >> user_input.sh
RUN echo "  r|R) echo 'execute WC'; sudo /opt/conda/bin/pip install -e .; cd Examples; ipython -i use_scrape.py ;;" >> user_input.sh
RUN echo "  s|S) echo 'interactive shell' ;;" >> user_input.sh
RUN echo "  *) echo dont know ;;" >> user_input.sh
RUN echo "esac" >> user_input.sh
RUN cat user_input.sh
ENTRYPOINT /bin/bash user_input.sh; /bin/bash
