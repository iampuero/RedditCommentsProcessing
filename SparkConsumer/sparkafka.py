from pyspark import SparkContext,StorageLevel
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from pyspark.conf import SparkConf
from pyspark_cassandra import CassandraSparkContext,Row,streaming
import pyspark_cassandra
from json import loads


def actualiza(newvals,oldvals):
    if oldvals == None:
        oldvals=(0,0)
    return (newvals[0]+oldvals[0],newvals[0]+oldvals[1])


def actualiza2(newcount,oldcount):
    if oldcount == None:
        oldcount=0
    return sum(newcount,oldcount)


conf = SparkConf().setAppName("PySpark Cassandra Test").set("spark.cassandra.connection.host","localhost")
sc = CassandraSparkContext(conf=conf)

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
          .flatMap(lambda x: (((x["subreddit"],y),x["ups"]-x["downs"]) for y in x["body"].lower().replace(".","").replace(",","").split() if len(y)<15) )\
          .reduceByKey(lambda x,y:x+y)\
          .map(lambda x: (x,1))\
          .reduceByKey(lambda x,y: x+y)\
          .map(lambda x: ((x[0][0][0],x[0][0][1]),(x[0][1],x[1])))

counts = dks.map(lambda x: loads(x[1])) \
          .flatMap(lambda x: (((x["subreddit"],y),1) for y in x["body"].lower().replace(".","").replace(",","").split() if len(y)<15 ))\
          .reduceByKey(lambda x,y:x+y)

totalscores = counts.updateStateByKey(actualiza2)
#csrdd = totalscores.map(lambda x:{"subreddit": x[0][0],"word": x[0][1],"count":x[1][0],"score":x[1][1]})
csrdd = totalscores.map(lambda x:{"subreddit": x[0][0],"word": x[0][1],"count":x[1],"score":0})
csrdd.saveToCassandra("reddit","word_counter")
#wc.map(lambda x: cassandraSend([x[0],x[1],x[2],x[3]]))
#directKafkaStream.pprint()
scores.pprint()


ssc.start()             # Start the computation
ssc.awaitTermination()  # Wait for the computation to terminate