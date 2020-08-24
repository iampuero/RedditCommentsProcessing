# Proyecto de integración BigData - Reddit Comments
> Integración de plataformas **Kafka** (Producer) -> **Spark/Storm** (Processing) -> **Cassandra**
> Comparación técnica de processing utilizando Spark y Storm desde Kafka

## Instrucciones de uso

**Instalar la distribución recomendada de java de ser necesario**
``sudo apt install default-jre``

### Kafka

**Instalación y ejecución de kafka**

``wget https://www.apache.org/dyn/closer.cgi?path=/kafka/2.5.0/kafka_2.12-2.5.0.tgz``

``tar -xzf kafka_2.12-2.5.0.tgz``

**Iniciar zookeeper y kafka server**

``cd kafka_2.12-2.5.0``

``./bin/zookeeper-server-start.sh config/zookeeper.properties``

``./bin/kafka-server-start.sh config/server.properties``

**Crear topic Reddit**

``./bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic Reddit``

* Usar python para crear un productor ``python3 kproducer.py``

### Spark 

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

``./spark2.4/bin/spark-submit --jars spark2.4/jars/spark-streaming-kafka-0-10-assembly_2.11-2.4.6.jar  --packages anguenot/pyspark-cassandra:2.4.0 sparkafka.py localhost 9092``

### Storm

**Compilación de proyecto**
```shell
$ cd StormConsumer/code
$ mvn install
```
primero nos movemos dentro de la carpeta code, creamos un ejecutable .jar con `mvn install` y luego nos devolvemos.

**Ejecutar tareas en storm**
Nuestra aplicación de Storm se ejecuta utilizando el .jar generado:
```shell
$ cd StormConsumer/code
$ java -jar ./target/storm-app-1.0-SNAPSHOT-jar-with-dependencies.jar
```

### Cassandra

**Descargar y descomprimir**

``wget https://downloads.apache.org/cassandra/3.11.7/apache-cassandra-3.11.7-bin.tar.gz``

``tar -xzf apache-cassandra-3.11.7-bin.tar.gz``

**Generación de KeySpace y Tabla:**
```shell
$ cqlsh # enter the terminal of cassandra
cqlsh> CREATE KEYSPACE IF NOT EXISTS test_text WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'} AND durable_writes = true;
cqlsh> CREATE TABLE IF NOT EXISTS test_text.counter (number bigint, update_date timestamp, count bigint, PRIMARY KEY(number));"

```

**Alternativa con docker compose**
Primero es necesario tener instalado docker y docker-compose:
- Windows, en el caso de utilizar este SO es necesario descargar [Docker Hub](https://docs.docker.com/docker-for-windows/install/). A menos que tengas Windows Shell.
- Mac, desafortunadamente nunca he utilizado Docker en Mac, pero segun la página tambien es necesario [Docker Hub](https://docs.docker.com/docker-for-mac/install/).
- Linux, en este caso si instala como cualquier programa desde la [terminal](https://docs.docker.com/engine/install/ubuntu/).

#### Python
Para ejecutar los contenedores utilizamos _docker-compose_. En el caso de Linux es necesario tener instalada las siguientes librerias de Python: py-pip, python-dev, libffi-dev, openssl-dev, gcc, libc-dev, and make.

#### Docker-compose
Como se menciona en el punto anterior es necesario tener instalado docker-compose, independiende del sistema operativo es necesario [instalarlo via comandos](https://docs.docker.com/compose/install/), se adjunta el link de instalación pues varia entre SO. 

#### Ejecución
Con esta alternativa no es necesario crear el keyspace y la tabla:
```shell
$ docker-compose build
```
Luego se ejecuta con:
```shell
$ docker-compose up
```
el proceso se termina como cualquier otro proceso (CTR+c).

### Streamlit

``pip3 install streamlit seaborn matplotlib pandas cassandra-driver``

``streamlit run vis.py``