# Hola
De momento solo se esta ejecutando con todo montado de forma local:

## Ejecución local
### Dependencias
#### Java:
La mayoria de las tecnologias ocupadas utilizan Java, en el caso de no tenerlo instalado, ejecutar las siguientes lineas:
```shell
$ sudo apt update
$ sudo apt install default-jdk
```
#### Zookeeper:
Para poder ejecutar Kafka es necesario tener instalado Zookeeper (ZK), 

#### Maven:
Para compilar y ejecutar la aplicación es necesario tener maven.

### Comandos previos
#### Kafaka
Es necesario crear el topico por el cual pasaran los mensajes

#### Cassandra
Es necesario crear el keyspace:
```shell
$ cqlsh # enter the terminal of cassandra
cqlsh> CREATE KEYSPACE IF NOT EXISTS test_text WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'} AND durable_writes = true;
cqlsh> CREATE TABLE IF NOT EXISTS test_text.counter (number bigint, update_date timestamp, count bigint, PRIMARY KEY(number));"

```

#### Storm
Se tiene que compilar el proyecto:
```shell
$ cd code
$ mvn install
```
primero nos movemos dentro de la carpeta code, creamos un ejecutable .jar con `mvn install` y luego nos devolvemos.

### Ejecución:
#### 1. Zookeeper
Primero es necesario dejar ejecutando ZK y Kafka como servicios.
```shell
$ sudo systemctl start zookeeper
```
Para revisar el estado ejecutamos:
```shell
$ sudo systemctl status zookeeper
```
en el caso de que todo funcione deberia arrojar el siguiente mensaje:
```
● zookeeper.service - Apache Zookeeper server
     Loaded: loaded (/etc/systemd/system/zookeeper.service; disabled; vendor preset: enabled)
     Active: active (running)
       Docs: http://zookeeper.apache.org
   Main PID: 17226 (java)
      Tasks: 31 (limit: 19062)
     Memory: 62.6M
...
```

#### 2. Kafka
El proceso es similar para Kafka:
```shell
$ sudo systemctl start kafka
$ sudo systemctl status kafka
```
en el caso de que todo saliera bien se imprimira por pantalla un estado similar al presentado en ZK.

#### 3. Cassandra
En el caso de cassandra una vez instalado deberia esta activo como servicio, pero para estar seguros se siguen los mismos pasos que con ZK y kafka:
```shell
$ sudo systemctl start cassandra
$ sudo systemctl status cassandra
```

#### 4. Storm
Nuestra aplicación de Storm se ejecuta utilizando el .jar generado:
```shell
$ cd code
$ java -jar ./target/storm-app-1.0-SNAPSHOT-jar-with-dependencies.jar
```
esto es asumiendo que la terminal esta a la misma altura que este archivo `Readme.md`.

***
## Ejecución con docker
### Dependencias
#### Docker
Toda esta parte del proyecto es manejada utilizando Docker. Para eso es necesario tenerlo instalado:
- Windows, en el caso de utilizar este SO es necesario descargar [Docker Hub](https://docs.docker.com/docker-for-windows/install/). A menos que tengas Windows Shell.
- Mac, desafortunadamente nunca he utilizado Docker en Mac, pero segun la página tambien es necesario [Docker Hub](https://docs.docker.com/docker-for-mac/install/).
- Linux, en este caso si instala como cualquier programa desde la [terminal](https://docs.docker.com/engine/install/ubuntu/).

#### Python
Para ejecutar los contenedores utilizamos _docker-compose_. En el caso de Linux es necesario tener instalada las siguientes librerias de Python: py-pip, python-dev, libffi-dev, openssl-dev, gcc, libc-dev, and make.

#### Docker-compose
Como se menciona en el punto anterior es necesario tener instalado docker-compose, independiende del sistema operativo es necesario [instalarlo via comandos](https://docs.docker.com/compose/install/), se adjunta el link de instalación pues varia entre SO. 

### Ejecución
Primero es necesario crear los containers:
```shell
$ docker-compose build
```
Luego se ejecuta con:
```shell
$ docker-compose up
```
el proceso se termina como cualquier otro proceso (CTR+c).
