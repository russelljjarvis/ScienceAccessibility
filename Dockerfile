# neuron-mpi-neuroml
# author Russell Jarvis rjjarvis@asu.edu

FROM jupyter/scipy-notebook

USER root
RUN chown -R $NB_USER $HOME

#Get a whole lot of GNU core development tools

RUN apt-get update
RUN apt-get install apt-transport-https ca-certificates
RUN apt-get -y install apt-transport-https curl
RUN apt-get install -y wget

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

USER $NB_USER
ENV WORK_HOME $HOME/work
WORKDIR $WORK_HOME