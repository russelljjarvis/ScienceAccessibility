FROM russelljarvis/science_accessibility:slc
ADD . .
RUN sudo chown -R jovyan .
RUN python -c "import SComplexity"
RUN python -c "from SComplexity import t_analysis, utils, scrape"
RUN sudo /opt/conda/bin/pip install wordcloud
# RUN python
WORKDIR SComplexity
RUN sudo /opt/conda/bin/pip install git+https://github.com/elifesciences/api-validator-python

RUN python -c "from SComplexity import online_app_backend"

# RUN python enter_author_name.py "R Gerkin"
# ENTRYPOINT python enter_author_name.py

# ENTRYPOINT ["python", "enter_author_name.py"]
