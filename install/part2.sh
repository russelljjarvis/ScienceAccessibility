#!/bin/bash
sudo /opt/conda/bin/pip install --upgrade pip
sudo /opt/conda/bin/python -m pip install -U pip

pip install -U -r ../requirements.txt
python -c "import nltk; nltk.download('punkt')"
python -c "import nltk; nltk.download('stopwords')" 