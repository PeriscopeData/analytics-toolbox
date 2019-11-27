import plotly
import plotly.graph_objs as go
import numpy as np

import pandas as pd

first_name = df.first_name.values
last_name = df.last_name.values
total_spent = df.total_spent.values
gameplays = df.gameplays.values

trace = go.Table(columnwidth = [.3,.3,.3,.3],
    header=dict(values=['First Name', 'Last Name', 'Total Spent', 'Gameplays'],
                fill = dict(color='#8849a5'),
                font = dict(color = 'white', size = 12),
                align = ['left'] ),
    cells=dict(values=[first_name, last_name, total_spent, gameplays],
               fill = dict(color=[#unique color for the first column
                                                ['#b4a8ce' if val >=750 else '#f5f6f7' for val in gameplays] ]),
               align = ['left'] * 5))

data = [trace]


periscope.plotly(data)