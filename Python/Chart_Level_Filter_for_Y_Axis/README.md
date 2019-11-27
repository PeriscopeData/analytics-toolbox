# Use a Chart-Level filter for your Y Axia — Plot.ly

![chart_filter](Python/Chart_Level_Filter_for_Y_Axis/Images/chart_filter.png)

Want to create a chart-level filter, allowing you to change your Y axis? Say hello to your new favorite library plot.ly! [Periscope's Python and R integration](https://doc.periscopedata.com/article/r-and-python#content) allows you to use Plot.ly (as well as a host of other libraries), some of which we will leverage in this example.

Here, in your SQL output, be sure that your fields for the X axis are preceded with an 'x' character, and all your fields for the Y axis options are preceded by the 'y' character. If the y axis should be formatted as a dollar or percent, ensure the prefix is  'y$' or 'y%'

**Python 3.6 Code**

	# SQL output should have these columns:
	#    x value prefixed with 'x'
	#    y value(s) prefixed with 'y' -- if $ or %, prefix with 'y$' or 'y%'
	#    series value(s) prefixed with 's'

	import pandas as pd
	import plotly.plotly as py
	import plotly.graph_objs as go
	import datetime
	from datetime import timedelta
	import numpy as np

	community_post = ''
	dummy_df = pd.DataFrame()
	dummy_df['x_date'] = pd.date_range(start='1/1/2018', end='1/1/2019')
	dummy_df['row_num'] = range(1, dummy_df.shape[0] + 1)
	dummy_df['multiplier'] = np.random.randint(10,50, dummy_df.shape[0])
	dummy_df['y$_revenue'] = dummy_df['row_num'] * dummy_df['multiplier']
	dummy_df['y_purchases'] = np.random.randint(100, 1000, dummy_df.shape[0])

	# Helper Function that removes underscores
	def column_name(column):
	  return column.split('_', 1)[1].replace('_',' ').title()

	# Helper function that formats values as $ or %
	def format(column):
	  if column.startswith('Y$'):
	    return '$.3s'
	  elif column.startswith('Y%'):
	    return '.0%'
	  else:
	    return '.3s'

	# Helper function that returns unique column values
	def unique_vals(df, column):
	  return df.groupby(column).size().reset_index()[column]

	# Get the x, y, and series columns
	def get_columns(df):
	  x_column = [c for c in df.columns if c.startswith('X')][0]
	  y_columns = [c for c in df.columns if c.startswith('Y')]
	  series_columns = [c for c in df.columns if c.startswith('S_')]
	  unique_series = unique_vals(df, series_columns) if len(series_columns) > 0 else None
	  return x_column, y_columns, series_columns, unique_series

	def button(y_col, y_columns, unique_series = None):
	  return {
	    'label': column_name(y_col),
	    'method': 'update',
	    'args': [
	      {
	        'visible': [c==y_col for c in y_columns for i in range(0, 1 if unique_series is None else len(unique_series))]
	      },
	      {
	        'yaxis': {
	          'tickformat': format(y_col),
	          'hoverformat': format(y_col)
	        }
	      }
	    ]
	  }

	def style_link(text, link, **settings):
	  style = ';'.join([f'{key.replace("_","-")}:{settings[key]}' for key in settings])
	  return f'<a href="{link}" style="{style}">{text}</a>'

	def plot(df, annotation=None):
	  # Force consistent casing for columns
	  df.columns = [c.upper() for c in df.columns]
	  x_column, y_columns, series_columns, unique_series = get_columns(df)
	  has_series = unique_series is not None
	  showlegend = has_series

	  data = []
	  buttons = []

	  for idx, y_col in enumerate(y_columns):
	    buttons.append(button(y_col, y_columns, unique_series=unique_series))

	    # if no series -- create the traces for each y value and only display the first one
	    if not has_series:
	      trace = go.Scatter(
	        x=df[x_column],
	        y=df[y_col],
	        name=column_name(y_col),
	        visible=(idx==0)
	      )
	      data.append(trace)

	    # if series -- create the traces for each series for each y value, still only displaying series for the first y value
	    else:
	      for idx_series, series in unique_series.iterrows():
	        query = ' & '.join(f'{col} == "{series[{col}].iloc[0]}"' for col in series_columns)
	        df_series = df.query(query)
	        trace = go.Scatter(
	          x=df_series[x_column],
	          y=df_series[y_col],
	          name=f'{", ".join([series[{col}].iloc[0] for col in series_columns])}',
	          visible=(idx == 0)
	        )
	        data.append(trace)

	  updatemenus = list([
	    {
	      'active': 0,
	      'buttons': buttons,
	      'x': -.1,
	      'y': 1.25,
	      'xanchor': 'left',
	      'yanchor': 'top',
	      'bgcolor': '#FFFFFF'
	    }
	  ])

	  first_y = y_columns[0]
	  xaxis = {'title': column_name(x_column)}

	  # If x value is a date, then add the quick-filter options for dates
	  if isinstance(df[x_column].iloc[0], datetime.date):
	    duration = (df[x_column].max() - df[x_column].min()).days
	    month_buttons = [dict(count=x, label=str(x)+'m', step='month', stepmode='backward') for x in [1,3,6] if x * 30 <= duration]

	    xaxis['rangeselector'] = {
	      'buttons': list(month_buttons + [{'step': 'all'}]) if len(month_buttons) > 0 else None,
	      'xanchor': 'right',
	      'yanchor': 'top',
	      'x': 1,
	      'y': 1.2
	    }

	  layout = {
	    'showlegend': showlegend,
	    'yaxis': {
	      'tickformat': format(first_y),
	      'hoverformat': format(first_y)
	    },
	    'xaxis': xaxis,
	    'margin': {
	      't': 20,
	      'b': 50,
	      'l': 60,
	      'r': 10
	    }
	  }

	  if annotation is not None:
	    layout['annotations'] = [annotation]
	  if len(y_columns) > 1:
	    layout['updatemenus'] = updatemenus
	  else:
	    layout['yaxis']['title'] = column_name(y_columns[0])

	  fig = dict(data=data, layout=layout)

	  # Use Periscope to visualize a dataframe by passing the data to periscope.output()
	  periscope.plotly(fig)

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