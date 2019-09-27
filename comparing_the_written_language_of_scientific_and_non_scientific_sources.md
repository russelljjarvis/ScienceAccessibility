

### [Journal of Open Source Software](https://joss.readthedocs.io/en/latest/submitting.html)

# Comparing the Written Language of Scientific and Non-scientific Sources

### Authors
Russell Jarvis, Patrick McGurrin


### Summary
To ensure that text is accessible to a general population, writers must keep in mind the length of written text, as well as sentence structure, vocabulary, and other related language features [11].  Popular magazines, newspapers, and other online outlets purposefully cater language for a wide audience. On the other hand, there is a tendency for academic writing to use more complex, jargon-heavy language [12]. This likely stems from the inherent complexity of topics, as well as the expectation to share ideas predominantly with other scientists in the form of academic journal articles.

In the age of growing science communication, this tendency for scientists to use more complex language can carry over when writing in more mainstream media, such as blogs, websites, and social media. This can make this public-facing material difficult to read and understand, undermining efforts to communicate scientific topics more broadly to the general public.

To address this, we created a tool to analyze complexity of a given scientist’s work relative to other writing sources.  The tool first quantifies and contextualizes the readability of online written material, including currently existing text repositories like the Upgoer5 and results from web searches with varying topics and complexity. These data are then used as a reference to compare user-selected written work. The user enters an author’'s name, which begins a web-scraping process to collect text written by that author from google scholar. The software then computes the readability of this information and compares it to the reference sources mentioned above.

We believe this tool uses a data-driven approach to provide insightful,  statistical insights to the user about their writing. We hope it will help scientists interested in science communication to better shape the readability of their published work. This will make written content more accessible to a broad audience, and with hope lead to an improved global communication and understanding of complex topics, such as those in science and technology.

### Methods
We built a web-scraping and written text analysis infrastructure by extending many existing Free and Open Source (FOS) tools, including  Google Scrape (reference), Beautiful Soup (reference), and Selenium (reference).


## Text Metrics to Assess Language Complexity
1.  Text-stat - measures text reading level (complexity)

2.  The Natural Language Processing Tool Kit (NLTK) - measures text subjectivity and sentiment

3.  Search Engine Factors - records page rank

4.  LZW (de-)compression-ratio - measures information entropy

5.  Cluster centers - measures clustering of data when organized using complexity, sentiment, word length and compression ratios

These metrics are combined (?) to formulate a single readability score for each scraped item. The results of each item are then combined and used to generate a plot. 

## Reference Texts used for Analysis
We include a number of available reference texts with a-priori assumptions about how complex the text should be.

1.  Upgoer5 - a library using only the 10,000 most commonly occurring English words[2].

2.  Readability Declining Over Time - 

3. Science of Writing - 

4.  Postmodern Essay Generator (PMEG) - generates output consisting of sentences that obey the rules of written English, but without restraints on the semantic conceptual references [5].

5.  ART Corpus - a library of scientific papers published in The Royal Society of Chemistry (RSC) [1].


| Text Source | Mean Complexity | Unique Words |
|----------|----------|:-------------:|
| Upgoer 5                                     | 6                               | 35,103 |
| Readability Declining Over Time                                    | 9.0                         | -  |
| Science of Writing                                    | 14.0                         | -  |
| Post-Modern Essay Generator | 16.5                          | -  |
| Art Corpus                                  | 18.68                        | 2,594 |

## Plot Information 
The results of this tool generate a histogram binned by readability score (y-axis), which is initially populated exclusively by the ART corpus. We use the ART corpus because it is a pre-established library of scientific papers. Upgoer5. Readability Declining Over Time, Science of Writing, and PMEG are analyzed, with their mean readability scores also being applied to the histogram plot.

Each time a new author is entered into the tool by the user, it is scraped from google scholar and the minimum (min), maximum (max), and mean readability of that author's work are extracted and calculated. 


## Reproducibility
 We used a Docker file and associated container together as a self-documenting and extremely portable software environment clone to ensure reproducibility given the hierarchy of software dependencies.

## Results
Data is available in our [Open Science Framework data repository](https://osf.io/dashboard).

### Setting Up the Environment (Developer)
A docker container can be downloaded from Docker hub or built locally.
```BASH
docker login your_user_name@dockerhub.com
docker pull russelljarvis/science_accessibility:slc
mkdir $HOME/data_words
docker run -it -v $HOME/data_words russelljarvis/science_accessibility:slc
```
### Running a Simple Example (User)

Assuming you have installed Docker on your Operating System, and have a dockerhub account, run the following commands in a BASH terminal.

```BASH
docker pull russelljarvis/science_accessibility_user:latest
```
 Here is a python example to search for results from academic author Richard Gerkin. When inside the docker container, issue the command:

```BASH
mkdir $HOME/data_words
docker run -v $HOME/data_words russelljarvis/science_accessibility_user "R Gerkin"
```
This generates a graph displaying the mean writing complexity of author Bradley Lusk against a distribution of content from ART corpus.

To date, we have created a command line interface (CLI) to achieve this goal. Moving forward, we aim to expand this to a web application that will be more user friendly and allow additional utility.

![Specific Author Relative to Distribution](for_markdown_repository.png)


## Conclusions


## Future Directions

We'd like to add in wikipedia - a free, popular, crowdsourced encyclopedia that is generated from self-nominating volunteers. This language is specifically shaped by editors to be accessible for a general audience and would be a useful iaddition to the results. 

In addition, we're interested in general readability of the web. An additional future step is to apply search engine queries
of different, unrelated, and broad-ranging lists of search terms that apply scientific, cultural, and other more random queries to assess readability. The first ten search results were used for analysis.





## References
[1] Soldatova, Larisa, and Maria Liakata. "An ontology methodology and cisp-the proposed core information about scientific papers." JISC Project Report (2007).

[2] Kuhn, Tobias. "The controlled natural language of randall munroe’s thing explainer." International Workshop on Controlled Natural Language. Springer, Cham, 2016.

[3] Japos, Genaro V. "Effectiveness of coaching interventions using grammarly software and plagiarism detection software in reducing grammatical errors and plagiarism of undergraduate researches." JPAIR Institutional Research 1.1 (2013): 97-109.

[4] Kincaid, J. Peter, et al. "Derivation of new readability formulas (automated readability index, fog count and flesch reading ease formula) for navy enlisted personnel." (1975).  

[5] Bulhak, Andrew C. "On the simulation of postmodernism and mental debility using recursive transition networks." Monash University Department of Computer Science (1996).  

[6] V. Clayton, “The Needless Complexity of Academic Writing,” The Atlantic, 26-Oct-2015.

[7] Cannon, Robert C., et al. "LEMS: a language for expressing complex biological models in concise and hierarchical form and its use in underpinning NeuroML 2." Frontiers in neuroinformatics 8 (2014): 79.

[8] Gerkin, Richard C., and Cyrus Omar. "Collaboratively testing the validity of neuroscientific models." Frontiers in Neuroinformatics 1 (2014).

[9] Oppenheimer, Daniel M. "Consequences of erudite vernacular utilized irrespective of necessity: Problems with using long words needlessly." Applied Cognitive Psychology: The Official Journal of the Society for Applied Research in Memory and Cognition 20.2 (2006): 139-156.

[10]  High, Rob. "The era of cognitive systems: An inside look at IBM Watson and how it works." IBM Corporation, Redbooks (2012).

[11] Kutner, Mark, Elizabeth Greenberg, and Justin Baer. "A First Look at the Literacy of America's Adults in the 21st Century. NCES 2006-470." _National Center for Education Statistics_(2006).

[12] Plavén-Sigray, Pontus, Granville James Matheson, Björn Christian Schiffler, and William Hedley Thompson. "The readability of scientific texts is decreasing over time." Elife 6 (2017): e27725.
