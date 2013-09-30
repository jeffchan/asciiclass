import json
import sys

if len(sys.argv) < 4:
	exit('USAGE: python matcher.py set_a.json set_b.json output.csv')

fa = open(sys.argv[1], 'r+')
fb = open(sys.argv[2], 'r+')

set_a = json.load(fa)
set_b = json.load(fb)

def build_dict(entries, key):
	dictionary = {}
	for entry in entries:
		if entry[key] in dictionary:
			dictionary[entry[key]].append(entry)
		else:
			dictionary[entry[key]] = [entry]
	return dictionary

def edit_distance(s1, s2):
	# ignore punctuation and capitalization
	s1 = ignore(s1)
	s2 = ignore(s2)
	
	len1 = len(s1)
	len2 = len(s2)
	
	d = {}
	
	# initialize memoization table with extra row and col for dynamic programming
	for i in range(-1, len1) :
		d[(i, -1)] = i # for deletion
	for j in range(-1, len2) :
		d[(-1, j)] = j # for insertion
	
	for i in range(len1) :
		for j in range(len2) :
			# increase distance only if characters are different
			dist = 1 if s1[i] != s2[j] else 0
			
			d[(i,j)] = min(d[(i-1,j-1)] + dist, d[(i-1,j)] + 1, d[(i,j-1)] + 1)
			
			# the case of adjacent character swap
			if i > 0 and j > 0 and s1[i] == s2[j-1] and s1[i-1] == s2[j] :
				d[(i,j)] = min(d[(i,j)], d[(i-2,j-2)] + dist)

	return d[(len1-1, len2-1)]+1 # +1 because 0-index based

