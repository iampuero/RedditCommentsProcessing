# Hola
## Dependencias:
### Docker
Toda esta parte del proyecto es manejada utilizando Docker. Para eso es necesario tenerlo instalado:
- Windows, en el caso de utilizar este SO es necesario descargar [Docker Hub](https://docs.docker.com/docker-for-windows/install/). A menos que tengas Windows Shell.
- Mac, desafortunadamente nunca he utilizado Docker en Mac, pero segun la página tambien es necesario [Docker Hub](https://docs.docker.com/docker-for-mac/install/).
- Linux, en este caso si instala como cualquier programa desde la [terminal](https://docs.docker.com/engine/install/ubuntu/).

### Python
Para ejecutar los contenedores utilizamos _docker-compose_. En el caso de Linux es necesario tener instalada las siguientes librerias de Python: py-pip, python-dev, libffi-dev, openssl-dev, gcc, libc-dev, and make.

### Docker-compose
Como se menciona en el punto anterior es necesario tener instalado docker-compose, independiende del sistema operativo es necesario [instalarlo por comandos](https://docs.docker.com/compose/install/).

## Ejecución:
Primero es necesario crear los containers:

`docker-compose build`

Luego se ejecuta con:

`docker-compose up`

el proceso se termina como cualquier otro proceso (CTR+c).
