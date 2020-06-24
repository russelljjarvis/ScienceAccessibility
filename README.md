
[![Build Status](https://travis-ci.com/russelljjarvis/ScienceAccessibility.png)](https://travis-ci.com/russelljjarvis/ScienceAccessibility) 

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/russelljjarvis/ScienceAccess/master)



**![Example Screen Shot](https://russelljjarvis.github.io/ScienceAccess/data/example_app.png)**

**First Step**
```
git clone https://github.com/russelljjarvis/ScienceAccess.git
cd ScienceAccess

```

**If you don't have python3:**
```
sudo bash install_python3.sh
```

**Installation Apple** 
```
sudo bash apple_setup.sh
```

**Installation Linux** 
```
sudo bash setup.sh
```
**Run**
```
streamlit run app.py
```

**[Manuscript](https://github.com/russelljjarvis/ScienceAccessibility/blob/remaster/Documentation/manuscript.md)** 

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

[Similar projects](https://blog.machinebox.io/detect-fake-news-by-building-your-own-classifier-31e516418b1d).

