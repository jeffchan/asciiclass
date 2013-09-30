import json
import sys

if len(sys.argv) < 4:
	exit('USAGE: python matcher.py set_a.json set_b.json output.csv')

fa = open(sys.argv[1], 'r+')
fb = open(sys.argv[2], 'r+')

set_a = json.load(fa)
set_b = json.load(fb)