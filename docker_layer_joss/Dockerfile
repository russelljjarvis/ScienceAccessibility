FROM russelljarvis/science_accessibility_user:latest
RUN ls -ltr
#RUN du Examples
#RUN sudo rm -r ART_Corpus.tar
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
RUN wget https://www.dropbox.com/s/3h12l5y2pn49c80/traingDats.p?dl=0
RUN wget https://www.dropbox.com/s/crarli3772rf3lj/more_authors_results.p?dl=0
RUN wget https://www.dropbox.com/s/x66zf52himmp5ox/benchmarks.p?dl=0
ADD . .
RUN pip install .
RUN sudo /opt/conda/bin/pip install git+https://github.com/plotly/dash
RUN python -c "import SComplexity"
RUN python -c "from SComplexity import t_analysis, utils, scrape"
RUN ls -ltr
RUN ls online_app_backend.py
ENTRYPOINT python enter_author_name.py
