from pyspark import SparkContext

import json
import time
import math

from term_tools import get_terms
from difflib import get_close_matches
from operator import add

HOST = 'local'
AWS_KEY = 'lJPMR8IqPw2rsVKmsSgniUd+cLhpItI42Z6DCFku'

### Load Corpus ###
print 'loading context'
sc = SparkContext(HOST, 'tf-idf', pyFiles=['term_tools.py'])

print 'loading corpus'
lay = sc.textFile('s3n://AKIAJFDTPC4XX2LVETGA:'+AWS_KEY+'@6885public/enron/*.json')
# lay = sc.textFile('s3n://AKIAJFDTPC4XX2LVETGA:'+AWS_KEY+'@6885public/enron/lay-k.json')

json_lay = lay.map(lambda x: json.loads(x)).cache()
print 'json lay count', json_lay.count()

### Helper Methods ###
# Input: [{sender: 'sender', term: 'term'} ...]
# Output: {'sender1': 2, 'sender2': 3}
def single_term_freq(term_sender_pairs):
	freq = {}
	for pair in term_sender_pairs:
		sender = pair['sender']
		if sender in freq:
			freq[sender] += 1
		else:
			freq[sender] = 1
	return freq

# Input: Email json objects
# Output: [{term,sender}...]
def term_sender_pairs(email):
	sender = email['sender']
	master_email = sender #default
	if sender in send_to_master.value:
		master_email = send_to_master.value[sender]
	return map(lambda x: {'term': x, 'sender': master_email}, get_terms(email['text']))

# Input: (term, [{sender,term}, {sender,term}])
# Output: [(term, (sender, freq) ...]
def sender_term_freq(term_pair):
	term, pairs = term_pair
  tf = single_term_freq(pairs)
  return map(lambda x: (term, x), tf.items())

def consolidate_emails(pair):
	letter,email_pairs = pair
	names = [x[1] for x in email_pairs]

	name_to_email = dict()
	for email,name in email_pairs:
		name_to_email[name] = email

	consolidated = []
	for email,name in email_pairs:
		matches = get_close_matches(name, names, cutoff=0.75)
		matching_emails = set()
		for match in matches:
			matching_emails.add(name_to_email[match])
		consolidated.append((email, matching_emails))
	
	return map(lambda x: x, consolidated)


### Disambiguate ###
# Get a list of unique sender emails from the corpus
unique_senders = json_lay.map(lambda x: x['sender']).distinct()

# Sort by the first letter of names (where name is the stuff before the @ symbol)
sorted_names = unique_senders.map(lambda x: (x,x.split('@')[0])).groupBy(lambda x: x[1][0], 500)

# Create a master dictionary of consolidated emails. Example 'a.b@yahoo.com' => ['a.b@enron.com', 'a.b@yahoo.com']
combined = sorted_names.flatMap(consolidate_emails).flatMap(lambda x: map(lambda y: (y, x[0]), x[1])).collectAsMap()

# Broadcast to all nodes
send_to_master = sc.broadcast(combined)


### Calculate per-term IDF ###
term_count = json_lay.flatMap(lambda email: get_terms(email['text'])).map(lambda term: (term, 1)).reduceByKey(add)
per_term_idf = term_count.map(lambda term: (term[0], math.log(516893.0 / term[1]))).cache()

### Get term/sender pairs ###
term_sender_pairing = json_lay.flatMap(term_sender_pairs).groupBy(lambda x: x['term'], 500)

### Find sender-term freq ###
sender_tf = term_sender_pairing.flatMap(sender_term_freq).cache()

### Find TF-IDF ###
tfidf = sender_tf.join(per_term_idf, 500).map(lambda x:{'sender': x[1][0][0], 'term':x[0], 'tf-idf':x[1][0][1]*x[1][1]})

output = tfidf.collect()
for x in output:
  print x