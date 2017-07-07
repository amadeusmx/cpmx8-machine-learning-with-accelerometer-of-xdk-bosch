#Data feeder

#from pyspark import SparkContext
#from pyspark import rdd
import sys
import csv
import serial
import time
#Serial port
ser = serial.Serial('/dev/ttyACM0', 2000000, timeout=2, xonxoff=False, rtscts=False, dsrdtr=False) #Tried with and without the last 3 parameters, and also at 1Mbps, same happens.
ser.flushInput()
ser.flushOutput()
SIZE = 10000
ACTIVITY = 'Walkking'
USER = '1'
#sc = SparkContext(appName="Data feeder")


rowsize = 0
while rowsize < SIZE:
	#open file
	file = open('/usr/local/spark-2.1.1/cpmx8/pruebas/myCollection.csv', 'ab')
	writer = csv.writer(file)

	data_raw = ser.readline()
	timenow = int(time.time()*1000)
	row = data_raw.split(',')
	row[2] = row[2].split('\n')[0]
	row.append(timenow)
	row.append(ACTIVITY)
	row.append(USER)
	#data = ','.join(row)
	#save into file
	
	writer.writerow(row)
	
	#print(data)
	rowsize+=1
	#print(rowsize)
	print(str(rowsize) + " - " + str(row))
	#close file
	file.close()

print(str(SIZE) + " muestras capturadas, para activitdad: " + str(ACTIVITY))
sys.exit()
