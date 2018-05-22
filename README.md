# Scientific readability project

Executing these files is not yet straight forward, as the execution environment is dependency heavy. Docker is used to solve non trivial software dependency issues where possible.

If docker is installed on the base OS, git clone this repository, and assuming the file build.sh is chmod +x , run: `bash build.sh` to perform the dockerbuild. To run the jupyter notebook over docker:


## Enter the docker enivornment interactively in one of two ways, via a bash shell, or via an ipython notebook:
Launch via BASH in Linux
### 1
```
'cd this_path; sudo docker run -p 8888:8888 -v this_path:/home/jovyan slc jupyter notebook --ip=0.0.0.0 --NotebookApp.token=\"\" --NotebookApp.disable_check_xsrf=True' 
```

Maybe define a bash alias, if this command get's too big and old.

```
alias drvt='cd this_path; sudo docker run -p 8888:8888 -v this_path:/home/jovyan slc jupyter notebook --ip=0.0.0.0 --NotebookApp.token=\"\" --NotebookApp.disable_check_xsrf=True' 
```
                                                                 
To Run the project, one needs to execute the files:
`bash 
python scrape.py`,
and or the jupyter notebook: vstrl.ipynb. 


If you succeed at launching a jupyter notebook, you can enter a terminal there through the browser. Jupyter notebooks are therefore the most general solution.