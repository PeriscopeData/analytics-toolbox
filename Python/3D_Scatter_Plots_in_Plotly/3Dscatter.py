# SQL output is imported as a dataframe variable called 'df'
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go

# 3D scatter plot. Resource: https://plot.ly/python/3d-scatter-plots/

setosa = go.Scatter3d(
    x = df.where(df['ESTIMATED_TARGET'].astype(int) == 0)['SEPALLENGTHCM'],
    y = df.where(df['ESTIMATED_TARGET'].astype(int) == 0)['SEPALWIDTHCM'],
    z = df.where(df['ESTIMATED_TARGET'].astype(int) == 0)['PETALLENGTHCM'],
    mode ='markers',
    name = 'setosa',
    marker =dict(
      color = 'rgb(198, 151, 237)',
      size = 8,
      opacity = 0.9
    )
)

versicolor  = go.Scatter3d(
    x= df.where(df['ESTIMATED_TARGET'].astype(int) == 1)['SEPALLENGTHCM'],
    y= df.where(df['ESTIMATED_TARGET'].astype(int) == 1)['SEPALWIDTHCM'],
    z= df.where(df['ESTIMATED_TARGET'].astype(int) == 1)['PETALLENGTHCM'],
    mode='markers',
    name = 'versicolor',
    marker=dict(
        color='rgb(87, 104, 178)',
        size=8,
        symbol='circle',
        opacity=0.9
    )
)

virginica  = go.Scatter3d(
    x = df.where(df['ESTIMATED_TARGET'].astype(int) == 2)['SEPALLENGTHCM'],
    y = df.where(df['ESTIMATED_TARGET'].astype(int) == 2)['SEPALWIDTHCM'],
    z = df.where(df['ESTIMATED_TARGET'].astype(int) == 2)['PETALLENGTHCM'],
    mode = 'markers',
    name = 'virginica',
    marker = dict(
        color = 'rgb(136, 68, 226)',
        size = 8,
        symbol = 'circle',
        opacity = 0.9
    )
)

data = [setosa , versicolor , virginica ]
layout = go.Layout(
   scene = dict(xaxis = dict(title='Sepal Length(cm)'),
                yaxis = dict(title='Sepal Width(cm)'),
                zaxis = dict(title='Petal Length(cm)'),),
    margin=dict(
        l=10,
        r=10,
        b=10,
        t=10
    )
)
fig = go.Figure(data=data, layout=layout)

# Use Periscope to visualize a dataframe, text, or an image by passing data to periscope.table(), periscope.text(), or periscope.image() respectively.
periscope.plotly(fig)