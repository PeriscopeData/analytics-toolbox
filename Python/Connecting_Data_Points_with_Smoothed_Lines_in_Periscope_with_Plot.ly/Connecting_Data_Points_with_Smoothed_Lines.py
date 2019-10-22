# SQL output is imported as a dataframe variable called 'df'
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go

# Create trace. Notice the reference to shape in the line argument of the trace. This is set to spline, generating smoothed connectors
trace = dict(
    x = df.week,
    y = df['count'],
    mode = 'lines+markers',
    type = 'scatter',
    name = 'count',
    line = dict(shape = 'spline', color = 'rgb(205, 12, 24)', width= 4, dash = 'dash'),
    marker = dict(symbol = "star-diamond", color = 'rgb(17, 157, 255)',size = 8),
    connectgaps = True
)

# Create layout parameter to assing axes titles and set margins
layout =  dict(
    xaxis = dict(title = 'Week'),
    yaxis = dict(title = 'Count'),
    margin = dict(
        l=70,
        r=10,
        b=50,
        t=10
    )
)

# Compose the final figure
data = [trace]
fig =  go.Figure(data = data, layout = layout)

# Use Periscope to visualize a dataframe, text, or an image by passing data to periscope.table(), periscope.text(), or periscope.image() respectively.
periscope.plotly(fig)