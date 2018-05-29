# Scientific readability project

Executing these files is not yet straight forward, as the execution environment is dependency heavy. Docker is used to solve non trivial software dependency issues where possible.

If docker is installed on the base OS, git clone this repository, and assuming the file build.sh is chmod +x , run: `bash build.sh` to perform the dockerbuild. To run the jupyter notebook over docker:


* Enter the docker enivornment interactively in one of two ways, via a bash shell, or via an ipython notebook or
launch via BASH in Linux as follows:

```
'cd this_path; sudo docker run -p 8888:8888 -v this_path:/home/jovyan slc jupyter notebook --ip=0.0.0.0 --NotebookApp.token=\"\" --NotebookApp.disable_check_xsrf=True'
```

Maybe define a bash alias, if this command get's too big and old.

```
alias drvt='cd this_path; sudo docker run -p 8888:8888 -v this_path:/home/jovyan slc jupyter notebook --ip=0.0.0.0 --NotebookApp.token=\"\" --NotebookApp.disable_check_xsrf=True'
```

To Run the project, one needs to execute the files navigate to the examples directory and execute:
`python scrape.py`,
scrapes search engines for parameters defined in utils_and_params

and or the jupyter notebook: vstrl.ipynb which plots analysis based on scrapped data.

Note: a lot of complexity in the code base comes from the need to masquerade as a non bot web surfer.
It's a bad idea to surf naked ie to only use: `urllib`, or `requests`, as these resource grabbers are sure fire bot give aways.
`Selenium`, `Google Scrape` (uses Selenium), and `delver Crawler`, are the surfing clothes I used; they work together to prolong a period feigned humanhood.
The downloading of pdf's as opposed to html usually occurs in the nude, but this does not seem to cause any problems. 

Search Engine: 'who are you?' code: 'I am an honest human centric browser, and certainly note a nude surfing robot'. Search Engine: 'good, here are some pages'.
Time elapses and the deception is revealed just like in 'the Emperors New Clothes'.