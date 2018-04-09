# Scientific readability project
* NB: I renamed ScrapeLinks_and_Text.py sclat_revised.py
* NB: I renamed TextAnalysis_v3.py t_analysis_purepython.py

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


Instructions for running code on your end. In the terminal navigate to to the Sreadability directory. Type

```git pull origin master``` and enter GH credentials.

Then use wcp alias. (ie type `wcp` in the terminal). If that does not work you may need to remember to type ```source ~/.profile``` if you have not yet run `cat ~/.bashrc >> ~/.bash_profile `

and then
type ```wcp``` until the prompt says 'jovyan' then you are in the container (fast command line virtual machine).
Then inside container run ```ipython -i ScrapeLinksandText_v5.py``` and then ```ipython -i tAnalysis.py```
Or I can do it on your computer when you are free next.

To install octave (MATLAB by FOSS), use the command inside docker container:
```sudo bash install_octave.sh```

To run both Scrape_links_and_text_etc.py and tAnalysis.py

Run:

``` ipython -i run_all.py ```
which runs both scrape_links_and_text and text_analysis at the same time (note older existing outputs of scrape_links_and_text are used as inputs into text_analysis, such
that the latest analysis, is always one iteration older than the latest.

```bash run_all.sh ``` simultaneously executes run_all, at the same time as installing octave.
Once run_all.py is completed it tries to then execute the MATLAB graphing code on the results files
