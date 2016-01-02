# Task2-Yelp

This repository holds the codes and documentations for doing city-wise comparison of hospitals from the Yelp Academic Dataset.

Softwares and Python Packages Needed:

Python 2.7.x
MongoDB 3.x
pymongo
json
pattern
nltk
Tableau

Dependencies and Ordering of running the Python files:

1. MongoDB database server has to be running at all times in the background, in order to run any of the Python files.

2. The following is one of the correct orders in which the python files should be run:

reviewCollectionBuilder.py
hospitalFilter.py
hospitalReviewFilter.py
charlotteHospitalFilter.py
charlotteHospitalReviewFilter.py
charlotteHospitalSentiment.py
madisonHospitalFilter.py
madisonHospitalReviewFilter.py
madisonHospitalSentiment.py
pittsburghHospitalFilter.py
pittsburghHospitalReviewFilter.py
pittsburghHospitalSentiment.py
evaluation.py

This order will produce the required csv files that can be used for further visualization using Tableau.

About some specific files:

1. While running the reviewCollectionBuilder.py file, a Memory Error may be thrown based on the system on which the code is run. To tackle this, the loading of the review json file has to be changed. I the code the entire review json file is decoded and temporarily stored inside a single variable, instead of doing this the decoded json file has to be line by line immediately inserted into the MongoDB collection. This will ensure that the entire review json file is not loaded into Main Memory, which in turn will make sure that no Memory Error is thrown.

2. The descriptions of what all the python files do are available at the start of each file.

3. evaluation.py file calculates the accuracy of the extracted phrases only for Charlotte hospitals, but the same code can be changed just a little bit to adapt to other cities as well.

4. The stats in results.csv file are used in the evaluation.py file.