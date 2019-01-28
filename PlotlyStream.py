#!/usr/bin/python

import serial
import time
import plotly as plt
import numpy
from drawnow import *

ser = serial.Serial(port='/dev/tty.usbmodem14611',
				baudrate=115200, timeout=None)
plotly.tools.set_credentials_file(username='hassaanraza', api_key='czVpzjhNscjVYLHj0txF')


def connectSerial():
	print(ser.name)
	ser.write(b'\r')
	#print(ser.read())
	time.sleep(.5)
	ser.write(b'\r')
	#print(ser.readline())
	print(ser.readline())

def callLec():
	ser.write("lec\r".encode())
	print(ser.read(7))
	
def setupGraph():
	plt.ion() #Tell matplotlib you want interactive mode to plot live data
	#fig = plt.figure()
	#ax = plt.axes(projection='3d')
	plt.ylim(-5.10,5.10)                                 #Set y min and max values
	plt.xlim(-5.10,5.10)                                 #Set y min and max values
	plt.title('Live Streaming Position Data')      #Plot the title
	plt.grid(True)                                  #Turn the grid on
	plt.ylabel('m') 
	plt.xlabel('m') 

	plt.scatter(0,0)
	plt.scatter(3.30,3.61)
	plt.scatter(0.0, 3.61)
	plt.scatter(3.30,0.0)


def onePoint():
	setupGraph()
	p1 = plt.scatter(0,0)
	while True:
		line = ser.readline()
		print(line.decode())
		if "5D80" in line.decode():
			
			#quality metrics
			#print("contains")
			dataArray = line.decode().split(',')   #Split it into an array called dataArray
			
			qualityVal = float(dataArray[6])
			#print(qualityVal)
		
			if qualityVal > 85:
				p1.set_offsets([float(dataArray[3]), float(dataArray[4])])      #plot the first point
				plt.pause(.05)                     #Pause Briefly. Important to keep drawnow from crashing
	

	
def twoPoints():
	setupGraph()
	p1 = plt.scatter(0,0)
	p2 = plt.scatter(0,0)
	while True:
		line = ser.readline()
		print(line.decode())
		if "POS" in line.decode():
			#print("contains")
			dataArray = line.decode().split(',')   #Split it into an array called dataArray
			if float(dataArray[1]) == 0:
				p1.set_offsets([float(dataArray[4]), float(dataArray[3])])      #plot the first point
				plt.pause(.005)                     #Pause Briefly. Important to keep drawnow from crashing
				#p1.remove()
			if float(dataArray[1]) == 1:
				p2.set_offsets([float(dataArray[4]), float(dataArray[3])])      #plot the first point
				plt.pause(.005)                     #Pause Briefly. Important to keep drawnow from crashing
				#p2.remove()


			#P =    float( dataArray[1])            #Convert second element to floating number and put in P
	#		cnt=cnt+1
	#		if(cnt>50):                            #If you have 50 or more points, delete the first one from the array
	#			tempF.pop(0)                       #This allows us to just see the last 50 data points

		
connectSerial()
callLec()
onePoint()

#time.sleep(.5)
#ser.write(b'?')
#print(ser.readline())
ser.close()
