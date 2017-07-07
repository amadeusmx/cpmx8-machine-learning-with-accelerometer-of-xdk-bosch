Ejemplo de un sistema de aprendizaje basado en machine learning.

A partir del movimiento de un sensor acelerometro en la mano o pierna de una persona, se debe predecir 
si dicha persona está caminando, trotando, si está parada o sentada.

Integra:

apache spark 2.1.1
Python 2.7
Mllib
Sensor XDK bosch

Pasos para hacer funcionar dicho ejemplo: (Tener un sensor bosch XDK)

Bajar el framework apache spark 2.1.1
Descomprimirlo en alguna carpeta de ubuntu linux

Declarar variables del sistema:

JAVA_HOME=/usr/lib/jvm/java-8-oracle/jre      (Cambia dependiendo de tu sistema)
export JAVA_HOME
PATH=$PATH:$JAVA_HOME
export PATH

SPARK_HOME=/usr/local/spark-2.1.1
export SPARK_HOME
PATH=$PATH:$SPARK_HOME
export PATH

export PYTHONPATH=$SPARK_HOME/python/:$PYTHONPATH

Correr los programas:

bin/spark-submit my_program.py


Es importante mencionar que se deben cambiar directorios declarados dentro de cada uno de los archivos:

Trainer, ubicación del archivo myCollection.csv
Trainer, ubicación donde se guardarán los modelos
Activity_recognizer, ubicación de los modelos guardados
Data_feeder, ubicación del archivo myCollection.csv

Finalmente al correr los programas te pedirá que resulevas dependencias...

pip install "dependencia requerida..."

Happy code!
