6.885 Lab 4
Tanya Liu (tanyaliu@mit.edu)
Jeff Chan (jeffchan@mit.edu)

== Running the matcher
USAGE: python matcher.py [train|test] [truth.csv]

# Reading from locu_test.json and foursquare_test.json. Output to matches_test.csv
python matcher.py

# Reading from locu_test.json and foursquare_test.json. Output to matches_test.csv
python matcher.py test

# Reading from locu_train.json and foursquare_train.json. Output to matches_train.csv
python matcher.py train

# Reading from locu_train.json and foursquare_train.json. Output to matches_train.csv. Score using truth.csv
python matcher.py train truth.csv

== Dependencies
Python 2.6 or 2.7 -- no additional packages
