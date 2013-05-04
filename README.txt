README.txt
CS171 - Project III
Ryan Mitchell, Yuki Yamada

Wikipedia Around the Globe: 
The Where and When of Language

Data:
Our data is stored in 50MB .csv file, all-wikipedia.csv. We have uploaded this to a dropbox share and sent it to the TFs. In addition to that larger .csv file, which was the raw edit data collected, we also use 20 .json files (used in the map visualization) and additionally data.csv (used in the streamgraph visualization).

In addition to those files, we have included all-wikipedia-normalized.csv. This is the file used in the Map Visualization, with data counts normalized by WikiEditScore (See report).


Code: The visualizations are encoded in index.html. They should be opened via an HTTP request rather than from file:// , with a local HTTP server running in order to access the cross-domain file request. Alternatively, it can be viewed in Firefox from a local file, or accessed at: http://javasaur.com/wikimap/index.html .

For visualization usability, the visualiation loads an intro.js tutorial guide, as well as providing users with walkthrough elements to identify highlights in the data.





Included Files:
/data-source/all-wikipedia.csv -- Raw data file as collected by scrapers.
/data-source/all-wikipedia-NORMALIZED.csv  -- Raw data file as collected by scrapers, with datacounts normalized according to WikiEditScore (See report).
/scripts/csv_generator.py - reads all-wikipedia.csv and generate the .csv files required for the streamgraph visualization.
/scripts/dataCounter1.1.py - reads all-wikipedia.csv and outputs a counts.csv file. Used to keep track of our data collection progress and ensure that we had collected sufficient data from each langauge 
/scripts/dataNormalizer.py - reads all-wikipedia.csv and outputs a new all-wikipedia-normalized.csv file with the correct number of edits in each language (see Map Creation section of report).
/scripts/formatter-json-decLat.py - reads all-wikipedia.csv and outputs the .json files for each language and hour slice. decLat refers to the fact that this generator creates the output files to a precision of 0.1 degrees latitude/longitude. (DEPRECATED IN PROJECT III - SEE formatter-json-decLat-withLanH.py )
/scripts/formatter-json-intLat.py - reads all-wikipedia.csv and outputs the .json files for each language's "All Times" slice. intLat refers to the fact that THIS generator combines the data into integer degree latitude/longitude buckets. These lower-resolution .json containers were used to increase the performance of the All Times selection.  (DEPRECATED IN PROJECT III SEE formatter-json-decLat-withLanH.py)
/scripts/merge.py - reads <language>-wikipedia.csv from dirs /1/, /2/, etc and combines them into a single output file all-wikipedia.csv and combined outputs for each language. This allowed to collect data from multiple scraper instances and quickly combine the data collected by each instance.
/scripts/output-fixer.py - this reads the .json files outputted from the formatter-json-*.py scripts, and fixes a trailing , in the feature collection array in each file.
/scripts/wikiScraper1.2.py - This is the data collection scraper, which when run generates a file for each language in the form <languagecode>-wikipedia.csv. For example, en-wikipedia.csv or de-wikipedia.csv. This script is currently set to collect data from only the top 10 languages, but we modified it as necessary to collect additional specific languages.
/scripts/formatter-json-decLat-withLanH.py - this is the new json generator for Project 3. In addition to 

Visualization:
./index.html
./data/etc
./js/etc
./css/etc