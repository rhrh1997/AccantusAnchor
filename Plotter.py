#!/usr/bin/python

import serial
import time
import matplotlib.pyplot as plt 
import numpy
from drawnow import *

ser = serial.Serial(port='/dev/tty.usbmodem14521',
					baudrate=115200, timeout=None)
print(ser.name)
ser.write(b'\r')
#print(ser.read())
time.sleep(.5)
ser.write(b'\r')
print('testing')
#print(ser.readline())
print(ser.readline())
print("Starting.... \n")

tempF= [30,40,50]
plt.ion() #Tell matplotlib you want interactive mode to plot live data
#fig = plt.figure()
#ax = plt.axes(projection='3d')
plt.ylim(-5.10,5.10)                                 #Set y min and max values
plt.xlim(-5.10,5.10)                                 #Set y min and max values
plt.title('Live Streaming Position Data')      #Plot the title
plt.grid(True)                                  #Turn the grid on
plt.ylabel('cm') 
cnt=0
 

ser.write("lec\r".encode())
print(ser.read(7))
while True:
	line = ser.readline()
	print(line.decode())
	if "POS" in line.decode():
		#print("contains")
		#arduinoString = arduinoData.readline() #read the line of text from the serial port
		dataArray = line.decode().split(',')   #Split it into an array called dataArray
		#P =    float( dataArray[1])            #Convert second element to floating number and put in P
		#pressure.append(P)                     #Building our pressure array by appending P readings
		p1 = plt.scatter(float(dataArray[4]), float(dataArray[3]))      #plot the temperature
		plt.pause(.05)                     #Pause Briefly. Important to keep drawnow from crashing
#		cnt=cnt+1
#		if(cnt>50):                            #If you have 50 or more points, delete the first one from the array
#			tempF.pop(0)                       #This allows us to just see the last 50 data points
		p1.remove()

	

#time.sleep(.5)
#ser.write(b'?')
#print(ser.readline())
ser.close()
