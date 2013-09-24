import csv
import sys

if len(sys.argv) < 2:
	sys.exit('Error: Please include an input file.  Example python script.py input.csv')

with open(sys.argv[1], 'rb') as csvfile:
	reader = csv.reader(csvfile)
	words = set()
	for row in reader:
		words.add(row[0])

print len(words)
