# Lab 4: Entity Resolution

*Assigned: 24, September 2013*

*Due: 1, October 2013, 12:59 PM (just before class)*

*MODIFIED, SEPTEMBER 25 -- There is no longer a one to one mapping (bijection) between entities in the Locu / foursquare data sets.  Some entities may have
no matches.*

In this lab, you will take two datasets that describe the same
entities, and identify which entity in one dataset is the same as an
entity in the other dataset.  Our datasets were provided by Foursquare
and Locu, and contain descriptive information about various venues
such as venue names and phone numbers.  

Rather than have you compete against yourself, we've turned this lab
into a competition: students will submit their best matching
algorihtms and try to beat one-another on a leaderboard to identify
the best algorithm.  You may enter this competition yourself or as a
team of up to 3 students.  We will give a nice prize to the winning
team or teams.

This lab uses several files for you to test your entity resolution algorithms on:
 * [locu_train.json](https://s3.amazonaws.com/6885public/foursquare-locu+challenge/hard/locu_train_hard.json)
 * [foursquare_train.json](https://s3.amazonaws.com/6885public/foursquare-locu+challenge/hard/foursquare_train_hard.json)
 * [matches_train.csv](https://s3.amazonaws.com/6885public/foursquare-locu+challenge/hard/matches_train_hard.csv)

The `json` files contain a json-encoded list of venue attribute
dictionaries.  The `csv` file contains two columns, `locu_id` and
`foursquare_id`, which reference the venue `id` fields that match in
each dataset.

Your job is to write a script that will load both datasets and
identify matching venues in each dataset.  Measure the [precision,
recall, and F1-score](https://en.wikipedia.org/wiki/F-score) of your
algorithm against the ground truth in `matches_train.csv`.  Once
you're satisfied with an algorithm that has high values for these
training data points, move on to the two test files:
 * [locu_test.json](https://s3.amazonaws.com/6885public/foursquare-locu+challenge/hard/locu_test_hard.json)
 * [foursquare_test.json](https://s3.amazonaws.com/6885public/foursquare-locu+challenge/hard/foursquare_test_hard.json)

Your job is to generate `matches_test.csv`, a mapping that looks like `matches_train.csv` but with mappings for the new test listings.  Here are a few notes:
 * The schemas for these datasets are aligned, but this was something that Locu and Foursquare engineers had to do ahead of time when we initially matched our datasets.
 * The two datasets don't have the same exact formatting for some fields: check out the `phone` field in each dataset as an example.  You'll have to normalize some of your datasets.
 * You might notice matches in matches_train.csv that you disagree with.  That's fair: our data comes from matching algorithms and crowds, both of which can be imperfect.  If you feel it makes your algorithm's training process better, feel free to blacklist (programmatically) certain training values.
 * There are many different features that can suggest venue similarity. Field equality is a good one: if the names or phone numbers of venues are equal, the venues might be equal.  But this is a relatively high-precision, low-recall feature (`Bob's Pizza` and `Bob's Pizzeria` aren't equal), and so you'll have to add other ones.  For example, [Levenshtein distance](https://en.wikipedia.org/wiki/Levenshtein_distance) between two strings offers finer granularity of how similar two strings are.  At Locu we have many tens of features, ranging from field equality to more esoteric but useful ones (e.g., "Does the first numeric value in the address field match?").
 * Since there are many features, you need some way to combine them.  A simple weighted average of values, where more important values (similar names) are weighed more highly will get you quite far.  In practice, you'd want to build a classifier that takes these features and learns the weights based on the training data.  If you're using Python and want to build a classifier, check out [scikit-learn](http://scikit-learn.org/).  We've seen good results with the decision tree ensemble/random forest techniques.  Note that this step will take time, so only do it if you've hand-rolled your own reasonable matcher already.
 * It's possible to be near 1 for precision/recall/F1 with enough training data and good enough machine learning models, but this took Locu engineers several months to get right.
 * These datasets aren't too large, but in practice require matching several million venues across datasets.  Performing an `O(N^2)` comparison on all venues would take too long in those cases so some heuristics are needed to narrow down the likely candidates.

# Submission Instructions

## Upload your best results to the leaderboard

To compete in the challenge, you should go to
[http://6885.csail.mit.edu](http://6885.csail.mit.edu). Once
you have registered for an account, you can upload your results and
also see the results of other students so that you can improve your
algorithm and compete for the grand prize!

On the website, you will need to submit your result file (`matches_test.csv`) and the script/program that outputs this file.  This script/program should be runnable from inside a directory containing the files `locu_train.json`, `foursquare_train.json`, `matches_train.csv`, `locu_test.json`,  and `foursquare_test.json`, and should output `matches_test.csv` based on these files.  It can be a script (preferred) or a directory with source code and a `README.txt` file describing how to compile/run your program.  Please make sure you include a list of packages that need to be installed on a stock Ubuntu 12 installation for your program to run.   We will run your program against a set of hidden test data (that we have not provided) as a final test of the top few teams' code.

*While we'll use `matches_test.csv` to identify the most promising teams, only programs that run on the data and emit the best `matches_test.csv` on our machine will be considered for a prize.*

## Upload a writeup to Stellar

In addition to competing in the challenge, please upload a text file to the [course Stellar site](http://stellar.mit.edu/S/course/6/fa13/6.885/) as the "lab4" assignment. Each team member should upload their own copy of this file (it is OK if uploads of team members are identical).

The text file should contain:

1. Your user name and registered email address on the competition site.
1. A list of your teammates.
1. Answers to the following questions:
 * Describe your entity resolution technique, as well as its precision, recall, and F1 score.
 * What were the most important features that powered your technique?
 * How did you avoid pairwise comparison of all venues across both datasets?
