from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils


# Create a local StreamingContext with two working thread and batch interval of 1 second
sc = SparkContext("local[2]", "RedditReciever")
ssc = StreamingContext(sc, 1)
directKafkaStream = KafkaUtils.createDirectStream(ssc, ['Reddit'], {"bootstrap.servers": 'localhost:9092'})


directKafkaStream.pprint()

ssc.start()             # Start the computation
ssc.awaitTermination()  # Wait for the computation to terminate