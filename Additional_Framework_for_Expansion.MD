
### Additional Text Analysis Tools
The current tool uses the text-stat "Standard" metric. The ***standard*** metric evaluates the corpus using a variety of writing complexity algorithms (Gunning Fog, Flesch-Kincaid etc), and finds the average measurement using this list of metrics. The text-standard complexity metric tends to be more robust than any one metric, and it is less easily biased by smaller and longer text lengths.
The Flesch-Kincaid readability score - the most commonly used metric to assess readability - to quantify the complexity of all scraped text. We used this single metric intentionally, with the idea that  the main tool would be more straightforward to a user if the readability score was kept simple, so as to be used intuitively to improve readability. 

However, we understand that other features of text can (and perhaps should) be incoporated to provide even more context into a text's depth and complexity. Related, scientists may be interested in accessing these additional features for more hypothesis-driven questions about the complexity of scientific text. With that in mind, the current code has additional measurement metrics built in for these future endeavors. These include: 

| Text Metric |   Description of Measurement |
|----------|----------|
| Text-stat                                        | text reading level (complexity) |
| The Natural Language Processing Tool Kit (NLTK)  | text subjectivity and sentiment |
| Search Engine Factors      | page rank  |
| LZW (de-)compression-ratio | information entropy of text |
| Cluster centers            | clustering of text when organized using complexity, sentiment, word length and compression  ratios   |


### Additional web scraping tools
For this tool we include one metric of the broader internet - wikipedia - to represent a common reference text that people use for educational purposes. Again, we believe that the tool providing some context, but not overwhelming the user with information, is the key for usability and use for readability improvement.

However, we also believe it could be useful to include a more broad quantification of the general readability of the web. To address this, the code is also equipped for search engine queries of different and broad-ranging lists of search terms to assess readability of an eclectic range of text. This would further contextualize the readability of published scientific work with regard to both scientific and non-scientific topics engaged by the public on a more daily basis.


