# CPMX-8 XDK Bosch

## Resumen


Ejemplo de un sistema de aprendizaje basado en machine learning.

A partir del registro del sensor XDK (Bosch), se deberá predecir si dicha persona está caminando, trotando, de pie o sentada.

## Stack

* [Apache Spark](https://spark.apache.org/downloads.html) - 2.1.1
* [Python](https://www.python.org/downloads/) - 2.7
* [Mllib](https://spark.apache.org/mllib/)
* [Sensor XDK Bosch](https://xdk.bosch-connectivity.com/)

## Getting Started (Ubuntu)

Hacer funcionar el sensor XDK puedes encontrar la guía de inicio [aquí](https://xdk.bosch-connectivity.com/documents/37728/219851/XDK_Guide_WB_First_Steps.pdf/2687e19a-6e73-4803-94ed-6be59eaab010)

Descargar y descomprimir Apache Spark [download](https://d3kbcqa49mib13.cloudfront.net/spark-2.1.1-bin-hadoop2.7.tgz)

```bash
$ wget https://d3kbcqa49mib13.cloudfront.net/spark-2.1.1-bin-hadoop2.7.tgz
$ tar zxfv spark-2.1.1-bin-hadoop2.7.tgz
```

Declarar variables de entorno:

```bash
JAVA_HOME=/path/to/jvm
export JAVA_HOME
PATH=$PATH:$JAVA_HOME
export PATH

SPARK_HOME=/path/to/apache/spark
export SPARK_HOME
PATH=$PATH:$SPARK_HOME
export PATH

export PYTHONPATH=$SPARK_HOME/python/:$PYTHONPATH
```

Instalar dependencias de python
```bash
$ pip install wheel
$ pip install pandas
```

Correr los programas:

```bash
/path/to/spark-submit /path/to/my_program.py
```

Es importante mencionar que se deben cambiar directorios declarados dentro de cada uno de los archivos:

[Trainer](https://github.com/elden/cpmx8-machine-learning-with-accelerometer-of-xdk-bosch/blob/69eeee5d6c1136f86458e039991e8554a2d608e7/trainer.py), ubicación del archivo [myCollection.csv](https://github.com/elden/cpmx8-machine-learning-with-accelerometer-of-xdk-bosch/blob/69eeee5d6c1136f86458e039991e8554a2d608e7/trainer.py#L57)

[Trainer](https://github.com/elden/cpmx8-machine-learning-with-accelerometer-of-xdk-bosch/blob/69eeee5d6c1136f86458e039991e8554a2d608e7/trainer.py), ubicación donde se guardarán los modelos
 [L190](https://github.com/elden/cpmx8-machine-learning-with-accelerometer-of-xdk-bosch/blob/69eeee5d6c1136f86458e039991e8554a2d608e7/trainer.py#L190) [L197](https://github.com/elden/cpmx8-machine-learning-with-accelerometer-of-xdk-bosch/blob/69eeee5d6c1136f86458e039991e8554a2d608e7/trainer.py#L197)

[Activity_recognizer](https://github.com/elden/cpmx8-machine-learning-with-accelerometer-of-xdk-bosch/blob/69eeee5d6c1136f86458e039991e8554a2d608e7/Activity%20recognizer.py), ubicación de los modelos guardados [L84](https://github.com/elden/cpmx8-machine-learning-with-accelerometer-of-xdk-bosch/blob/69eeee5d6c1136f86458e039991e8554a2d608e7/Activity%20recognizer.py#L84)

[Data_feeder](https://github.com/elden/cpmx8-machine-learning-with-accelerometer-of-xdk-bosch/blob/69eeee5d6c1136f86458e039991e8554a2d608e7/Data%20feeder.py), ubicación del archivo [myCollection.csv](https://github.com/elden/cpmx8-machine-learning-with-accelerometer-of-xdk-bosch/blob/69eeee5d6c1136f86458e039991e8554a2d608e7/Data%20feeder.py#L22)

#### TODO

* Recibir los archivos a analizar y los directorios destino para evitar tener rutas absolutas =D

Happy code!
