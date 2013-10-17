# Lab 6: Spark

*Assigned: Oct 10, 2013*

*Due: Thursday Oct 17, 2013 12:59PM (just before class)*

In this lab you will use [Spark](http://spark.incubator.apache.org), a parallel cluster computing framework designed to be easier to program and more efficient than MapReduce/Hadoop while providing the same degree of scalability.

You may also want to check out the [Spark NSDI 2012 Paper](http://www.cs.berkeley.edu/~matei/papers/2012/nsdi_spark.pdf) by Zaharia et al.

# Setup

## Amazon

There are several steps to set up Amazon and EC2 to run Spark:

1. Start the EC2 instance from [lab 1](https://github.com/mitdbg/asciiclass/tree/master/labs/lab1).  When you start the instance, take a look at the URL in the Amazon console.  It should have a segment of the form: `region=XX-YYYY-N` (example: `us-east-1` or `us-west-2`).  Note this region.
1. [Go to this website](https://6885.signin.aws.amazon.com/console) and login with the username `6885student` (we will give you the password on Piazza).
1. Head over to https://console.aws.amazon.com/ec2/home?region=REGION-NAME-HERE#s=KeyPairs after replacing REGION-NAME-HERE with the region that your ec2 instance from lab 1 runs in (see the first step above).
1. Click `Create Key Pair` and name the pair `sparklab-yourusername.pem`.  Download the keypair, and scp it to your EC2 instance from Step 1, e.g.:
 `scp -i YOUR-EC2-KEY.pem sparklab-yourusername.pem ubuntu@ec2-54-200-32-204.us-west-2.compute.amazonaws.com:~/`
1. On the EC2 machine, `chmod 600 sparklab-yourusername.pem`.

## Spark
SSH to your EC2 instance, download Spark, and unpack it (you may need to `sudo apt-get install git` before doing this):

````bash
git clone https://github.com/apache/incubator-spark.git
cd incubator-spark/ec2
git checkout d585613ee22ed9292a69e35cedb0d5965f4c906f
````

Set up your Amazon credentials:
````bash
export AWS_ACCESS_KEY_ID=AKIAJFDTPC4XX2LVETGA
export AWS_SECRET_ACCESS_KEY=<ACCESS KEY FROM PIAZZA>
````

AWS uses python 2.6 by default.  The Spark launch scripts assume python 2.7, so
install it:

	sudo yum install python27
	sudo rm /usr/bin/python
	sudo ln -s /usr/bin/python2.7 /usr/bin/python

Launch a Spark cluster with 7 machines:

````bash
./spark-ec2 -k sparklab-yourusername -i ~/sparklab-yourusername.pem -s 7 --instance-type=m1.small --region=XX-YYYY-N launch YOURUSERNAME-cluster
````

Note: 

* Replace `XX-YYYY-N` and `YOURUSERNAME` with your user name. You will want to do this in all of the subsequent `spark-ec2` commands
* The `-k` argument expects the original name you gave to the pem file through the AWS console
* The `-i` argument expects the path to the `.pem` file.

This process will take about 20 minutes.  If it spits out an error, you can try using the `start` command.

To stop or start your cluster (if you stop the lab half-way to get dinner, save some money!):

````bash
./spark-ec2 -k sparklab-yourusername -i ~/sparklab-yourusername.pem --region=XX-YYYY-N stop YOURUSERNAME-cluster
./spark-ec2 -k sparklab-yourusername -i ~/sparklab-yourusername.pem --region=XX-YYYY-N start YOURUSERNAME-cluster
````

# Run something on your cluster

First, login to the master node:

````bash
./spark-ec2 -k sparklab-yourusername -i ~/sparklab-yourusername.pem --region=XX-YYYY-N login YOURUSERNAME-cluster
```` 

Once you're on the Spark master node, download the file, `test.py`:

	wget https://raw.github.com/mitdbg/asciiclass/lab6/labs/lab6/test.py

And edit the file in two ways:

1. Replace `<MASTER URI>` with the contents in `~/spark-ec2/cluster-url`
1. Replace `<AWS KEY FROM PIAZZA>` 

`test.py` contains the following code:

````python
from pyspark import SparkContext

import json
import time

print 'loading'
sc = SparkContext("<MASTER URI>", "Simple App")
# Replace `lay-k.json` with `*.json` to get a whole lot more data.
lay = sc.textFile('s3n://AKIAJFDTPC4XX2LVETGA:<AWS KEY FROM PIAZZA>@6885public/enron/lay-k.json')

json_lay = lay.map(lambda x: json.loads(x)).cache()
print 'json lay count', json_lay.count()

filtered_lay = json_lay.filter(lambda x: 'chairman' in x['text'].lower())
print 'lay filtered to chairman', filtered_lay.count()

to_list = json_lay.flatMap(lambda x: x['to'])
print 'to_list', to_list.count()

counted_values = to_list.countByValue()
# Uncomment the next line to see a dictionary of every `to` mapped to
# the number of times it appeared.
#print 'counted_values', counted_values

# How to use a join to combine two datasets.
frequencies = sc.parallelize([('a', 2), ('the', 3)])
inverted_index = sc.parallelize([('a', ('doc1', 5)), ('the', ('doc1', 6)), ('cats', ('doc2', 1)), ('the', ('doc2', 2))])

# See also rightOuterJoin and leftOuterJoin.
join_result = frequencies.join(inverted_index)

# If you don't want to produce something as confusing as the next
# line's [1][1][0] nonesense, represent your data as dictionaries with
# named fields :).
multiplied_frequencies = join_result.map(lambda x: (x[0], x[1][1][0], x[1][0]*x[1][1][1]))
print 'term-document weighted frequencies', multiplied_frequencies.collect()
````

Run the test.py script:
````bash
/root/spark/pyspark test.py
/root/spark/pyspark test.py 2>/dev/null # if you don't want to see the java debugging output
````


You can also run a python prompt to play with pyspark interactively:
````bash
MASTER=`cat ~/spark-ec2/cluster-url` /root/spark/pyspark
````


Note: 

* The Spark instances run `python2.6`.  If you want pyspark to run 2.7 on all the nodes, you'll need to
muck with the launch scripts :(
* [The configuration documentation](http://spark.incubator.apache.org/docs/latest/configuration.html) describes knobs for tuning memory allocation, etc.  If your `.collect()` call is throwing memory errors, check out `spark.akka.frameSize`.


To read about more Spark functions, check out the [PySpark Documentation](http://spark.incubator.apache.org/docs/latest/api/pyspark/index.html).  While you won't likely be programming in Scala for this lab, the [Scala Documentation on Transformations and Actions](http://spark.incubator.apache.org/docs/latest/scala-programming-guide.html) has some nice English-language explanations of each function.


# Shut it down

To destroy the cluster once you're done:
````bash
./spark-ec2 -k sparklab-yourusername -i ~/sparklab-yourusername.pem --region=XX-YYYY-N destroy YOURUSERNAME-cluster
```` 

# Questions

Re-do `lab 5`'s TF-IDF analysis using Spark.  Include some amount (your choice) of sender disambiguation.

1. Describe the disambiguation you performed.  How did Spark affect (if at all) the choice of technique?

Reflect on your experience using Spark:

1. Compare your experience to using EMR.  What things did Spark simplify?  
2. Given Spark, why would you use EMR?
3. Were there any limitations to using the Spark model?
4. Describe in a few sentences how Spark would simplify an implementation 
   of pagerank over your answer in Lab 5 using EMR. 

**Bonus questions (optional)**

Implement [PageRank](http://en.wikipedia.org/wiki/PageRank) over the graph induced by the `from:` and `to:` fields in the Enron data sets in the S3 folder `6885public/enron/*.json`.  To make this easier, you may wish to refer to the [Spark implementation of PageRank over URLs](https://github.com/apache/incubator-spark/blob/master/python/examples/pagerank.py).  

1. Run for 10 iterations and report the ten nodes in the email graph with the highest PageRank, and their PageRank values.
1. Describe in a few sentences how Spark simplifies the implementation and improves the performance of this task over using Hadoop.


# Submission Instructions


Answer the questions above in a text file called "lab6-lastname", where lastname is your last name.  Make sure the text file also has your complete name.   Save your writeup and scripts in a zip file or tarball.   Upload it to the [course Stellar site](http://stellar.mit.edu/S/course/6/fa13/6.885/) as the "lab6" assignment.

Now you're almost done!  Go read the assigned paper(s) for today.

You can always feel free to contact us with questions on [Piazza](https://piazza.com/class/hl6u4m7ft8n373).

### Feedback (optional, but valuable)

If you have any comments about this lab, or any thoughts about the
class so far, we would greatly appreciate them.  Your comments will
be strictly used to improve the rest of the labs and classes and have
no impact on your grade. 

Some questions that would be helpful:

* Is the lab too difficult or too easy or too boring?  
* Did you look forward to any exercise that the lab did not cover?
* Which parts of the lab were interesting or valuable towards understanding the material?
* How is the pace of the course so far?
