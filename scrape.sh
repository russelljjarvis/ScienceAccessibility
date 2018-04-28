#!/bin/bash
#declare -a arr=("scholar" "yahoo" "duckduckgo" "google" "bing")
#-o- OUTPUT_FILENAME, --output-filename OUTPUT_FILENAME
#The name of the output file. If the file ending is
#"json", write a json file, if the ending is "csv",
#write a csv file.
#--shell               Fire up a shell with a loaded sqlalchemy session.
#-n NUM_RESULTS_PER_PAGE, --num-results-per-page NUM_RESULTS_PER_PAGE
#The number of results per page. Must be smaller than
#100, by default 50 for raw mode and 10 for selenium
#mode. Some search engines ignore this setting.
#-p NUM_PAGES_FOR_KEYWORD, --num-pages-for-keyword NUM_PAGES_FOR_KEYWORD
#The number of pages to request for each keyword. Each
#page is requested by a unique connection and if
#                        possible by a unique IP (at least in "http" mode).
## now loop through the above array
declare -a arr=("google" "yandex" "bing" "yahoo" "baidu" "duckduckgo" "ask")
declare -a arr2=("GMO" "Vaccine" "Play+Dough" "Genetically+Modified+Organism" "Livestrong" "Neutron" "Neuromorphic hardware")
#python run.py --keyword "Vaccine" --search-engines="$i"
#python run.py --keyword "Play Dough" --search-engines="$i"
#python run.py --keyword "Genetically_Modified" --search-engines="$i"
#python run.py --keyword "Genetically_Modified" --search-engines="$i" 
#python run.py --keyword "Livestrong" --search-engines="$i" -o 

for i in "${arr[@]}"
do
   for j in "${arr2[@]}" 
   do
       echo "$i $j"
       python run.py --keyword "$j" --search-engines="$i" -p=50 --output-filename "$i$j.csv"
   done
done
