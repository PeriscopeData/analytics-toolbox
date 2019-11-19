import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches
from matplotlib.collections import PatchCollection

# extract important variables from the data frame
def extract():
#   GET DATA FROM DATA FRAME
#   if df.size == 0:
#     return [0, 0, 0 , 0, 0]
#   else:
#     opps_created = df.iloc[0]['opps_created']
#     opps_accepted = df.iloc[0]['opps_accepted']
#     opps_trialed = df.iloc[0]['opps_trialed']
#     opps_won = df.iloc[0]['opps_won']

# EXAMPLE DATA
    opps_created = 150
    opps_accepted = 80
    opps_trialed = 50
    opps_won = 20
    return [opps_created, opps_accepted, opps_trialed, opps_won]


####################
# create text chart
####################
def kpi_text(ax, text = '', text_color = 'black', x_position = 0, y_position = 0.5, font_size = 13):
    return ax.text(x = x_position,
                   y = y_position,
                   s = text,
                   color = text_color,
                   family = 'sans-serif',
                   fontsize = font_size,
                   horizontalalignment = 'center',
                   verticalalignment = 'center')


# create the plot
def kpi_chart(df):

  # set up the figure
  fig, ax = plt.subplots(figsize = (5.5,5.5))

  fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
  ax.axis('off')

  # styling (colors and font sizes)
  mediumgray = '#999292'
  lightgray = '#c4c4c4'
  purples = plt.get_cmap('Purples_r')

  fontsize_text = 30
  offset_x = 0.1
  offset_y = 0.13

  # parse the data
  funnel_df = extract()
#     use the following if you are using the extract_df function to parse the desired values
#   funnel_df = extract(df)
  [opps_created, opps_accepted, opps_trialed, opps_won] = funnel_df

  # map the data
  def get_data_domain(data):
    return {'min': min(data), 'max': max(data)}

  def data_mapper(data = [None], outputsize = 0.5):
    #assumes zero-max domain normalization
    # 0.48 is the max radius with a bit of padding
    domain = get_data_domain(data)
    mapped_area =  [1.0 * d/domain['max'] * outputsize  for d in data]
    mapped_radius = [np.sqrt(d/np.pi) for d in mapped_area]
    return mapped_radius

  # mapping the data
  mapped_df = data_mapper(funnel_df)
  colors = ['aliceblue', 'paleturquoise', 'darkturquoise', 'lightseagreen']

  # the circles
  for i in range(len(mapped_df)):
      ax.add_patch(
        mpatches.Circle( (0.5 + offset_x, mapped_df[i] + offset_y),
                        mapped_df[i],
                        color = colors[i]))

  kpi_text(ax,
       text = funnel_df[-1],
       text_color = 'white',
       font_size = fontsize_text,
       x_position = 0.5 + offset_x,
       y_position = mapped_df[-1] + 0.01 + offset_y)


  for i in range(len(mapped_df) - 2, -1, -1):
      kpi_text(ax,
               text = funnel_df[i],
               text_color = 'teal',
               font_size = fontsize_text,
               x_position = 0.5 + offset_x,
               y_position = mapped_df[i + 1] + mapped_df[i] + 0.01 + + offset_y)

  cols = ['Created', 'Accepted', 'Trialed', 'Won']

  for i in range(len(cols) - 2, -1, -1):
      kpi_text(ax,
               text = cols[i],
               text_color = 'steelblue',
               font_size = fontsize_text/1.7,
               x_position = 0.5 + offset_x,
               y_position =  mapped_df[i] + mapped_df[i+1] - 0.05 + 0.01 + offset_y)
  kpi_text(ax,
       text = cols[-1],
       text_color = 'white',
       font_size = fontsize_text/1.7,
       x_position = 0.5 + offset_x,
       y_position = mapped_df[-1] - 0.05 + 0.01 + offset_y)


  return plt

periscope.image(kpi_chart())