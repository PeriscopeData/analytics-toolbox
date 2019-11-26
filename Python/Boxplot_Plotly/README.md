# Boxplot — Plot.ly

![boxplot](/Python/Boxplot_Plotly/Images/boxplot.png)

Boxplots are a widely recognized chart type and are excellent for quickly and succinctly visualizing distributions. The following Python script, leveraging the plot.ly library with Periscope's Python/R Integration, generates the image above and can quickly plug into your SQL output.

To see your data in the boxplot instead of dummy data, ensure that your SQL output is in 2 columns as outlined blow:

1. s_name: the value to group by. if you're grouping by **platform**, call it `s_platform`
2. y_name: the Y value for the box plot. if you're plotting **revenue**, call it `y_revenue` (optionally, apply dollar formatting by naming the columns `y$_name`)

**Python 3.6 Code**

	# PERISCOPE BOX PLOT TEMPLATE
	# SQL output should have 2 columns:
	#    1) s_<name>: the value to group by. if you're grouping by `platform`, call it s_platform
	#    2) y_<name>: the Y value for the box plot. if you're plotting `revenue`, call it y_revenue
	#      optionally apply dollar formatting by naming the columns y$_<name>

	import pandas as pd
	import plotly.plotly as py
	import plotly.graph_objs as go
	import datetime
	from datetime import timedelta
	import numpy as np

	# Dummy data to use in case SQL output is in the incorrect format
	community_post = ''
	dummy_df = pd.DataFrame()
	dummy_df['y_purchases'] = np.random.randint(1,50, 10000)
	dummy_df['s_platform'] = dummy_df.apply(lambda x: 'android' if x['y_purchases'] % 3 == 1 else 'iOs', axis=1)

	# HELPER FUNCTIONS
	def column_name(column):
	  return column.split('_', 1)[1].replace('_',' ').title()

	def format(column):
	  if column.startswith('Y$'):
	    return '$s'
	  elif column.startswith('Y%'):
	    return '.0%'
	  else:
	    return 's'

	def get_columns(df):
	  y_column = [c for c in df.columns if c.startswith('Y')][0]
	  series_columns = [c for c in df.columns if c.startswith('S')]
	  unique_series = unique_vals(df, series_columns) if len(series_columns) > 0 else None
	  return y_column, series_columns, unique_series

	def unique_vals(df, column):
	  return df.groupby(column).size().reset_index()[column]

	def style_link(text, link, **settings):
	  style = ';'.join([f'{key.replace("_","-")}:{settings[key]}' for key in settings])
	  return f'<a href="{link}" style="{style}">{text}</a>'

	# MAIN FUNCTION
	def plot(df, annotation=None):
	  df.columns = [c.upper() for c in df.columns]
	  y_column, series_columns, unique_series = get_columns(df)
	  has_series = unique_series is not None
	  # showlegend = has_series

	  traces = []
	  for idx, series in unique_series.iterrows():
	    query = ' & '.join(f'{col} == "{series[{col}].iloc[0]}"' for col in series_columns)
	    df_series = df.query(query)
	    traces.append(
	      go.Box(
	        y=df_series[y_column],
	        boxpoints = False,
	        name=f'{", ".join([series[{col}].iloc[0] for col in series_columns])}'
	      )
	    )

	  data = traces

	  layout = {
	    'margin': {
	      'l': 50,
	      'r': 0,
	      'b': 50,
	      't': 0
	    },
	    'yaxis': {
	      'title': column_name(y_column),
	      'tickformat': format(y_column),
	      'hoverformat': format(y_column)
	    },
	    'xaxis': {
	      'title': f'{", ".join([column_name(col) for col in series_columns])}'
	    },
	    'showlegend': False
	  }
	  if annotation is not None:
	    layout['annotations'] = [annotation]
	  fig = dict(data=data, layout=layout)
	  periscope.plotly(fig)

	try:
	  plot(df)

	# Plot dummy data in case the SQL Output is in the incorrect format
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