import json
import sys
import csv
import re

print 'USAGE: python matcher.py [train|test] [truth.csv]'

if len(sys.argv) >= 2:
	name = sys.argv[1]
else :
	name = 'test'

print 'Reading from locu_'+name+'.json and foursquare_'+name+'.json'
print 'Output to matches_'+name+'.csv'

file_a = open('locu_'+name+'.json', 'r+')
file_b = open('foursquare_'+name+'.json', 'r+')


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
	s = re.sub(r'[\s()\.,?!:;&\-\_\']', '', s)
	return s.lower()

def compare_phone(s1, s2):
	if s1 == None or s2 == None:
		return False
	else:
		s1 = ignore(s1)
		s2 = ignore(s2)
		return s1 != '' and s2 != '' and s1 == s2

def compare_address(s1, s2):
	if s1 == '' or s2 == '':
		return False
	else:
		# s1_match = re.match(r'([\d]+)\s?', s1)
		# s2_match = re.match(r'([\d]+)\s?', s2)
		# return s1_match != None and s2_match != None and s1_match.group(1) == s2_match.group(1)
		return ignore(s1) == ignore(s2)

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

	for entry_a in entries_a:
		for entry_b in entries_b:
			if entry_a['id'] in matched and entry_b['id'] in matched:
				break

			if ignore(entry_a['name']) == ignore(entry_b['name']) or edit_distance(entry_a['name'], entry_b['name']) <= 2:
				matches.append((entry_a['id'], entry_b['id']))
				matched.add(entry_a['id'])
				matched.add(entry_b['id'])
				break

			if compare_phone(entry_a['phone'], entry_b['phone']):
				matches.append((entry_a['id'], entry_b['id']))
				matched.add(entry_a['id'])
				matched.add(entry_b['id'])
				break

if len(sys.argv) == 3:
	truth = {}
	with open(sys.argv[2], 'rb') as file_truth:
		reader = csv.reader(file_truth, delimiter=',')
		for row in reader:
			truth[row[0]] = row[1]
	print Scorer(matches, truth)

with open('matches_'+name+'.csv', 'wb') as csvfile:
	writer = csv.writer(csvfile, delimiter=',')
	writer.writerow(['locu_id', 'foursquare_id'])
	for (a, b) in matches:
		writer.writerow([a, b])
