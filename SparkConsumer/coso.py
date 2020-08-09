from cassandra.cluster import Cluster
from time import sleep
cluster = Cluster(["localhost"])
session = cluster.connect("reddit")

while True:
    rows = session.execute("SELECT * from word_counter WHERE count > 25 ALLOW FILTERING")
    data = [[row.subreddit,row.word,row.count] for row in rows]
    print (data)
    sleep(5)