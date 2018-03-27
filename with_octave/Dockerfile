from russelljarvis/wordcomplexity
ADD wcproject $HOME/wcproject
WORKDIR $HOME/wcproject
RUN sudo bash install_octave.sh
RUN sudo chown -R jovyan $HOME
RUN mv *.py ../
RUN mv *.m ../
WORKDIR $HOME
#RUN ipython -i sclat.py ;
#RUN ipython -i t_analysis.py ;
#RUN octave crawlAnalysis.m & octave QuantAnalysis_v2.m
RUN sudo /opt/conda/bin/pip install oct2py

ENTRYPOINT ipython sclat.py; ipython t_analysis.py; octave crawlAnalysis.m & octave QuantAnalysis_v2.m
