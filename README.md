[![Build Status](https://travis-ci.com/russelljjarvis/ScienceAccessibility.png)](https://travis-ci.com/russelljjarvis/ScienceAccessibility) <-works when public.
# Science Accessibility Project

## [Upgoer 5](http://splasho.com/upgoer5/library.php) Overview
Understanding big words is hard, so when big ideas are written down with lots of big words, the large pile of big words is also hard to understand. 

We used a computer programs on lots of different writing, meant for different people, to see how hard each piece of writing was to understand. We want to stop people avoiding learning hard ideas, only because there were too many hard words. We want most people understanding more hard ideas, so those people are not hurt because they did not understand important things. We think we can help by explaining the problem with small words, and by creating tools to address the problem.


## Machine Estimation of Writing Complexity:
The accessibility of written word can be approximated by a computer program that reads over the text, and guesses the mental difficulty, associated with comprehending a written document. The computer program maps reading difficult onto a quantity that represents the number of years of schooling needed to decode the language in the document. For convenience, we can refer to the difficulty associated with the text as the 'complexity' of the document. 

# The Distribution of Complex Writing the [ART Science corpus](https://www.aber.ac.uk/en/media/departmental/computerscience/cb/art/gz/ART_Corpus.tar.gz):
![complexity_distribution_art_corpus](https://user-images.githubusercontent.com/7786645/53114731-b20dd080-3501-11e9-8609-972d1172c8a2.png)

### How do some well known texts do?

First we sample some extremes in writing style, and then we will tabulate results, so we have some nice reference points to help us to make sense of other results. On the lower and upper limits we have: XKCD: [Pushing the limits of extremely readable science](http://splasho.com/upgoer5/library.php) and [Machine generated post modern nonesense:](http://www.elsewhere.org/pomo/)

Higher is worse:

| complexity   |      texts      |
|----------|:-------------:|
| 6.0   | [upgoer5](http://splasho.com/upgoer5/library.php)   |
| 9.0 |    [readability of science declining](https://elifesciences.org/download/aHR0cHM6Ly9jZG4uZWxpZmVzY2llbmNlcy5vcmcvYXJ0aWNsZXMvMjc3MjUvZWxpZmUtMjc3MjUtdjIucGRm/elife-27725-v2.pdf?_hash=WA%2Fey48HnQ4FpVd6bc0xCTZPXjE5ralhFP2TaMBMp1c%3D)   |
| 14.0 | [science of writing](https://cseweb.ucsd.edu/~swanson/papers/science-of-writing.pdf) |
| 14.3 | [mean post modern essay generator](http://www.elsewhere.org/pomo/) |
| 14.9 | mean wikipedia |

# Some particular cases:
| complexity   |      texts      |
|----------|:-------------:|
| 12.0 | this readme.md |
| 18.68 | [Intermittent dynamics and hyper-aging in dense colloidal gels](https://www.researchgate.net/publication/244552241_Intermittent_dynamics_and_hyper-aging_in_dense_colloidal_gelsThis_paper_was_originally_presented_as_a_poster_at_the_Faraday_Discussion_123_meeting) |
| 17.0 | [The number of olfactory stimuli that humans can discriminate is still unknown](https://elifesciences.org/articles/08127)|
| 37.0 | [Phytochromobilin C15-Z,syn - C15-E,anti isomerization: concerted or stepwise?](https://www.researchgate.net/profile/Bo_Durbeej/publication/225093436_Phytochromobilin_C15-Zsyn_C15-Eanti_isomerization_Concerted_or_stepwise/links/0912f4fcd237e6701a000000.pdf) |



## Proposed Remedies:
# 1
Previously I mentioned creating tools to remedy the situation, of academic research being written in incomprehensible, and audiance limited style. One tool, that functions as a natural extension of this work, is to enable 'clear writing' tournaments between prominent academic researchers, for example:

| mean complexity   |      author      |
|----------|:-------------:|
| 28.85 | [professor R Gerkin](https://scholar.google.com/citations?user=GzG5kRAAAAAJ&hl=en&oi=sra)   |
| 29.8 | [professor D Grayden](https://scholar.google.com/citations?user=X7aP2LIAAAAJ&hl=en) |
| 30.58 |     [professor S Crook](https://scholar.google.com/citations?user=xnsDhO4AAAAJ&hl=en&oe=ASCII&oi=sra)  |




Example code for the [proposed tool](https://github.com/russelljjarvis/ScienceAccessibility/blob/dev/Examples/Incentivise_by_competing.ipynb) would allow you to select academic authors who then play out a competition demand, and to utilize their writing contributions in the context of a tournament where, academic tournament members compete to write simpler text.

A more recently maintained version of that [file](https://github.com/russelljjarvis/ScienceAccessibility/blob/dev/Examples/compete.py)

# 2
Run text through [simplify](http://nlpprogress.com/english/simplification.html?fbclid=IwAR0B8G7zEmxVYbFWJMOyVTaHWkv4o9tTTFvVpsOcWrUQ777SXpM6KuM-8QI), evaluate complexity after translating the document simplify. 
How different are the scores?


## Developer Overview 
Non-scientific writing typically exceeds genuine scientific writing in two important aspects: in contrast to genuine science, non-science is often expressed with a less complex, and more engaging writing style. We believe non-science writing occupies a more accessible niche, that academic science writing should also occupy. 

Unfortunately, writing styles intended for different audiences, are predictably different We show that computers can learn to guess the type of a written document: blog, wikipedia, opinion, and traditional science, by first sampling a large variety of web documents, and then classifying using sentiment, complexity, and other variables. By predicting which of the several different niches a document occupies, we are able to characterize the different writing types, and to describe strategies to remedy writing complexity.

Multiple stake holders benefit when science is communicated with lower complexity expression of ideas. With lower complexity science writing, knowledge would be more readily transferred into public awareness, additionally, digital organization of facts derived from journal articles would occur more readily, as successful machine comprehension of documented science would likely occur with less human intervention. 

The impact of science on society, is likely propotional to the accessibility of the written work. Objectively describing the character of the different writing styles will allow us to prescribe how, to shift academic science writing into a more accessible niche, where science can more aggressively compete with pseudo-science, and blogs, at a moment in history when public awareness is critically at stake.

## Analysis of Text.
Running the scraper is not necessary for analysing the text documents. 

## Sentiment Versus Complexity

[An interactive plot of the same thing, where clicking on a data point takes you to the webpage that generated the data point](https://russelljjarvis.github.io/ScienceAccessibility/)


### Word frequencies as clouds:
### Per category
#### Not Science
![image](https://user-images.githubusercontent.com/7786645/52091608-322fbe80-2572-11e9-8553-3e346a8b824e.png)
#### Science
![image](https://user-images.githubusercontent.com/7786645/52091615-352aaf00-2572-11e9-905a-0b75fe0005d7.png)


The observant reader will see, 'et al', occurs in published literature quite a lot, highlighting an obvious finding that science writing often refers to external evidence.


[Similar projects](https://blog.machinebox.io/detect-fake-news-by-building-your-own-classifier-31e516418b1d).


## Building All of the Project.
(including the scraper).

The internet in someways is like a big group of computers that are all friends with each. A scraper is A computer that visits many of the other computers on the internet. The scraper does not have to be friends with the computers it visits, it just needs to know the address at which each computer in the big friendship group can be reached.

The scraping, and crawling code for this is dependency heavy. Who wants to duplicate building of this whole environment from scratch? No-one? I thought so. [Docker is used to provide a universal build, and prevent duplicated effort](https://cloud.docker.com/repository/registry-1.docker.io/russelljarvis/science_accessibility).

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

## What about Code Cognitive Complexity?
The project takes measures to minimize that also. See the codeComplexity directory. 

