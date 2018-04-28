from russelljarvis/wordcomplexity
WORKDIR $HOME/SReadability
ADD . $HOME/SReadability
RUN sudo chown -R jovyan $HOME
WORKDIR $HOME
RUN sudo /opt/conda/bin/pip install stem requests requests[socks]
RUN sudo chown -R jovyan $HOME
RUN sudo apt-get -y install less
RUN sudo apt-get update
RUN sudo apt-get install -y curl tor
RUN sudo apt-get update
RUN sudo /opt/conda/bin/pip install atlas sklearn
RUN sudo conda install pycurl gcc
RUN sudo /opt/conda/bin/pip install git+https://github.com/NikolaiT/GoogleScraper.git
RUN git clone https://github.com/NikolaiT/GoogleScraper.git
RUN cp scrape.sh GoogleScraper
ENTRYPOINT /bin/bash scrape.sh


