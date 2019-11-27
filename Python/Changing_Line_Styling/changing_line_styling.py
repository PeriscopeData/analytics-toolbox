# SQL output is imported as a dataframe variable called 'df'
# Import pandas to use dataframe objects
import pandas as pd

# Import plot.ly viz libraries
import plotly.plotly as py
import plotly.graph_objs as go

# Pivot data. Details on how to do this here https://community.periscopedata.com/t/q5gk76/pivoting-and-melting-dataframes
df=pd.pivot_table(df,index='week',columns='source',values='count')
df=df.reset_index()

# Create traces
# Refer to https://plot.ly/python/line-charts/ for more options

admob_trace = dict(
    x = df.week,
    y = df['admob'],
    mode = 'lines',
    type = 'scatter',
    name = 'admob',
    line = dict(shape = 'linear', color = 'rgb(205, 12, 24)', width= 4, dash = 'dash'),
    connectgaps = True
)
leadbolt_trace = go.Scatter(
    x = df['week'],
    y = df['leadbolt'],
    mode = 'lines+markers',
    name = 'leadbolt',
    line = dict(shape = 'linear', color = 'rgb(10, 12, 240)', dash = 'dash'),
    marker = dict(symbol = "star-diamond", color = 'rgb(17, 157, 255)',size = 12),
    connectgaps = True
)
organic_trace = go.Scatter(
    x = df.week,
    y = df['organic'],
    mode = 'lines',
    name = 'organic',
    line = dict(shape = 'linear', color = 'rgb(10, 120, 24)', dash = 'dot'),
    connectgaps = True
)
tapjoy_trace = go.Scatter(
    x = df['week'],
    y = df['tapjoy'],
    mode = 'lines',
    name = 'tapjoy',
    line = dict(shape = 'linear', color = 'rgb(100, 10, 100)', width = 2, dash = 'dot'),
    connectgaps = True
)

# Setting up the layout settings in the "layout" argument
layout =  dict(
    xaxis = dict(title = 'Week'),
    yaxis = dict(title = 'Source'),
    margin = dict(
        l=70,
        r=10,
        b=50,
        t=10
    )
)
data = [admob_trace, leadbolt_trace, organic_trace, tapjoy_trace]

fig =  go.Figure(data = data, layout=layout)

# Use Periscope to visualize a dataframe, text, or an image by passing data to periscope.table(), periscope.text(), or periscope.image() respectively.
periscope.plotly(fig)