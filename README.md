# Scientific readability project

To Run the project
You need to run python sclat.py, and python t_analysis_purepython.py
jupyter notebook Visualization_of_terms_reading_level.ipynb in a non trivial environment brought to you by Docker (read below)


* To future developers a GH repository of this code lives at
https://github.com/russelljjarvis/SReadability.git/
Its currently private but it can be forked and cloned etc.

Running t_analysis_purepython.py is not sufficient to perform an analysis unless the bottom most
code block is uncommented.

preferably the Jupyter notebook Visualization of Terms.ipynb is run instead.
Using more pythonic data types (dictionaries and lists) speeds up a parallel
analysis, as these data types are able to utilize memory more efficiently.

The search engine Duckduckgo is added in as well as search terms 'play dough', and
'neutron' as reference points. Ideally

# Launch via BASH alias's in Linux
## 1
This how I execute the project but I can't be bothered explaining how.

# Launch Graphically in OSX
## 1
click on whale symbol
## 2.
click Kitematic in drop down.
## 3.

# inside Kitematic find this docker container through the repository:
https://hub.docker.com/r/russelljarvis/run_all_wcomplexity/
in search bar type: run_all_complexity,
## 4.
click on it and follow download and run links.
## 5
Select settings, and Volumes. Try to mount a volume
## 6
I think you will also be able to get output files graphically.
## 7
If you can't mount mount the volume in settings, edit the file $HOME/.bash_profile
subsitute `run_all_complexity` into `wcp`

The original versions of the files have been deleted from the most current branch, although they still are accessible on this website, by viewing 'parent commits'


Python chromium/geckodriver configuration is here:
https://github.com/russelljjarvis/SReadability/blob/dev/Dockerfile#L34-L111


Instructions for running code on your end. In the terminal navigate to to the WCP directory. Type

```git pull origin master``` and enter GH credentials.

Then use wcp alias. (ie type `wcp` in the terminal). If that does not work you may need to remember to type ```source ~/.profile``` if you have not yet run `cat ~/.bashrc >> ~/.bash_profile `

and then
type ```wcp``` until the prompt says 'jovyan' then you are in the container (fast command line virtual machine).
Then inside container run ```ipython -i sclat.py``` and then ```ipython -i t_analysis_purepython.py```
Or I can do it on your computer when you are free next.

alias octave='cd /Users/Dropbox\ \(ASU\)/SReadability_revised; docker run -it -v /Users/rjjarvis/Dropbox\ \(ASU\)/SReadability_revised:/home/jovyan russelljarvis/wcomp_env:latest /bin/bash'

alias joct='cd /Users/Dropbox\ \(ASU\)/SReadability_revised; docker run -p 8888:8888 -e USERID=$UID -v /Users/rjjarvis/Dropbox\ \(ASU\)/SReadability_revised:/home/jovyan/wcproject russelljarvis/wcomp_env:latest jupyter notebook \
--ip=0.0.0.0 --NotebookApp.disable_check_xsrf=True'
