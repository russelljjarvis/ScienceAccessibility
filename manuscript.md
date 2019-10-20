title: 'Comparing the Readability of Scientific and Non-scientific Sources'
		
tags:
  readability
  science communication
  science writing

authors
  - name: Russell Jarvis
    affiliation: PhD Candidate Neuroscience, Arizona State University
  - name: Patrick McGurrin
    affiliation: National Institute of Neurological Disorders and Stroke, National Institutes of Health
  - name: Shivam Bansal
    affiliation: Senior Data Scientist, H2O.ai
  - name: Bradley G Lusk
    affiliation: Science The Earth; Mesa, AZ 85201, USA
    
date: 20 October 2019

bibliography: paper.bib

## Summary
To ensure writing is accessible to a general population, writers must consider the length of written text, as well as sentence structure, vocabulary, and other language features [@Kutner:2006]. While popular magazines, newspapers, and other outlets purposefully cater language for a wide audience, there is a tendency for academic writing to use complex, jargon-heavy language [@Plavén-Sigray:2017]. 

In the age of growing science communication, this tendency for scientists to use more complex language can carry over when writing in more mainstream media, such as blogs and social media. This can make public-facing material difficult to comprehend, undermining efforts to communicate scientific topics to the general public.

To address this, we created a tool to analyze complexity of a given scientist’s work relative to other writing sources. The tool first quantifies existing text repositories with varying complexity, and subsequently uses this output as a reference to contextualize the readability of user-selected written work. 

While other readability tools currently exist to report the complexity of a single document, this tool uses a more data-driven approach to provide authors with insights into the readability of their published work with regard to other text repositories. This will enable them to monitor the complexity of their writing with regard to other available text types, and lead to the creation of more accessible online material. We hope it will help scientists interested in science communication to make their published work more accessible to a broad audience, and lead to an improved global communication and understanding of complex topics.

## Methods

### Text Analysis Metrics
We built a web-scraping and text analysis infrastructure by extending many existing Free and Open Source (FOS) tools, including Google Scrape, Beautiful Soup, and Selenium.

The Flesch-Kincaid readability score [@Kincaid:1975] is the most commonly used metric to assess readability, and was used here to quantify the complexity of each text item.

Before analysis of the user input, we query and analyze a number of available text repositories with varying complexity. The Flesch-Kincaid readability score was caluclated for each time in the repository.

| Text Source | Mean Complexity | Description |
|----------|----------|:-------------:|
| Upgoer 5                            | 6   | a library using only the 10,000 most commonly occurring English words |
| Wikipedia                               | 14.9 | a free, popular, crowdsourced encyclopedia   |
| Post-Modern Essay Generator (PMEG)  | 16.5 | generates output consisting of sentences that obey the rules of written English, but without restraints on the semantic conceptual references   |
| Art Corpus                       | 18.68  | a library of scientific papers published in The Royal Society of Chemistry |

The author's name entered by the user is queried through Google Scholar, returning the results from articles containing the author's name. The Flesch-Kincaid readability score is then caluclated for each of these articles.

### Plot Information 
The entered author name generates a histogram binned by readability score, which is initially populated exclusively by the ART corpus [@Soldatova:2007] data. We use this data because it is a pre-established library of scientific papers. The resulting graph displays the mean writing complexity of the entered author against a distribution of ART corpus content.

The mean readability scores of Upgoer5 [@Kuhn:2016], Wikipedia, and PMEG [@Bulhak:1996] libraries are also applied to the histogram plot to contextualize the complexity of the ART corpus data with other text repositories of known complexity. 

We also include mean readability scores from two scholarly reference papers, Science Declining Over Time [@Kutner:2006] and Science of Writing [@Gopen:1990], which discuss writing to a broad audience in an academic context. We use these to demonstrate the feasability of discussing complex content using more accessible language.

Lastly, the mean reading level of the entered author's work, as well as the maximum and minimum scores, are displayed in the context of the above reference data. 

### Reproducibility
A Docker file and associated container together serve as a self-documenting and portable software environment clone to ensure reproducibility given the hierarchy of software dependencies.

## Results
Data are available here: [Open Science Framework data repository](https://osf.io/dashboard).

### Setting Up the Environment (Developer)
A docker container can be downloaded from Docker hub or built locally.
```BASH
docker login your_user_name@dockerhub.com
docker pull russelljarvis/science_accessibility:slc
mkdir $HOME/data_words
docker run -it -v $HOME/data_words russelljarvis/science_accessibility:slc
```
### Running a Simple Example (User)
After Docker installation on your Operating System, run the following commands in a BASH terminal.
```BASH
docker pull russelljarvis/science_accessibility_user:latest
```
Here is a python example to search for results from academic author Richard Gerkin. When inside the docker container, issue the command:
```BASH
mkdir $HOME/data_words
docker run -v $HOME/data_words russelljarvis/science_accessibility_user "R Gerkin"
```
![Specific Author Relative to Distribution](for_joss_standard_dev.png)

This tool also allows the entry of two author names to view whose text has the lowest average reading grade level. Public competitions and leader boards often incentivize good practices, and may also help to improve readability scores over time.

![Specific Author Relative to Distribution](compete.png)


## Future Work
We have created a command line interface (CLI) for using this tool. However, we aim to expand this to a web application that is more user friendly to those less familiar with coding. 

While the readability of ART Corpus is comparable to that of other scientific journals [2], a future goal is also to incoporate a larger repository of journal articles to compute the distribution of readability. In addition, we're interested in general readability of the web, and aim to add search engine queries of different and broad-ranging lists of search terms to assess readability of an eclectic range of text. This would further contextualize the readability of published scientific work with regard to topics engaged by the public on a more daily basis.

A final goal is to incorporate other readability metrics, including information entropy, word length, and compression rations, subjectivity, and reading ease scores. While the Flesch-Kincaid readability score is the most common readability metric, including other metrics will serve to provide more robust feedback to the user with regard to the complexity and structure of their written text.



