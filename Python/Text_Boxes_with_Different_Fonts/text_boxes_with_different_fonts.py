import plotly.graph_objs as go

layout = go.Layout(
      title=dict(
      text= 'Welcome to my Dashboard!',
      y = .3,
      x = .5
    ),
    font=dict(
        family='Cursive',
        size=48,
        color='#7A33FF'
    ),
    xaxis=dict(
        showgrid=False,
        ticks='',
        showticklabels=False
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        showticklabels=False
    )
)
fig = go.Figure(layout=layout)
periscope.plotly(fig)