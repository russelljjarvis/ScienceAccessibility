**[Installation](Documentation/Documentation_Quick_Start.md)** |
**[Documentation](#documentation)** |
**[Contributing](contributing.md)** |
**[Testing](#testing)** |
**[License](license.md)** |
**[Manuscript](Documentation/manuscript.md)** |



[![Build Status](https://travis-ci.com/russelljjarvis/ScienceAccessibility.png)](https://travis-ci.com/russelljjarvis/ScienceAccessibility) 

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/russelljjarvis/simple_science_access.git/master)

# Overview

Understanding a big word is hard, so when big ideas are written down with lots of big words, the large pile of big words is also hard to understand. 

We used a computer to quickly visit and read many different websites to see how hard each piece of writing was to understand. People may avoid learning hard ideas, only because too many hard words encountered in the process.  We think we can help by explaining the problem with smaller words, and by creating tools to address the problem.

## Why Are We Doing This?
We want to promote clearer and simpler writing in science, by encorouging scientists in the same field to compete with each other over writing more clearly.

## How Are we Doing This?

### Machine Estimation of Writing Complexity:

The accessibility of written word can be approximated by a computer program that reads over the text and guesses the mental difficulty, associated with comprehending a written document. The computer program maps reading difficult onto a quantity that is informed by the cognitive load of the writing, and the number of years of schooling needed to decode the language in the document. For convenience, we can refer to the difficulty associated with the text as the 'complexity' of the document. 

### How do some well-known texts do?

First, we sample some extremes in writing style, and then we will tabulate results, so we have some nice reference points to help us to make sense of other results. On the lower and upper limits we have: XKCD: [Pushing the limits of extremely readable science](http://splasho.com/upgoer5/library.php) and for some comparison, we wanted to check some [Machine generated postmodern nonesense](http://www.elsewhere.org/pomo/)

Higher is worse:

| complexity   |      texts      |
|----------|:-------------:|
| 6.0   | [upgoer5](http://splasho.com/upgoer5/library.php)   |
| 9.0 |    [readability of science declining](https://elifesciences.org/download/aHR0cHM6Ly9jZG4uZWxpZmVzY2llbmNlcy5vcmcvYXJ0aWNsZXMvMjc3MjUvZWxpZmUtMjc3MjUtdjIucGRm/elife-27725-v2.pdf?_hash=WA%2Fey48HnQ4FpVd6bc0xCTZPXjE5ralhFP2TaMBMp1c%3D)   |
| 14.0 | [science of writing](https://cseweb.ucsd.edu/~swanson/papers/science-of-writing.pdf) |
| 14.9 | mean wikipedia |
| 16.5 | [mean post modern essay generator](http://www.elsewhere.org/pomo/) |

# Some particular cases:
| complexity   |      texts      |
|----------|:-------------:|
| 13.0 | this readme.md |
| 17.0 | [The number of olfactory stimuli that humans can discriminate is still unknown](https://elifesciences.org/articles/08127)|
| 18.68 | [Intermittent dynamics and hyper-aging in dense colloidal gels](https://www.researchgate.net/publication/244552241_Intermittent_dynamics_and_hyper-aging_in_dense_colloidal_gelsThis_paper_was_originally_presented_as_a_poster_at_the_Faraday_Discussion_123_meeting) |
| 37.0 | [Phytochromobilin C15-Z,syn - C15-E,anti isomerization: concerted or stepwise?](https://www.researchgate.net/profile/Bo_Durbeej/publication/225093436_Phytochromobilin_C15-Zsyn_C15-Eanti_isomerization_Concerted_or_stepwise/links/0912f4fcd237e6701a000000.pdf) |


### Proposed Remedies:
* 1
Previously I mentioned creating tools to remedy inaccessible academic research> One tool, that functions as a natural extension of this work, is to enable 'clear writing' tournaments between prominent academic researchers, for example:

| mean complexity   |      author      |
|----------|:-------------:|
| 28.85 | [professor R Gerkin](https://scholar.google.com/citations?user=GzG5kRAAAAAJ&hl=en&oi=sra)   |
| 29.8 | [ other_author] |
| 30.58 |     [other_author]  |


Example code for the [proposed tool](https://github.com/russelljjarvis/ScienceAccessibility/blob/dev/Examples/Incentivise_by_competing.ipynb) would allow you to select academic authors who then play out a competition demand, and to utilize their writing contributions in the context of a tournament where academic tournament members compete to write simpler text. A more recently maintained version of that [file](https://github.com/russelljjarvis/ScienceAccessibility/blob/dev/Examples/compete.py)

* 2
A different remedy proposal is to run the text through [simplify](http://nlpprogress.com/english/simplification.html?fbclid=IwAR0B8G7zEmxVYbFWJMOyVTaHWkv4o9tTTFvVpsOcWrUQ777SXpM6KuM-8QI), evaluate complexity after translating the document simplify. 
How different are the scores?

### The Following is a plot of the Distribution of Science Writing Versus non-science writing the [ART Science corpus](https://www.aber.ac.uk/en/media/departmental/computerscience/cb/art/gz/ART_Corpus.tar.gz):
![image](https://user-images.githubusercontent.com/7786645/53215155-96dbb780-360c-11e9-9280-d8592d31d2f9.png)


The science writing niche is characterized, by having a mean reading grade level of 18, neutral, to negatively polarized sentiment type and close to an almost complete absence of subjectivity. Science writing is more resistant to file compression, meaning that information entropy is high, due to concise, coded language. These statistical features, give quite a lot to go on, with regards to using language style to predict the scientific status of a randomly selected web document. The same notion of entropy being generally higher in science is corroborated with the perplexity measure, which measures how improbable the particular frequency distribution of words of observed in a document was.


## Developer Overview 
Non-scientific writing typically exceeds genuine scientific writing in two important aspects: in contrast to genuine science, non-science is often expressed with a less complex, and more engaging writing style. We believe non-science writing occupies a more accessible niche, that academic science writing should also occupy. 

Unfortunately, writing styles intended for different audiences, are predictably different We show that computers can learn to guess the type of a written document: blog, Wikipedia, opinion, and traditional science, by first sampling a large variety of web documents, and then classifying using sentiment, complexity, and other variables. By predicting which of the several different niches a document occupies, we are able to characterize the different writing types and to describe strategies to remedy writing complexity.

Multiple stakeholders benefit when science is communicated with lower complexity expression of ideas. With lower complexity science writing, knowledge would be more readily transferred into public awareness, additionally, the digital organization of facts derived from journal articles would occur more readily, as successful machine comprehension of documented science would likely occur with less human intervention. 

The impact of science on society is likely proportional to the accessibility of written work. Objectively describing the character of the different writing styles will allow us to prescribe how, to shift academic science writing into a more accessible niche, where science can more aggressively compete with pseudo-science, and blogs.

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

The internet in some ways is like a big group of computers that are all friends with each. A scraper is A computer that visits many of the other computers on the internet. The scraper does not have to be friends with the computers it visits, it just needs to know the address at which each computer in the big friendship group can be reached.

The scraping and crawling code for this is dependency heavy. Who wants to duplicate the building of this whole environment from scratch? No-one? I thought so. [Docker is used to providing a universal build, and prevent duplicated effort](https://hub.docker.com/r/russelljarvis/science_accessibility).

If Docker is installed on the base OS, git clone this repository, and assuming the file build.sh is chmod +x , run: `bash build.sh` to perform the dockerbuild. To run the jupyter notebook over docker, enter the docker environment interactively in one of two ways, via a bash shell, or via an ipython notebook or
and then launch python via BASH in Linux as follows:

Warning: This Docker environment is currently 11.5GB, however it contains some non trivial scraping tools.

```BASH
docker login your_user_name@dockerhub.com
docker pull russelljarvis/science_accessibility
mkdir $HOME/data_words
docker run -it -v $HOME/data_words russelljarvis/science_accessibility
```
```BASH
cd Examples
ipython -i enter_author_name.py "R Gerkin"
``` 

To Run the project, you need to navigate to the Examples directory and then execute:
`python use_scrape.py`, which scrapes search engines for parameters defined in that file.
Once that is done an analysis program `use_analysis` is then called to run an analysis on the scraped text. This program generates some simple figures. The figures are very basic, and they act to function only as proof of concept.

Given pre-existing data (pickled files consisting of raw text contents), the analysis file can also be run on its own by executing: `python use_analysis.py`. To analyse the scraped texts, the Jupyter notebook: `vstrl.ipynb` also contains idioms for plotting and analysis based on scrapped data, although it is not maintained. The package Bokeh facilitates pretty interactive plots with data point mouse over data metrics.

Another file `Examples/use_code_complexity.py` reports back about the complexity of the code base. This code complexity analysis is not thorough enough to include third-party modules that were heavily utilized in the analysis, however, the principle of code complexity, with an application limited scope is generally applied in our approach, as it's obviously not desirable to use obfuscated code as a tool used to advocate for a simple language.



### What about Code Cognitive Complexity?
That is an issue too. The project takes measures to minimize that also. Many modern text editors feature cyclomatic complexity plugins.
