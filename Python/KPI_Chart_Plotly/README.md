# KPI Chart — Plot.ly

![kpi](/Python/KPI_Chart_Plotly/Images/kpi.png)

Contextualizing KPIs is a must. For instance, if a company has 500 users, how does that compare to the number of users last week? Using [Periscope Data's Python Integration](https://doc.periscopedata.com/article/r-and-python#content), we can create customized number overlays to cleanly present this information. To generate this visual, we require a SQL output with the following 2 columns:

1. ds_aggregation: the date or datetime. name should be `ds_hour`, `ds_day`, `ds_week`, `ds_month`, `ds_quarter`, or `ds_year`. if you are using [Periscope Data's aggregation filter](https://doc.periscopedata.com/article/aggregation-filter#article-title) to allow this parameter to by dynamic, you can name it `ds_[aggregation]`
2. y_value: the value to forecast. name it whatever makes sense, e.g. `y_signups`, `y$_revenue`, etc. add the dollar sign ($) to format in dollars.

**Python 3.6 Script**

	# PERISCOPE KPI CHART TEMPLATE
	# SQL output should have 2 columns:
	#    1) ds_aggregation: the date or datetime. name should be ds_hour, ds_day, ds_week, ds_month, ds_quarter, or ds_year. if you are using Periscope's aggregation filter, you can name it ds_[aggregation]

	#    2) y_value: the value to forecast. name it whatever makes sense, e.g. y_signups, y$_revenue, etc. add the dollar sign ($) to format in dollars.

	import pandas as pd
	import plotly.plotly as py
	import plotly.graph_objs as go
	import datetime
	import numpy as np

	# Generating dummy data if SQL output is not in the correct format
	community_post = ''
	dummy_df = pd.DataFrame()
	dummy_df['ds_day'] = pd.date_range(start='12/1/2018', end='1/1/2019')
	dummy_df['row_num'] = range(1, dummy_df.shape[0] + 1)
	dummy_df['multiplier'] = np.random.randint(10,50, dummy_df.shape[0])
	dummy_df['y$_revenue'] = dummy_df['row_num'] * dummy_df['multiplier']

	# gets the formatter for the column ($ or %)
	def get_formatter(column):
	  if '$' in column:
	    return '$'
	  elif '%' in column:
	    return '%'
	  else:
	    return None

	# returns the plotly formatter for the column
	def tickformat(column):
	  if column.startswith('y$'):
	    return '$.3s'
	  elif column.startswith('y%'):
	    return '.0%'
	  else:
	    return '.3s'

	# formats the column name
	def column_name(column):
	  return column.split('_', 1)[1].replace('_',' ').title()

	# identifies the aggregation level
	def aggregation(ds_col):
	  return ds_col.split('_', 1)[1].lower()

	# formats a percent value
	def percent(pct):
	  return str(int(round(pct*100))) + '%'

	# formats a number based on its formatter ($ or %)
	def format(num, formatter = None):
	  if formatter is None:
	    return abbrev(num)
	  elif formatter == '$':
	    return dollars(num)
	  elif formatter == '%':
	    return percent(num)

	# formats a dollar value
	def dollars(num):
	  num = float('{:.3g}'.format(float(num)))
	  magnitude = 0
	  while abs(num) >= 1000:
	    magnitude += 1
	    num /= 1000.0
	  return '${}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])

	# makes a large number human-readable, e.g. 100000 -> 100K
	def abbrev(num):
	  num = float('{:.3g}'.format(float(num)))
	  magnitude = 0
	  while abs(num) >= 1000:
	    magnitude += 1
	    num /= 1000.0
	  return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])

	# returns the css styling for text
	def style_text(text, **settings):
	  style = ';'.join([f'{key.replace("_","-")}:{settings[key]}' for key in settings])
	  return f'<span style="{style}">{text}</span>'

	def style_link(text, link, **settings):
	  style = ';'.join([f'{key.replace("_","-")}:{settings[key]}' for key in settings])
	  return f'<a href="{link}" style="{style}">{text}</a>'

	# displays text in the center of the plot
	def number_overlay(text, annotation_msg=None):
	  axis_setting = dict(range=[-1,1], showline=False, ticks='', showticklabels=False, showgrid=False, zeroline=False, fixedrange=True)
	  annotation = dict(x=0, y=0, ax=0, ay=0, text=text)
	  margin = dict(t=60)
	  if annotation_msg is not None:
	    annotations = [annotation, annotation_msg]
	  else:
	    annotations = [annotation]
	  layout = go.Layout(xaxis=axis_setting,yaxis=axis_setting,annotations=annotations,margin=margin,)
	  fig=go.Figure(data=[], layout=layout)
	  periscope.plotly(fig, config={'displayModeBar':False})

	# translates a hex code to RGB values
	def rgb_from_hex(hex):
	  h = hex.lstrip('#')
	  return tuple(((int(h[i:i+2], 16))) for i in (0, 2 ,4))

	# translates RGB values to hex code
	def rgb_to_hex(rgb):
	  return '#%02x%02x%02x' % rgb

	# calculates the gradient value between two colors, based on a scale
	def gradient(value, scale, colors):
	  min = scale[0]
	  max = scale[1]
	  if value < min:
	    value = min
	  elif value > max:
	    value = max
	  pct = 1.0 * (value - min) / (max - min)
	  min_color = rgb_from_hex(colors[0])
	  max_color = rgb_from_hex(colors[1])
	  rgb = tuple(((int(round(pct * (max_color[i] - min_color[i]) + min_color[i])))) for i in range(0,3))
	  return rgb_to_hex(rgb)

	# prints a message indicating there was no data
	def no_data():
	  msg = 'No data to display.'
	  number_overlay(style_text(msg, font_size="18px"))

	def plot(df, annotation=None):
	  df.columns = [c.lower() for c in df.columns]
	  y_col = [c for c in df.columns if c.startswith('y')][0]
	  ds_col = [c for c in df.columns if c.startswith('ds')][0]
	  df[y_col] = pd.to_numeric(df[y_col])
	  df[ds_col] = pd.to_datetime(df[ds_col])
	  agg = aggregation(ds_col)

	  df.sort_values(by=[ds_col], inplace=True)
	  pct_col = 'pct_change'
	  df[pct_col] = df[y_col].pct_change()
	  formatter = get_formatter(y_col)

	  current = df.tail(1)
	  current_val = current[y_col].iloc[0]
	  percentage_change = current[pct_col].iloc[0]
	  indicator = '▲' if percentage_change >= 0 else '▼'
	  kpi_change = indicator + ' ' + percent(percentage_change) + ' since last ' + agg
	  color = gradient(percentage_change, [-.25, .25], ['#ff0000', '#00be11'])

	  text = (
	    style_text(column_name(y_col), font_size = '24px') + '<br><br><br><br>' +
	    style_text(format(current_val, formatter), font_size='50px', font_weight='bold') +
	    '<br><br>' +
	    style_text(kpi_change, font_size='16px', color=color)
	  )

	  number_overlay(text, annotation)

	try:
	  plot(df)
	except Exception as e:
	    print(e)
	    annotation = {
	    'x': 0.5,
	    'y': 0.5,
	    'ax': 0,
	    'ay': 0,
	    'xref': 'paper',
	    'yref': 'paper',
	    'text': style_link('DUMMY<br><br><br><br>DATA<br><br><br><br>EXAMPLE', community_post, font_size='60px', font_weight='bold', color='rgba(0, 0, 0, .25)'),
	    'showarrow': False,
	    'textangle': -25
	  }
	    plot(dummy_df, annotation=annotation)