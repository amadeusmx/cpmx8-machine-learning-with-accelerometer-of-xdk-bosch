#Activity recognizer
import sys
from math import sqrt
import itertools
from pyspark import SparkContext
from pyspark.mllib.linalg import Matrices, Vectors
from pyspark.mllib.tree import DecisionTree, DecisionTreeModel
from pyspark.mllib.tree import RandomForest, RandomForestModel
from pyspark.mllib.util import MLUtils
from time import time, sleep
from pyspark.mllib.stat import Statistics
#import datetime
import serial
from pyspark import rdd
from pprint import pprint
from pyspark import SparkContext


#############################
# # # # # Functions # # # # #
#############################
def computeResultantAcc(xx,yy,zz):
	Result = []
	for a,b,c in itertools.izip(xx,yy,zz):
		Result = sqrt(((a)*(a))+((b)*(b))+((c)*(c)))
	return Result;

def getComputations(x,y,z):
	features = []
	acc_x = x.map(lambda x:x)
	acc_y = y.map(lambda y:y)
	acc_z = z.map(lambda z:z)

	x_mean = acc_x.mean()
	y_mean = acc_y.mean()
	z_mean = acc_z.mean()
	features.append(x_mean)
	features.append(y_mean)
	features.append(z_mean)

	x_variance = acc_x.variance()
	y_variance = acc_y.variance()
	z_variance = acc_z.variance()
	features.append(x_variance)
	features.append(y_variance)
	features.append(z_variance)

	x_stdev = acc_x.stdev()
	y_stdev = acc_y.stdev()
	z_stdev = acc_z.stdev()
	features.append(x_stdev)
	features.append(y_stdev)
	features.append(z_stdev)

	avgabsDiff_x = acc_x.map(lambda x:x-x_mean).mean()
	avgabsDiff_y = acc_y.map(lambda y:y-y_mean).mean()
	avgabsDiff_z = acc_z.map(lambda z:z-z_mean).mean()
	features.append(avgabsDiff_x)
	features.append(avgabsDiff_y)
	features.append(avgabsDiff_z)

	Resultant = computeResultantAcc(acc_x.collect(),acc_y.collect(),acc_z.collect())
	features.append(Resultant)

	Diff_axs = float(float(x_mean) - float(y_mean))
	features.append(Diff_axs)

	return features;


##################################
# # # # # Configurations # # # # #
##################################
#Vars
SECONDS = 100000000
ONE_SECOND = 100000000
Activities = ["Walking","Jogging","Standing","Sitting"]


#apache spark
sc = SparkContext(appName="Activity recognizer")
#read model
#PredictionModel = DecisionTreeModel.load(sc, "/usr/local/spark-2.1.1/cpmx8/saved_models/two_decisionTree")
PredictionModel = RandomForestModel.load(sc, "/usr/local/spark-2.1.1/cpmx8/saved_models/two_randomForest")


############################
# # # # # Begining # # # # #
############################
#Eternal loop
while True:
	#pass

	#Set acumulator sensor variables
	acc_x = []
	acc_y = []
	acc_z = []
	g_acc = []
	#sleep(5)
	tdiff = 0
	t1 = time()
	while float(tdiff) < float(SECONDS/ONE_SECOND):
		#Serial port
		ser = serial.Serial('/dev/ttyACM0', 2000000, timeout=2, xonxoff=False, rtscts=False, dsrdtr=False) #Tried with and without the last 3 parameters, and also at 1Mbps, same happens.
		ser.flushInput()
		ser.flushOutput()
		#pass
		
		#read sensor
		data_raw = ser.readline()

		#parse the data
		parsed = data_raw.split(',')

		#send to array or list to acumulators
		acc_x.append(float(parsed[0]))
		acc_y.append(float(parsed[1]))
		acc_z.append(float(parsed[2].split('\n')[0]))
		#verify the time to reloop
		print(float(parsed[0]),float(parsed[1]),float(parsed[2]))
		t2 = time()
		tdiff = t2 - t1
		ser.close()
	#compute statistical data with acumulators
	features = getComputations(sc.parallelize(filter(None,acc_x)),\
							   sc.parallelize(filter(None,acc_y)),\
							   sc.parallelize(filter(None,acc_z))\
							   )
	
	#query model for prediction
	prediction = PredictionModel.predict(features)#.map(lambda r: r.features))

	#get result
	#Translate result to correct activity word
	Result = Activities[int(prediction)]
	print("----------------------------------------------------")
	print("    ------------------" + str(Result) + "------------------")
	print("----------------------------------------------------")
	sleep(0.5)
	#send result to server
