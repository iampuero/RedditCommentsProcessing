from time import sleep
from json import dumps,loads
from kafka import KafkaProducer
from sys import argv

producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                        value_serializer=lambda x: dumps(x).encode('utf-8'))

with open("files/"+argv[1]) as O:
    print("Broadcasting",argv[1])
    for line in O:
        data = loads(line)
        producer.send('Reddit', value=data)
        sleep(2)

