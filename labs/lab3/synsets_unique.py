import csv
import sys

if len(sys.argv) < 2:
	sys.exit('Error: Please include an input file.  Example python script.py input.csv')

with open(sys.argv[1], 'rb') as csvfile:
	reader = csv.reader(csvfile)
	table = {}
	for row in reader:
		word = row[0]
		if word in table :
			table[word].append(row[1])
		else :
			table[word] = [row[1]]

print len(table.keys())
