import pandas as pd
from fbprophet import Prophet
import plotly.plotly as py
import plotly.graph_objs as go
import datetime
from scipy.stats import boxcox
from scipy.special import inv_boxcox
from datetime import date

# Dummy Data
import numpy as np
dummy_df = pd.DataFrame()
dummy_df['ds_day'] = pd.date_range(start='1/1/2018', end='1/1/2019')
dummy_df['row_num'] = range(1, dummy_df.shape[0] + 1)
dummy_df['multiplier'] = np.random.randint(10,50, dummy_df.shape[0])
dummy_df['y$_revenue'] = dummy_df['row_num'] * dummy_df['multiplier']
df = dummy_df[['ds_day', 'y$_revenue']]

# Helper function that formats values as $ or %
def format(column):
  if column.startswith('y$'):
    return '$.3s'
  elif column.startswith('y%'):
    return '.0%'
  else:
    return '.3s'

# Helper Function that removes underscores
def column_name(column):
  return column.split('_', 1)[1].replace('_',' ').title()

# Helper function that determines the intended aggregation based on column name
def aggregation(ds_col):
  return ds_col.split('_', 1)[1].lower()

# Check for in progress data, will exclude later
def in_progress(dt, agg):
  now = datetime.datetime.now()
  if agg == 'hour':
    return (now.year == dt.year and now.month == dt.month and now.day == dt.day and now.hour == dt.hour)
  elif agg == 'day':
    return (now.year == dt.year and now.month == dt.month and now.day == dt.day)
  elif agg == 'week':
    return (now.year == dt.year and now.isocalendar()[1] == dt.isocalendar()[1])
  elif agg == 'month':
    return (now.year == dt.year and now.month == dt.month)
  elif agg == 'quarter':
    return (now.year == dt.year and int(now.month / 4) == int(dt.month / 4))
  elif agg == 'year':
    return (now.year == dt.year)

# Lowercase the column names
df.columns = [c.lower() for c in df.columns]
# Determine which is Y axis
y_col = [c for c in df.columns if c.startswith('y')][0]
# Determine which is X axis
ds_col = [c for c in df.columns if c.startswith('ds')][0]
# Determine what the aggregation is
agg = aggregation(ds_col)

# Data cleanup and in-progress analysis
df['y'] = pd.to_numeric(df[y_col])
df['y'], lam = boxcox(df['y'])
df['ds'] = pd.to_datetime(df[ds_col])
df['in_progress'] = df.apply(lambda x: in_progress(x['ds'], agg), axis=1)

# Instantiate Prophet and fit the model
m = Prophet()
m.fit(df.query('in_progress == False')[['ds','y']])

# Create the predictions dataframe that includes future dates
if agg == 'hour':
  future = m.make_future_dataframe(periods=72, freq='H')
elif agg == 'day':
    future = m.make_future_dataframe(periods=30)
elif agg == 'week':
  future = m.make_future_dataframe(periods=183)
  future['day_diff'] = future.apply(lambda x: (df['ds'].max() - x['ds']).days, axis=1)
  future = future[future['day_diff'] % 7 == 0]
elif agg == 'month':
  future = m.make_future_dataframe(periods=365)
  future = future[future['ds'].dt.day == 1]
elif agg == 'quarter':
  future = m.make_future_dataframe(periods=365)
  future = future[(future['ds'].dt.month % 3 == 1) & (future['ds'].dt.day == 1)]
elif agg == 'year':
  future = m.make_future_dataframe(periods=731)
  future = future[(future['ds'].dt.month == 1) & (future['ds'].dt.day == 1)]

# Predict the future
forecast = m.predict(future)
forecast[['yhat','yhat_upper','yhat_lower']] = forecast[['yhat','yhat_upper','yhat_lower']].apply(lambda x: inv_boxcox(x, lam))

# Create the plotly figure
yhat = go.Scatter(
  x = forecast['ds'],
  y = forecast['yhat'],
  mode = 'lines',
  marker = {
    'color': '#3bbed7'
  },
  line = {
    'width': 3
  },
  name = 'Forecast',
)

yhat_lower = go.Scatter(
  x = forecast['ds'],
  y = forecast['yhat_lower'],
  marker = {
    'color': 'rgba(0,0,0,0)'
  },
  showlegend = False,
  hoverinfo = 'none',
)

yhat_upper = go.Scatter(
  x = forecast['ds'],
  y = forecast['yhat_upper'],
  fill='tonexty',
  fillcolor = 'rgba(231, 234, 241,.75)',
  name = 'Confidence',
  hoverinfo = 'none',
  mode = 'none'
)

actual = go.Scatter(
  x = df['ds'],
  y = df[y_col],
  mode = 'markers',
  marker = {
    'color': '#fffaef',
    'size': 4,
    'line': {
      'color': '#000000',
      'width': .75
    }
  },
  name = 'Actual'
)

layout = go.Layout(
  yaxis = {
    'title': column_name(y_col),
    'tickformat': format(y_col),
    'hoverformat': format(y_col)
  },
  hovermode = 'x',
  xaxis = {
    'title': agg.title()
  },
  margin = {
    't': 20,
    'b': 50,
    'l': 60,
    'r': 10
  },
  legend = {
    'bgcolor': 'rgba(0,0,0,0)'
  }
)
data = [yhat_lower, yhat_upper, yhat, actual]

fig = dict(data = data, layout = layout)
periscope.plotly(fig)