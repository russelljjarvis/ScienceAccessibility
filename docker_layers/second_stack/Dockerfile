# FROM russelljarvis/science_accessibility:slc
FROM russelljarvis/science_accessibility_user:latest
#ADD . .
# WORKDIR ../SComplexity
RUN ls -ltr
#RUN du Examples
RUN sudo rm -r ART_Corpus.tar
RUN sudo rm -r geckodriver.log
WORKDIR $HOME
RUN du ./Examples

RUN sudo rm -r ./Examples/.scrapecache
RUN sudo rm -r ./Examples/protected
RUN sudo rm -r ./Examples/protected2
RUN sudo rm -r ./Examples/results_dir/other
RUN sudo rm -r ./Examples/results_dir
RUN sudo rm -r ./Examples/.ipynb_checkpoints
# RUN sudo rm -f ./Examples/*.p
RUN ls ./Examples/traingDats.p
RUN sudo rm -f ./Examples/*.db
RUN sudo rm -f ./Examples/*.csv
RUN sudo rm -f ./Examples/*.log
RUN sudo rm -f ./Examples/*.png
RUN du ./Examples

RUN sudo chown -R jovyan .
WORKDIR ./Examples

RUN python -c "import SComplexity"
RUN python -c "from SComplexity import t_analysis, utils, scrape"
# WORKDIR SComplexity/Examples
RUN ls -ltr
RUN ls online_app_backend.py
#RUN python -c "import online_app_backend"
# RUN python
RUN python enter_author_name.py "R Gerkin"
#ENTRYPOINT python enter_author_name.py 