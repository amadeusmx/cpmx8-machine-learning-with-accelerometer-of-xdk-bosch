#Spark trainer
import sys
from math import sqrt
import itertools
from pyspark.sql import SparkSession
from pyspark.context import SparkConf
from pyspark.sql import *
from pyspark.sql.functions import split
from pyspark.sql.types import StructType
from pyspark.sql.types import *
from pyspark import rdd
from pprint import pprint
from pyspark import SparkContext
import pandas as pd
from itertools import chain
import numpy as np 
from pyspark.mllib.linalg import Matrices, Vectors
from pyspark.mllib.stat import Statistics
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.tree import DecisionTree, RandomForest, RandomForestModel


Debug = False

ONE_SECOND = 45
SECONDS = 50
FREQUENCY = 50
if Debug == True:
	Activities = ["Walking"]#,"Jogging","Standing","Sitting"]
if Debug == False:
	Activities = ["Walking","Jogging","Standing","Sitting"]
values_c = []

#########################################################################################################
#-------------------------------------------F U N C T I O N S-------------------------------------------#
#########################################################################################################
def computeResultantAcc(x,y,z):
	Result = []
	for a,b,c in itertools.izip(x,y,z):
		Result = sqrt(((a)*(a))+((b)*(b))+((c)*(c)))
	return Result;


######################
#Get the data from csv
######################
sSess = SparkSession \
    .builder \
    .master("local[*]") \
    .appName("test") \
    .getOrCreate()
sqlC = SQLContext(sparkContext=sSess.sparkContext, sparkSession=sSess)

#val sql = new SQLContext(sc)
# Read all the csv files written atomically in a directory
#userSchema = StructType().add("user_id", "integer").add("activity", "string").add("timestamp","long").createDecimalType(10,2).add("acc_x", "decimal").add("acc_y", "decimal").add("acc_z", "decimal")
csvDF = (sSess.read.options(header="true").options(inferSchema="true").format("csv").load("/usr/local/spark-2.1.1/cpmx8/myCollection.csv"))
#csvDF.printSchema()
#################
#Train the system
#################
csvDF.cache()
csvDF.createOrReplaceTempView('train_table')
if Debug == True:
	users = [1]
if Debug == False:
	users = [1]
	#users = csvDF.limit(1).select("user_id").distinct()


for activity in Activities:
	for user in users:#.rdd.map(lambda a: a.user_id).collect():
		if Debug == True:
			at = sSess.sql('SELECT `timestamp` FROM `train_table` WHERE `user_id`=\'' + str(user) + '\' AND `activity`=\'' + str(activity) + '\' LIMIT 100')
		if Debug == False:
			at = sSess.sql('SELECT `timestamp` FROM `train_table` WHERE `user_id`=\'' + str(user) + '\' AND `activity`=\'' + str(activity) + '\' LIMIT 5000')
		at.cache()
		activity_times = at.rdd
		if activity_times.isEmpty() != True:
			main_lista1 = at.rdd.map(lambda x:x.timestamp).collect()
			total = len(main_lista1)
			for unit in main_lista1:
				if (main_lista1.index(unit)+1) < total:
					values = []
					val1 = main_lista1[main_lista1.index(unit)+1] - main_lista1[main_lista1.index(unit)]
					if (val1) > ONE_SECOND and val1 < (ONE_SECOND+5):
						startWindow = main_lista1[main_lista1.index(unit)]
						stopWindow = main_lista1[main_lista1.index(unit)+1]
						interval = (main_lista1[main_lista1.index(unit)+1] - main_lista1[main_lista1.index(unit)])/ SECONDS
						#print(str(main_lista1[main_lista1.index(unit)]) + ' , ' + str(main_lista1[main_lista1.index(unit)+1]))

						a = sSess.sql('SELECT `acc_x`,`acc_y`,`acc_z`,`timestamp` FROM `train_table` WHERE `user_id`=\'' + str(user) + '\' AND `activity`=\'' + str(activity) + '\' AND timestamp >\'' + str(startWindow) + '\' AND timestamp <\'' + str(stopWindow + (1 * FREQUENCY)) + '\'')
						a.cache()
						
						### --- features
						
						if len(a.rdd.map(lambda x: x).collect()) > 0:

							acc_x = a.rdd.map(lambda x:x.acc_x)
							acc_y = a.rdd.map(lambda y:y.acc_y)
							acc_z = a.rdd.map(lambda y:y.acc_z)
							time_ = a.rdd.map(lambda t:t.timestamp)

							values.append(float(Activities.index(activity)))

							#double[] mean = feature.computeMean();
							#mean = Statistics.colStats(vector2).mean()
							#----------------------
							x_mean = acc_x.mean()
							y_mean = acc_y.mean()
							z_mean = acc_z.mean()

							values.append(x_mean)
							values.append(y_mean)
							values.append(z_mean)
							#----------------------
							#// the variance (between sitting and standing)
				            #double[] variance = feature.computeVariance();
							#----------------------
							x_variance = acc_x.variance()
							y_variance = acc_y.variance()
							z_variance = acc_z.variance()

							values.append(x_variance)
							values.append(y_variance)
							values.append(z_variance)
							#----------------------
							#// the standard deviation
	            			#double[] standardDeviation = FeatureUtils.computeStandardDeviation(accelerationData, mean);
							#----------------------
							x_stdev = acc_x.stdev()
							y_stdev = acc_y.stdev()
							z_stdev = acc_z.stdev()

							values.append(x_stdev)
							values.append(y_stdev)
							values.append(z_stdev)
							#// the average absolute difference
	            			#double[] avgAbsDiff = feature.computeAvgAbsDifference(accelerationData, mean);
	            			#----------------------
							avgabsDiff_x = acc_x.map(lambda x:x-x_mean).mean()
							avgabsDiff_y = acc_y.map(lambda y:y-y_mean).mean()
							avgabsDiff_z = acc_z.map(lambda z:z-z_mean).mean()

							values.append(avgabsDiff_x)
							values.append(avgabsDiff_y)
							values.append(avgabsDiff_z)
							#----------------------
							#// the average resultant acceleration
	            			#double resultant = feature.computeResultantAcc(accelerationData);
							#----------------------
							Resultant = computeResultantAcc(acc_x.collect(),acc_y.collect(),acc_z.collect())

							values.append(Resultant)
							#----------------------
							#----------------------
							#// the average difference between X and Y
	            			#double difference = feature.computeDifferenceBetweenAxes(mean);
	            			#----------------------
							Diff_axs = float(float(x_mean) - float(y_mean))

							values.append(Diff_axs)
							#print(values)
							#----------------------
				        ### --- features
				        values_c.append(values)
				    ### --- more than 1 second
				### --- if - before finalizing for loop
			### --- main activity-timestamp loop filtered by activity-user
		### --- The query got many results > 0
	### --- each user
### --- each activity

def labelData(datus):
    # label: row[end], features: row[0:end-1]
    return datus.map(lambda x:x).map(lambda row: LabeledPoint(row[0], row[1:]))

training_data, testing_data = labelData(sSess.sparkContext.parallelize(filter(None,values_c))).randomSplit([0.8, 0.2])
if Debug == True:
	numClassess = 2
if Debug == False:
	numClassess = int(len(Activities))

model1 = RandomForest.trainClassifier(training_data, numClasses=numClassess, categoricalFeaturesInfo={},
                                         numTrees=3, featureSubsetStrategy="auto",
                                         impurity='gini', maxDepth=4, maxBins=32)

#print model1.toDebugString()

model1.save(sSess.sparkContext, "/usr/local/spark-2.1.1/cpmx8/saved_models/accelerometer_sensor_activity_rec_randomForest")

model2 = DecisionTree.trainClassifier(training_data, numClasses=numClassess, maxDepth=20,
                                     categoricalFeaturesInfo={},
                                     impurity='gini', maxBins=32)
#print model2.toDebugString()

model2.save(sSess.sparkContext, "/usr/local/spark-2.1.1/cpmx8/saved_models/accelerometer_sensor_activity_rec_decisionTree")

sys.exit()
