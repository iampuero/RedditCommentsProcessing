# Proyecto de integración BigData - Reddit Comments
> Integración de plataformas **Kafka** (Producer) -> **Spark/Storm** (Processing) -> **Cassandra**
> Comparación técnica de processing utilizando Spark y Storm desde Kafka

### Instrucciones de uso

**Instalar la distribución recomendada de java de ser necesario**
``sudo apt install default-jre``

#### Kafka

**Instalación y ejecución de kafka**

``wget https://www.apache.org/dyn/closer.cgi?path=/kafka/2.5.0/kafka_2.12-2.5.0.tgz``
``tar -xzf kafka_2.12-2.5.0.tgz``

**Iniciar zookeeper y kafka server**

``cd kafka_2.12-2.5.0``
``./bin/zookeeper-server-start.sh config/zookeeper.properties``
``./bin/kafka-server-start.sh config/server.properties``

**Crear topic <TOPIC_NAME>**
``./bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic <TOPIC_NAME>``

* Usar python para crear un productor ``python3 kproducer.py``

#### Spark 

**DOCS de Spark**
* https://spark.apache.org/docs/2.4.6/api/python/

**Descargar, descomprimir, descargar módulo de streams para kafka**

``wget https://www.apache.org/dyn/closer.lua/spark/spark-2.4.6/spark-2.4.6-bin-hadoop2.7.tgz``
``tar -xzf spark-2.4.6-bin-hadoop2.7.tgz``
``cd spark.../jars``
``wget https://search.maven.org/remotecontent?filepath=org/apache/spark/spark-streaming-kafka-0-10-assembly_2.11/2.4.6/spark-streaming-kafka-0-10-assembly_2.11-2.4.6.jar``
``cd ../..``

**Ejecutar tareas en spark**

* Usar el script para recibir de kafka ``sparkafka.py``

``./spark2.4/bin/spark-submit --jars spark2.4/jars/spark-streaming-kafka-0-10-assembly_2.11-2.4.6.jar sparkafka.py localhost 9092``

#### Cassandra

**Descargar y descomprimir** 
``wget https://downloads.apache.org/cassandra/3.11.7/apache-cassandra-3.11.7-bin.tar.gz``
``tar -xzf apache-cassandra-3.11.7-bin.tar.gz``