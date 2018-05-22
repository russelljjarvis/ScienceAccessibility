# Scientific readability project

To Run the project, one needs to execute the files:
`bash 
python scrape.py`,
and the jupyter notebook: Visualisation_search_terms_reading_levelGS.ipynb. 

TODO rename Visualisation_search_terms_reading_levelGS.ipynb vstrl.ipynb

Executing these files is not yet straight forward, as the execution environment is dependency heavy. Docker is used to solve non trivial software dependency issues where possible.

## Launch via BASH in Linux
### 1
If docker is installed on the base OS, git clone this repository, and assuming the file build.sh is chmod +x , run: `bash build.sh` to perform the dockerbuild. To run the jupyter notebook over docker:
```
'cd this_path; sudo docker run -p 8888:8888 -v this_path:/home/jovyan wtor jupyter notebook --ip=0.0.0.0 --NotebookApp.token=\"\" --NotebookApp.disable_check_xsrf=True' 
```

Maybe define a bash alias, if this command get's too big and old.

```
alias drvt='cd this_path; sudo docker run -p 8888:8888 -v this_path:/home/jovyan wtor jupyter notebook --ip=0.0.0.0 --NotebookApp.token=\"\" --NotebookApp.disable_check_xsrf=True' 
```
                                                                  

## Launch Graphically in OSX
### 1
click on whale symbol
## 2.
click Kitematic in drop down.
### 3.

## inside Kitematic find this docker container through the repository:
https://hub.docker.com/r/russelljarvis/run_all_wcomplexity/
in search bar type: run_all_complexity,
### 4.
click on it and follow download and run links.
### 5
Select settings, and Volumes. Try to mount a volume
### 6
I think you will also be able to get output files graphically.
### 7
If you can't mount mount the volume in settings, edit the file $HOME/.bash_profile
subsitute `run_all_complexity` into `wcp`

The original versions of the files have been deleted from the most current branch, although they still are accessible on this website, by viewing 'parent commits'


Python chromium/geckodriver configuration is here:
https://github.com/russelljjarvis/SReadability/blob/dev/Dockerfile#L34-L111

