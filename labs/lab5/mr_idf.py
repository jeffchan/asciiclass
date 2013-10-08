import sys
import math
from mrjob.protocol import JSONValueProtocol
from mrjob.job import MRJob
from term_tools import get_terms

TOTAL_DOCUMENTS = 516893

class MRIdf(MRJob):
    INPUT_PROTOCOL = JSONValueProtocol
    OUTPUT_PROTOCOL = JSONValueProtocol

    def mapper(self, key, email):
        terms = set(get_terms(email['text']))
        for term in terms:
            yield term, 1

    def reducer(self, term, howmany):
        occurences = sum(howmany)
        yield None, {'term': term, 'idf': math.log(float(TOTAL_DOCUMENTS) / occurences)}

if __name__ == '__main__':
        MRIdf.run()
