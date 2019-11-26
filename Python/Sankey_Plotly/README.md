# Sankey Diagrams — Plot.ly

![sankey](/Python/Sankey_Plotly/Images/sankey.png)

Sankey diagrams are a very easy-to-digest way to look at the flow of objects between different points. The below script takes a SQL output with these 3 columns:

1. unique_id: the unique identifier for that entity
2. stage_name: the name of the stage in the sankey
3. ls
sort: identifies the order in which the entity moved from stage to stage, e.g. a date column associated with each transition

**Python 3.6 Code**


	# PERISCOPE SANKEY TEMPLATE
	# SQL output should have 3 columns:
	#    1) unique_id: the unique identifier for that entity
	#    2) stage_name: the name of the stage in the sankey
	#    3) sort: identifies the order in which the entity moved from stage to stage, e.g. a date column associated with each transition
	import pandas as pd
	import numpy as np
	import plotly.plotly as py
	import random
	import string

	def dummy_stage(idx):
	  rand = random.randint(0, 2)
	  step = 'Step'
	  step += ' ' + str(int(idx / 1000) + 1)
	  step += list(string.ascii_uppercase)[rand]
	  return step

	community_post = ''
	dummy_df = pd.DataFrame()
	dummy_df['idx'] = pd.Series(range(0, 3000))
	dummy_df['unique_id'] = dummy_df.apply(lambda x: x['idx'] % 1000, axis=1)
	dummy_df['stage_name'] = dummy_df.apply(lambda x: dummy_stage(x['idx']), axis=1)
	dummy_df['sort'] = dummy_df.apply(lambda x: int(x['idx'] / 1000), axis=1)

	print(dummy_df)

	DEFAULT_PLOTLY_COLORS = [
	    '#1f77b4',  # muted blue
	    '#ff7f0e',  # safety orange
	    '#2ca02c',  # cooked asparagus green
	    '#d62728',  # brick red
	    '#9467bd',  # muted purple
	    '#e377c2',  # raspberry yogurt pink
	    '#7f7f7f',  # middle gray
	    '#bcbd22',  # curry yellow-green
	    '#17becf'   # blue-teal
	]

	def color(i):
	  return DEFAULT_PLOTLY_COLORS[i % len(DEFAULT_PLOTLY_COLORS)]

	def rgb_from_hex(hex):
	  h = hex.lstrip('#')
	  return ",".join(str((int(h[i:i+2], 16))) for i in (0, 2 ,4))

	# identifies any circular references in the data
	# e.g. some items go from stage A -> B, some go from B -> A. this breaks the diagram
	def is_circular(df_agg, row):
	  circular_reference = df_agg.query(f'prior_stage_index == {row["stage_index"]} & stage_index == {row["prior_stage_index"]}')
	  if circular_reference.size == 0:
	    return False
	  elif circular_reference['count'].iloc[0] > row['count']:
	    return True
	  else:
	    return False

	def style_link(text, link, **settings):
	  style = ';'.join([f'{key.replace("_","-")}:{settings[key]}' for key in settings])
	  return f'<a href="{link}" style="{style}">{text}</a>'

	def plot(df, annotation=None):
	  df.columns = [c.lower() for c in df.columns]

	  # get unique stages and assign indexes
	  stages = df.groupby(['stage_name']).size().reset_index()[['stage_name']]
	  stages['stage_index'] = stages.index
	  stages['color'] = stages.apply(lambda r: color(r['stage_index']), axis=1)

	  # identify the prior stage for each record
	  df['stage_index'] = df.apply(lambda r: stages.loc[stages['stage_name'] == r['stage_name']]['stage_index'].iloc[0], axis=1)
	  df['prior_stage_index'] = df.groupby('unique_id').stage_index.shift()

	  # only take records that have a prior stage (can't plot something on a sankey if it doesn't go anywhere)
	  df = df[np.isfinite(df['prior_stage_index'])]

	  # get prior stage name
	  df['prior_stage_name'] = df.apply(lambda r: stages.loc[stages['stage_index'] == r['prior_stage_index']]['stage_name'].iloc[0], axis=1)
	  df['prior_stage_index'] = df['prior_stage_index'].astype(int)

	  # aggregate counts
	  df_agg = df.groupby(['prior_stage_index', 'prior_stage_name', 'stage_index', 'stage_name']).size().reset_index(name='count')

	  # remove any circular references
	  df_agg['is_circular'] = df_agg.apply(lambda row: is_circular(df_agg, row), axis=1)
	  df_agg = df_agg.query('is_circular == False')

	  # identifies the end stages in the sankey
	  priors = df_agg['prior_stage_index']
	  ends = stages.query('stage_index not in @priors')

	  # apply colors to each flow
	  df_agg['color'] = df_agg.apply(lambda r: f'rgba({rgb_from_hex(color(r["prior_stage_index"]))},{.25 if r["stage_index"] in ends["stage_index"] else .25})', axis=1)

	  data=dict(
	    type='sankey',
	    node=dict(
	      label=stages['stage_name'],
	      pad = 30,
	      thickness = 5,
	      color=stages['color'],
	      line=dict(
	        width=0
	      )
	    ),
	    link=dict(
	      source=df_agg['prior_stage_index'].astype(int)
	      ,target=df_agg['stage_index']
	      ,value=df_agg['count']
	      ,color=df_agg['color']
	    )
	  )

	  layout =  dict(
	      font = dict(
	        size = 16
	      ),
	      hoverlabel = dict(
	          bgcolor = 'purple'
	      ),
	    margin=dict(
	                  t=20,
	                  b=50,
	                  l=10,
	                  r=10
	                )
	  )

	  if annotation is not None:
	    layout['annotations'] = [annotation]

	  fig = dict(data=[data], layout=layout)
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