# Scientific Readability Project
## Motivation for the Scientific Readability Project
Non-scientific writing typically exceeds genuine scientific writing in one important criteria: in contrast to genuine science non-science ideas are often expressed with a more accessible writing style. Presently, the accessibility of written work, can be approximated by computer programs, that express, the mental challenge, associated with comprehending a written document, in terms of years of schooling needed to decode the language, subjectivity, sentiment, and the overall language complexity of the document. 

Multiple stake holders can benefit when science is communicated with lower complexity expression of ideas. With lower complexity science writing, knowledge would be more readily transferred into public awareness, additionally, organization of facts derived from journal articles would occur more readily, as successful machine comprehension of documented science would likely occur with less human intervention.

We believe non-science writing occupies a style niche, that academic science writing should also occupy. We show that we can blindly predict the status of writing: popular culture writing, opinionative writing, and traditional science, by using machine learning to classify the different writing types. By predicting which of the several different writing types any writing piece occupies, we are able to characterize among different writing niches.

Objectively describing the different character of the different writing styles will allow us to prescribe how, to shift academic science writing into a more accessible niche, where science can more aggressively compete with pseudo-science, and blogs, facilitating greater knowledge transference, at a moment in history when public awareness is critically at stake.



## Data Counterpart of this Code Repository lives at:
https://osf.io/yng5u/wiki/home/


## Building the project.

Executing these files is not yet straight forward, as the execution environment is dependency heavy. Docker is used to solve non trivial software dependency issues where possible.

If docker is installed on the base OS, git clone this repository, and assuming the file build.sh is chmod +x , run: `bash build.sh` to perform the dockerbuild. To run the jupyter notebook over docker, enter the docker enivornment interactively in one of two ways, via a bash shell, or via an ipython notebook or
and then launch python via BASH in Linux as follows:

```
'cd this_path; sudo docker run -it -v this_path:/home/jovyan slc'
```

Maybe define a bash alias, if this command get's too big and old.

```
alias drvt='cd this_path; sudo docker run -v this_path:/home/jovyan slc'
```

To Run the project, you need navigaate to the Examples directory and then execute:
`python use_scrape.py`, which scrapes search engines for parameters defined in that file.
Once that is done an analysis program `use_analysis` is then called to run an analysis on the scraped text. This program generates some simple figures. The figures are very basic, and they act to function only as proof of concept.

Given pre-existing data (pickled files consisiting of raw text contents), the analysis file can also be run on it's own by executing: `python use_analysis.py`. To analyse the scraped texts, the jupyter notebook: `vstrl.ipynb` also contains idioms for plotting and analysis based on scrapped data, although it is not maintained. The package bokeh, facilitates pretty interactive plots with data point mouse over data metrics.

Another file `Examples/use_code_complexity.py` reports back about the complexity of the code base. This code complexity analysis is not thorough enough to include third party modules that were heavily utilized in the analysis, however, the principle of code complexity, with an application limited scope is generally applied in our approach, as it's obviously not desirable to use obfuscated code as a tool used to advocate for simple language.

A lot of complexity in the code base comes from the need to masquerade as a non bot web surfer. An example of a TCP/IP dialogue might read like this:
Search Engine: 'who are you?' code: 'I am an honest human centric browser, and certainly note a robot surfing in the nude'. Search Engine: 'good, here are some pages'.	 Time elapses and the truth is revealed just like in 'the Emperors New Clothes'.	Time elapses and reality is exposed just like in 'the Emperors New Clothes'.

Excepting for the scraping the wikipedia (which has bot friendly policies), it's a bad idea to surf raw ie to only use: `urllib`, or `requests`, as these resource grabbers are sure fire bot give aways.
`Selenium`, `Google Scrape` (uses Selenium), and `delver Crawler`, are the surfing clothes people use; they work together to prolong a period feigned humanhood. The downloading of pdf's as opposed to html usually is fine without a fake humancentric browser (that acts like it is storing cookies), but this does not seem to cause any problems.
