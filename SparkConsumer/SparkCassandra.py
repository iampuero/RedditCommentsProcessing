from pyspark.conf import SparkConf
from pyspark_cassandra import CassandraSparkContext,Row
import pyspark_cassandra


conf = SparkConf().setAppName("PySpark Cassandra Test").set("spark.cassandra.connection.host","localhost")

sc = CassandraSparkContext(conf=conf)
rdd = sc.parallelize([{
    "subreddit": "politics",
    "word": "ketan",
    "count":2,
    "score":4
    }
])
rdd.saveToCassandra("reddit","word_counter")