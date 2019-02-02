# Science Accessibility Project



## Overview 
Non-scientific writing typically exceeds genuine scientific writing in one important aspect: in contrast to genuine science, non-science is often expressed with a less complex, and more engaging writing style. We believe non-science writing occupies a more accessible niche, that academic science writing should also occupy. Unfortunately, writing styles intended for different audiences, are predictably different. We show that we can use machine learning to predict the status of writing styles: blog, wikipedia, opinion, and traditional science, by first sampling a large variety of web documents, and then classifying among the different writing types. By predicting which of the several different styles a document occupies, we are able to characterize among different writing niches, and to point to remedies.

Multiple stake holders can benefit when science is communicated with lower complexity expression of ideas. With lower complexity science writing, knowledge would be more readily transferred into public awareness, additionally, digital organization of facts derived from journal articles would occur more readily, as successful machine comprehension of documented science would likely occur with less human intervention.

Objectively describing the character of the different writing styles will allow us to prescribe how, to shift academic science writing into a more accessible niche, where science can more aggressively compete with pseudo-science, and blogs, at a moment in history when public awareness is critically at stake.

## Machine Estimation of Writing Complexity:
The accessibility of written word can be approximated by a computer program that reads over the text, and guesses the mental difficulty, associated with comprehending a written document. The computer program maps reading difficult onto a quantity that represents the number of years of schooling needed to decode the language in the document. For convenience, we can refer to the difficulty associated with the text as the 'complexity' of the document. 


## Open Data Counterpart of this Code Repository lives at:
https://osf.io/yng5u/wiki/home/

## Analysis of Text.
Running the scraper is not necessary for analysing the text documents.

### Word frequencies as clouds::
### Per category
#### Not Science
![image](https://user-images.githubusercontent.com/7786645/52091608-322fbe80-2572-11e9-8553-3e346a8b824e.png)
#### Science
![image](https://user-images.githubusercontent.com/7786645/52091615-352aaf00-2572-11e9-905a-0b75fe0005d7.png)


<p>The observant reader will see, 'et al', occurs in published literature quite a lot, highlighting an obvious finding that science writing often refers to external evidence.

### How do some well known texts do?

* For some XKCD credidibility: [Pushing the limits of extremely readable science](http://splasho.com/upgoer5/library.php)

* [The Readability of Science is Declining over time](https://elifesciences.org/download/aHR0cHM6Ly9jZG4uZWxpZmVzY2llbmNlcy5vcmcvYXJ0aWNsZXMvMjc3MjUvZWxpZmUtMjc3MjUtdjIucGRm/elife-27725-v2.pdf?_hash=WA%2Fey48HnQ4FpVd6bc0xCTZPXjE5ralhFP2TaMBMp1c%3D)

* [The science of Writing](https://cseweb.ucsd.edu/~swanson/papers/science-of-writing.pdf)

* [Machine generated post modern obfuscation:](http://www.elsewhere.org/pomo/)


| complexity   |      texts      |
|----------|:-------------:|
| 6.0   | upgoer5   |
| 9.0 |    readability of science declining   |
| 14.0 | science of writing |
| 12.0 | post modern essay gen |
| 14.9 | mean wikipedia complexity|


[Similar projects](https://blog.machinebox.io/detect-fake-news-by-building-your-own-classifier-31e516418b1d).


## Sentiment Versus Complexity
   
    
   
   
   
   
   
      
   
![image](http://russelljjarvis.github.io/russelljjarvis/ScienceAccessibility/index.html)
An interactive hyperlinked to URL version zof this plot is available at 
Examples/interactive_complexity_urls.html


## Building All of the Project.
(including the scraper).

The scraping, and crawling code for this is dependency heavy. Docker is used to solve non trivial software dependency issues where possible.

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

## Why is the Scraping Code So Complex?

A lot of complexity in the code base comes from the need to masquerade as a non bot web surfer. An example of a TCP/IP dialogue might read like this:
Search Engine: 'who are you?' code: 'I am an honest human centric browser, and certainly not a robot surfing in the nude'. Search Engine: 'good, here are some pages'.	 Time elapses and the truth is revealed just like in 'the Emperors New Clothes'.	

Excepting for the scraping the wikipedia (which has bot friendly policies), it's a bad idea to surf raw ie to only use: `urllib`, or `requests`, as these resource grabbers are sure fire bot give aways.
`Selenium`, `Google Scrape` (uses Selenium), and `delver Crawler`, are the surfing clothes people use; they work together to prolong a period feigned humanhood. The downloading of pdf's as opposed to html usually is fine without a fake humancentric browser (that acts like it is storing cookies), but this does not seem to cause any problems.

## What about Code Cognitive Complexity?
The project takes measures to minimize that also. See the codeComplexity directory.
