from pyspark import SparkContext,StorageLevel
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from pyspark.conf import SparkConf
from pyspark_cassandra import CassandraSparkContext,Row,streaming
import pyspark_cassandra
import string
from json import loads


whitelist = string.letters + ' '
STOP = ["a","about","above","after","again","against","all","am","an","and","any","are","aren't","as",
        "at","be","because","been","before","being","below","between","both","but","by","can't","cannot",
        "could","couldn't","did","didn't","do","does","doesn't","doing","don't","down","during","each","few",
        "for","from","further","had","hadn't","has","hasn't","have","haven't","having","he","he'd","he'll",
        "he's","her","here","here's","hers","herself","him","himself","his","how","how's","i","i'd","i'll",
        "i'm","i've","if","in","into","is","isn't","it","it's","its","itself","let's","me","more","most",
        "mustn't","my","myself","no","nor","not","of","off","on","once","only","or","other","ought","our",
        "ours	ourselves","out","over","own","same","shan't","she","she'd","she'll","she's","should","shouldn't",
        "so","some","such","than","that","that's","the","their","theirs","them","themselves","then","there","there's",
        "these","they","they'd","they'll","they're","they've","this","those","through","to","too","under","until","up",
        "very","was","wasn't","we","we'd","we'll","we're","we've","were","weren't","what","what's","when","when's","where",
        "where's","which","while","who","who's","whom","why","why's","with","won't","would","wouldn't","you","you'd","you'll",
        "you're","you've","your","yours","yourself","yourselves","just","like","will","can"]

def updateFunc(new_values, last_sum):
  count = 0
  new_ids = 0
  counts = [field[0] for field in new_values]
  ids = [field[1] for field in new_values]
  if last_sum:
    count = last_sum[0]
    new_ids = last_sum[1]

  return sum(counts) + count, sum(ids) + new_ids


def actualiza2(newcount,oldcount):
    if oldcount == None:
        oldcount=0
    return sum(newcount,oldcount)


conf = SparkConf().setAppName("PySpark Cassandra Test").set("spark.cassandra.connection.host","localhost")
sc = CassandraSparkContext(conf=conf)
sc.setLogLevel("WARN")
def cassandraSend(values):
    #print(values)
    rdd = sc.parallelize([{"subreddit": values[0],"word": values[1],
    "count":values[3],"score":values[2]}])
    rdd.saveToCassandra("reddit","word_counter")

ssc = StreamingContext(sc, 1)
ssc.checkpoint("checkpoint")

dks = KafkaUtils.createDirectStream(ssc, ['Reddit'], {"bootstrap.servers": 'localhost:9092'})

#scores
scores = dks.map(lambda x: loads(x[1])) \
          .flatMap(lambda x: (((x["subreddit"],y),x["ups"]-x["downs"]) for y in ''.join(c for c in x["body"].lower() if c in whitelist).split() if (len(y)<15 and y not in STOP)) )\
          .reduceByKey(lambda x,y:x+y)\
          .map(lambda x: (x,1))\
          .reduceByKey(lambda x,y: x+y)\
          .map(lambda x: ((x[0][0][0],x[0][0][1]),(x[0][1],x[1])))

#counts = dks.map(lambda x: loads(x[1])) \
#          .flatMap(lambda x: (((x["subreddit"],y),1) for y in x["body"].lower().replace(".","").replace(",","").split() if len(y)<15 ))\
#          .reduceByKey(lambda x,y:x+y)

#totalscores = counts.updateStateByKey(actualiza2)
totalscores = scores.updateStateByKey(updateFunc)
csrdd = totalscores.map(lambda x:{"subreddit": x[0][0],"word": x[0][1],"count":x[1][0],"score":x[1][1]})
#csrdd = totalscores.map(lambda x:{"subreddit": x[0][0],"word": x[0][1],"count":x[1],"score":0})
csrdd.saveToCassandra("reddit","word_counter")
#wc.map(lambda x: cassandraSend([x[0],x[1],x[2],x[3]]))
#directKafkaStream.pprint()
scores.pprint()


ssc.start()             # Start the computation
ssc.awaitTerminationOrTimeout(20)  # Wait for the computation to terminate
ssc.stop()
