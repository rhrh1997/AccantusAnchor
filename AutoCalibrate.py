#!/usr/bin/python

import serial
import time
import matplotlib.pyplot as plt 
import numpy
from drawnow import *

ser = serial.Serial(port='/dev/tty.usbmodem14121',
				baudrate=115200, timeout=None)


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
	
def calculateAnchorPosition():
	sec.write("amt\r".encode())
	time.sleep(2)
	ser.write(b'\r')
	time.sleep(.5)
	ser.write(b'\r')
	print(ser.read(7))
	
	#need to read ranging to anchor 
	
	#need to capture and switch
	
	
def setupGraph():
	plt.ion() #Tell matplotlib you want interactive mode to plot live data
	#img = plt.imread("Apartment.jpg")
	#fig, ax = plt.subplots()
	#ax.imshow(img, extent = [0, 3.30, 0, 3.61])
	#fig = plt.figure()
	#ax = plt.axes(projection='3d')
	plt.ylim(-7.10,7.10)                                 #Set y min and max values
	plt.xlim(-7.10,7.10)                                 #Set y min and max values
	plt.title('Accantus Live Positioning')      #Plot the title
	plt.grid(True)                                  #Turn the grid on
	plt.ylabel('m') 
	plt.xlabel('m') 

	plt.scatter(0,0)
	plt.scatter(6.73, 4.85)
	plt.scatter(6.80, 0.0)
	plt.scatter(0.0, 4.85)


def onePoint():
	setupGraph()
	p1 = plt.scatter(0,0)
	while True:
		line = ser.readline()
		print(line.decode())
		if "1737" in line.decode(): #CHANGE DEVICE ID HERE BENJAMIN 
			
			#print("contains")
			dataArray = line.decode().split(',')   #Split it into an array called dataArray
			
			qualityVal = float(dataArray[6])
			#print(qualityVal)
		
			#Quality Metrics
			#if qualityVal > 20:
			p1.set_offsets([float(dataArray[3]), float(dataArray[4])])      #plot the first point
			plt.pause(.000005)                     #Pause Briefly. Important to keep drawnow from crashing
	

	
def twoPoints():
	setupGraph()
	p1 = plt.scatter(0,0)
	p2 = plt.scatter(0,0)
	cnt = 0
	while True:
		line = ser.readline()
		print(line.decode())
		if "POS" in line.decode():
			#print("contains")
			dataArray = line.decode().split(',')   #Split it into an array called dataArray
			qualityVal = float(dataArray[6])
			if qualityVal > 85:
				if float(dataArray[1]) == 0:
					p1.set_offsets([float(dataArray[4]), float(dataArray[3])])      #plot the first point
					plt.pause(.00000000005)                     #Pause Briefly. Important to keep drawnow from crashing
					#p1.remove()
				if float(dataArray[1]) == 1:
					p2.set_offsets([float(dataArray[4]), float(dataArray[3])])      #plot the first point
					plt.pause(.00000000005)                     #Pause Briefly. Important to keep drawnow from crashing
					#p2.remove()
#		cnt = cnt + 1 
#		if cnt > 300:
#				cnt = 0
#				ser.reset_input_buffer()

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
