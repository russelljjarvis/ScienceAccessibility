# neuron-mpi-neuroml
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

RUN wget https://chromedriver.storage.googleapis.com/2.31/chromedriver_linux64.zip
RUN unzip chromedriver_linux64.zip


USER $NB_USER
ENV WORK_HOME $HOME/work
WORKDIR $WORK_HOME
WORKDIR SReadability
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

# install google chrome
RUN sudo apt-get -y update
RUN sudo apt-get install -yqq unzip libxss1 libappindicator1 libindicator7 gconf-service libasound2 \
  libgconf-2-4 libnspr4 libnss3 libpango1.0-0 libxtst6 fonts-liberation xdg-utils
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN sudo dpkg -i google-chrome*.deb

# install chromedriver
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN sudo unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# install xvfb
RUN sudo apt-get install -yqq xvfb

# set dbus env to avoid hanging
ENV DISPLAY=:99
ENV DBUS_SESSION_BUS_ADDRESS=/dev/null



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
RUN touch start.sh
RUN echo "cd /home/mnt" >> start.sh
RUN echo "ipython -i ScrapeLinksandText_v4.py" >> start.sh
#RUN echo "ipcluster start -n 8 --profile=default & sleep 5 && ipython -i tAnalysis_v3.py" >> start.sh
ENTRYPOINT /bin/bash start.sh
