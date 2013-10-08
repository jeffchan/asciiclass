import sys
import StringIO
import json
from mrjob.protocol import JSONValueProtocol
from mrjob.job import MRJob
from term_tools import get_terms
from mrjob.emr import EMRJobRunner 

AWS_ACCESS_KEY = 'AKIAJFDTPC4XX2LVETGA'
AWS_SECRET_KEY = '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'

class MRTf(MRJob):
    INPUT_PROTOCOL = JSONValueProtocol
    OUTPUT_PROTOCOL = JSONValueProtocol

    def mapper(self, key, email):
        for term in get_terms(email['text']):
            yield (email['sender'], term), 1

    def reducer_init(self):
        emr = EMRJobRunner(aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
        idf_parts = emr.get_s3_keys('s3://6885public/jeffchan/term-idfs/')
        self.word_to_idf = dict()
        for part in idf_parts:
            string = part.get_contents_as_string()
            io = StringIO.StringIO(string)
            for line in io:
                pair = json.loads(line)
                self.word_to_idf[pair['term']] = pair['idf']

    def reducer(self, term, howmany):
        tf = sum(howmany)
        sender,word = term
        idf = self.word_to_idf[word]
        tf_idf = tf * idf
        yield sender, {'word': word, 'tf-idf': tf_idf}

if __name__ == '__main__':
        MRTf.run()
