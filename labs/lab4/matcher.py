import json
import sys
import csv

if len(sys.argv) < 5:
	exit('USAGE: python matcher.py set_a.json set_b.json truth.csv output.csv')

file_a = open(sys.argv[1], 'r+')
file_b = open(sys.argv[2], 'r+')

truth = {}
with open(sys.argv[3], 'rb') as file_truth:
	reader = csv.reader(file_truth, delimiter=',')
	for row in reader:
		truth[row[0]] = row[1]

set_a = json.load(file_a)
set_b = json.load(file_b)

class Scorer():
	true_pos = 0
	false_pos = 0
	true_neg = 0
	false_neg = 0

	def __init__(self, matches, truth):
		self.matches = matches # list of tuples (a_id, b_id)
		self.truth = truth
		self.score()

	def score(self):
		for i in xrange(0, len(matches)):
			(a_id, b_id) = self.matches[i]
			if a_id in self.truth and self.truth[a_id] == b_id:
				self.true_pos += 1
			else:
				self.false_pos += 1

	def precision(self):
		return self.true_pos / float(self.true_pos + self.false_pos)

	def recall(self):
		return self.true_pos / float(len(self.truth))

	def f1(self):
		precision = self.precision()
		recall = self.recall()
		return (2.0 * precision * recall) / (precision + recall)

	def __repr__(self):
		return 'PREC=' + str(self.precision()) + ' RECALL=' + str(self.recall()) + ' F1=' + str(self.f1())


def build_dict(entries, key):
	dictionary = {}
	for entry in entries:
		if entry[key] in dictionary:
			dictionary[entry[key]].append(entry)
		else:
			dictionary[entry[key]] = [entry]
	return dictionary

def ignore(s):
	return s

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

a_by_postal = build_dict(set_a, 'postal_code')
b_by_postal = build_dict(set_b, 'postal_code')

all_postal = set(a_by_postal.keys() + b_by_postal.keys())

results = {}
matched = set()
matches = []
for postal in all_postal:
	if postal == '':
		continue

	if postal in a_by_postal:
		entries_a = a_by_postal[postal] + a_by_postal['']
	else:
		entries_a = a_by_postal['']

	if postal in b_by_postal:
		entries_b = b_by_postal[postal] + b_by_postal['']
	else:
		entries_b = b_by_postal['']

	results[postal] = 0
	for entry_a in entries_a:
		for entry_b in entries_b:
			if edit_distance(entry_a['name'], entry_b['name']) == 0 and entry_a['id'] not in matched and entry_b['id'] not in matched:
				results[postal] += 1
				matches.append((entry_a['id'], entry_b['id']))
				matched.add(entry_a['id'])
				matched.add(entry_b['id'])
				break

# print sum([results[result] for result in results])

print Scorer(matches, truth)
