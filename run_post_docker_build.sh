#/bin/bash
pip install natsort 
pip install pycld2
pip install beautifulsoup4
pip install scrapy
curl -O https://bootstrap.pypa.io/get-pip.py && \
    python3 get-pip.py && \
    rm get-pip.py
pip3 install jupyter
sudo /opt/conda/bin/ipython3 kernelspec install-self
