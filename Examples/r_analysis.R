
# Rscript
require("reticulate")
source_python("pickle_reader.py")
scraped <- read_pickle_file("scraped_new.p")
ARTCORPUS <- read_pickle_file("traingDats.p")
print(ARTCORPUS)
# Install
#install.packages("tm",repos="http://cran.u.r-project.org,depnencies=TRUE")  # for text mining
install.packages("SnowballC",repos="http://cran.us.r-project.org",dependencies=TRUE) # for text stemming
install.packages("wordcloud",repos="http://cran.us.r-project.org",dependencies=TRUE) # word-cloud generator
install.packages("RColorBrewer",repos="http://cran.us.r-project.org",dependencies=TRUE) # color palettes
install.packages("dplyr",repos="http://cran.us.r-project.org",dependencies=TRUE) # color palettes
library(data.table)
expr <- data.table(scraped)
# Load
library("tm")
library("SnowballC")
library("wordcloud")
library("RColorBrewer")

library(dplyr)
for (i in c(0:length(ARTCORPUS))){print(ARTCORPUS[i])}
#bind_tf_idf
#for (i in c(0:length(ARTCORPUS))){print(ARTCORPUS[[i]]$wcount)}
for (i in ARTCORPUS){print(i$wcount)}
fscience = list()
fnscience = list()
  cnt = 0
  for (i in scraped){
    if(i[11] == FALSE){
      fnscience[[paste(cnt)]] <- i
      cnt = cnt+1
      #fnscience.append(i)
    }
    if(i[11] == TRUE){
      fscience[[paste(cnt)]] <- i
      cnt = cnt+1
    }
  }
