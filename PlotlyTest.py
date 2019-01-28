#!/usr/bin/python

import plotly
import plotly.plotly as py
import plotly.tools as tls
import plotly.graph_objs as go
import numpy as np

stream_tokens = tls.get_credentials_file()['stream_ids']
token_1 = stream_tokens[-1]   # I'm getting my stream tokens from the end to ensure I'm not reusing tokens
token_2 = stream_tokens[-2]

stream_id1 = dict(token=token_1, maxpoints=1)
stream_id2 = dict(token=token_2, maxpoints=1)

N = 1
random_x = np.linspace(0, 1, N)
random_y0 = np.random.randn(N)+5
random_y1 = np.random.randn(N)
random_y2 = np.random.randn(N)-5

# Create traces
trace0 = go.Scatter(
	x = random_x,
	y = random_y0,
	mode = 'markers',
	name = 'markers',
	stream=stream_id1
)
trace1 = go.Scatter(
	x = random_x,
	y = random_y1,
	mode = 'lines+markers',
	name = 'lines+markers',
	stream=stream_id2
)

#data = [trace1, trace2]
#fig = go.Data([
#	go.Scatter(
#		x=[1, 2],
#		y=[3, 4], stream=stream_id1, name='trace1'
#	)
#])

data = [trace0, trace1]

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

#fig = go.Figure(data=data, layout=layout)
#fig = go.Data([trace1, trace2])
plot_url = py.plot(data, filename='test-streaming')


s_1 = py.Stream(stream_id=token_1)
s_2 = py.Stream(stream_id=token_2)

s_1.open()
s_2.open()

import time
import datetime
import numpy as np

k=10
i=0

while True:
	x = np.random.randn(N)+5
	delta = np.random.randint(4,10)
	y = np.random.randn(N)+5
	s_1.write(dict(x=x,y=y))
	s_2.write(dict(x=x,y=y))
	time.sleep(0.1)
	i += 1
s_1.close()
s_2.close()
#tls.embed('streaming-demos','124')
