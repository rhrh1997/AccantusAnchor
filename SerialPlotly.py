#!/usr/bin/python

import plotly
import plotly.plotly as py
import plotly.tools as tls
import plotly.graph_objs as go
import numpy as np
import time



###### Connecting via Serial #######

import serial 


try:
	ser = serial.Serial(port='/dev/tty.usbmodem000760002150',
				baudrate=115200, timeout=None)
except:
	print("ERROR: Unable to connect to the module. Check the cable or the port, it probably changed.")

def connectSerial():
	
	#Connect via serial and initiate DWM 
	print(ser.name)
	ser.write(b'\r')
	time.sleep(.5)
	ser.write(b'\r')
	print(ser.readline())


####### Commands #######

def callLec():
	ser.write("lec\r".encode())
	print(ser.read(7))


####### Streaming Data #######

stream_tokens = tls.get_credentials_file()['stream_ids']
token_1 = stream_tokens[-1]   # I'm getting my stream tokens from the end to ensure I'm not reusing tokens
token_2 = stream_tokens[-2]

#New streams are needed for each tags 
stream_id1 = dict(token=token_1, maxpoints=1)
stream_id2 = dict(token=token_2, maxpoints=1)


####### Setup Graphing #######


def setupGraph():
	N = 1
	random_x = np.linspace(0, 1, N)
	random_y0 = np.random.randn(N)+5
	random_y1 = np.random.randn(N)	
	
	trace0 = go.Scatter(
		x = random_x,
		y = random_y0,
		mode = 'lines+markers',
		name = '1737',
		stream=stream_id1
	)
	trace1 = go.Scatter(
		x = random_x,
		y = random_y1,
		mode = 'lines+markers',
		name = '4B16',
		stream=stream_id2
	)
	
	anchor0 = go.Scatter(
		x = 0,
		y = 0,
		mode = 'markers'
	)
	
	anchor1 = go.Scatter(
		x = 0,
		y = 4.85,
		mode = 'markers'
	)
	
	anchor2 = go.Scatter(
		x = 6.73,
		y = 4.85,
		mode = 'markers'
	)
	
	anchor3 = go.Scatter(
		x = 6.80,
		y = 0,
		mode = 'markers'
	)


	data = [trace0, trace1, anchor0, anchor1, anchor2, anchor3]

	layout = go.Layout(
		title='Streaming Two Traces',
		yaxis=dict(
			title='y for trace1'
		),
		yaxis2=dict(
			title='y for trace2',
			titlefont=dict(
				color='rgb(148, 103, 189)'
			),
			tickfont=dict(
				color='rgb(148, 103, 189)'
			),
			overlaying='y',
			side='right'
		)
	)

	plot_url = py.plot(data, filename='test-streaming')


s_1 = py.Stream(stream_id=token_1)
s_2 = py.Stream(stream_id=token_2)

#s_1.open()
#s_2.open()

####### Get Points  #######


def onePoint():
	setupGraph()
	s_1.open()
	
	while True:
		line = ser.readline()
		print(line.decode())
		if "1737" in line.decode():
			
			#quality metrics
			#print("contains")
			dataArray = line.decode().split(',')   #Split it into an array called dataArray
			
			qualityVal = float(dataArray[6])
			#print(qualityVal)
		
			#if qualityVal > 85:
			s_1.write(dict(x = float(dataArray[3]), y = float(dataArray[4]) ))     #plot the first point
				#plt.pause(.05)                     #Pause Briefly. Important to keep drawnow from crashing
	
	s_1.close()
	
def twoPoints():
	setupGraph()
	s_1.open()
	s_2.open()
	
	while True:
		line = ser.readline()
		print(line.decode())
		if "POS" in line.decode():
			#print("contains")
			dataArray = line.decode().split(',')   #Split it into an array called dataArray
			qualityVal = float(dataArray[6])
			if qualityVal > 85:
				if dataArray[2] == '5B0E':
					s_1.write(dict(x = float(dataArray[3]), y = float(dataArray[4])))     #plot the first point
					#plt.pause(.005)                     #Pause Briefly. Important to keep drawnow from crashing
					#p1.remove()
				if dataArray[2] == '4B16':
					s_2.write(dict(x = float(dataArray[3]), y = float(dataArray[4])))     #plot the first point
					#plt.pause(.005)                     #Pause Briefly. Important to keep drawnow from crashing
					#p2.remove()


			#P =    float( dataArray[1])            #Convert second element to floating number and put in P
	#		cnt=cnt+1
	#		if(cnt>50):                            #If you have 50 or more points, delete the first one from the array
	#			tempF.pop(0)                       #This allows us to just see the last 50 data points
#tls.embed('streaming-demos','124')
	
def main():
	connectSerial()
	callLec()
	twoPoints()
	ser.close()

main()
