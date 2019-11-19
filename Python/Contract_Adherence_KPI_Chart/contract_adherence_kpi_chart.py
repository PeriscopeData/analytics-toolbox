import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

##########################################################################
### HELPER UTILITY FUNCTIONS
##########################################################################

# Function: Takes an integer/float and returns a string with the number rounded to the nearest thousand place and appends the appropriate thousand's place symbol
# Input: float/intger
# Output: Formatted string
def prettify_num(num):
  pretty_num = ''
  if abs(num) < 10**3:
    pretty_num = str(num)
  elif abs(num) < 10**6:
    pretty_num = str(round(1.0*num/10**3,1)) + 'K'
  elif abs(num) < 10**9:
    pretty_num = str(round(1.0*num/10**6,1)) + 'M'
  else:
    pretty_num = str(round(1.0*num/10**9,1)) + 'B'
  return pretty_num

# Function: Divide the first number by the second and returns a string with the appropiate formatting
# Input: df with at least two columns
# Output: Formatted string of the percent taking the first number as the denomiator and the number in the second column as the numerator
def pretty_percent(num, den):
  if df.iloc[0,1] > 0:
    percentage = str(round(100.0 * num / den,1)) + '%'
  elif df.iloc[0,1] == 0:
    percentage = '0%'
  else:
    percentage = 'NA'
  return percentage

# Function: Color code the colors based on how the first column compares to the second column
# Input: df with at least two columns
# Output: a color stirng or hex code
def color_me_timbers(df):
  if df.size == 0 or df.iloc[0,1] == 0:
    color = 'gray'
  elif df.iloc[0,0] == -1:
    color = 'black'
  elif df.iloc[0,1] <= df.iloc[0,0]:
        color = '#0c577c'
#   elif df.iloc[0,1] < 1.2 * df.iloc[0,0]:
#     color = '#8b0000'
  elif df.iloc[0,1] > df.iloc[0,0]:
    color = '#8b0000' # red #ad0505 #e00000
  else:
    color = '#0c577c'
  return color

# Function: Parse the df and returns the numbers contextualized
# Input: df with at least two columns
# Output: an array of three numeric or null values: the percent(0-1), the current number, and the contract number
def parse(df):
  if df.size == 0:
    return [None, None]
  elif df.iloc[0,0] == -1:
    current = df.iloc[0,1]
    return [current, np.inf]
  else:
    current = df.iloc[0,1]
    contract = df.iloc[0,0]
    return [current, contract]

# Function: Parse the df and returns the prettified numbers to be sent to the matplot plot
# Input: df with at least two columns
# Output: an array of three prettified strings: the percent, the current number, and the contract number
def pretty_parse(df):
  [current, contract] = parse(df)
  if df.size == 0:
    return ['', '', 'NA']
  elif contract == np.inf:
    current = str(prettify_num(current))
    return [current, '$\infty$', '$\infty$']
  else:
    return [str(prettify_num(current)),
            str(prettify_num(contract)),
           pretty_percent(current, contract)]

##########################################################################
### HELPER PLOT FUNCTIONS
##########################################################################

# Function: create a centered text object
# Input: the axes object to append to and optionally (text, color, y_position, font_size)
# Output: matplot ax.text object
def kpi_text(ax, text = '', text_color = 'black', y_position = 0, font_size = 10):
    return ax.text(x = 0.5,
                   y = y_position,
                   s = text,
                   color = text_color,
                   family = 'sans-serif',
                   fontsize = font_size,
                   fontweight = 500,
                   horizontalalignment = 'center',
                   verticalalignment = 'center')

# Function: Find the center location of the reamining bar
# Input: Tuple with the Numerator and Denomiator
# Output: x location of the bar remaining as a float
def bar_text_locator((num, den)):
    location = 0
    if df.size == 0:
      location = 0.5
    elif den == - 1:
      location = 0.5
    elif den <= num:
        location = 0.5
    else:
        location = (1 + 1.0 * num / den) / 2
    return location

# Function: Create the bar text overlay string
# Input: numerator and denonomicator
# Output: prettified string
def bar_text_overlay(num, den):
  text = ''
  if df.size == 0:
    text = ''
  elif df.iloc[0,0] == -1:
    text = ''
  else:
    text = prettify_num(den - num)
  return text


# return the width of the left rectangle
# if null or infinite then left = 0 (all gray)
def left_bar_length(df):
  percent_completed = 0
  if df.size == 0:
    percent_completed = 0
  elif df.iloc[0,1] == -1:
    percent_completed = 0
  else:
    percent_completed = 1.0 * df.iloc[0,1] / df.iloc[0,0]
  return percent_completed

##########################################################################
### MAIN PLOT
##########################################################################

def kpi_chart(df, titletext = 'KPI'):

  # Parse data
  [current, contract] = parse(df)
  percent = 1.0 * current/contract if df.size != 0 else None
  [pcurrent, pcontract, ppercent] = pretty_parse(df)

  # Set up figure canvas
  fig, ax = plt.subplots(figsize = (5,5))
  fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
  ax.axis('off')

  #Colors
  mediumgray = '#999292'
  lightgray = '#c4c4c4'

  # Primary Texts (Title and Percents)
  title = kpi_text(ax, text = titletext, text_color = 'lightgray', font_size = 50, y_position = 0.85)
  percent = kpi_text(ax, text = ppercent, text_color = color_me_timbers(df), font_size = 90 if contract != np.inf else 130, y_position = 0.55)

  #Secondary Texts

  if df.size > 0:

    # Formatting variables
    x_start = 0
    y_start = 0.21
    bar_width = 1
    bar_height = 0.15 #0.165

    percent_completed = left_bar_length(df)
    bar_width_new = bar_width * (1 - percent_completed)
    x_start_new = x_start + (bar_width * percent_completed)
    bar_text_size = 35

    completedbox = ax.add_patch(
      patches.Rectangle(
          (x_start, y_start),   # (x,y)
          bar_width,          # width
          bar_height,          # height
          color = color_me_timbers(df)
      )
     )

    graybox = ax.add_patch(
      patches.Rectangle(
          (x_start_new, y_start),   # (x,y)
          bar_width_new,          # width
          bar_height,          # height
          color = mediumgray if contract != np.inf else 'black'
      )
  )

    graybox_width = graybox.get_extents().width

    bartext = ax.text(x = bar_text_locator((current, contract)),
                     y = 0.28, #285
                     s = bar_text_overlay(current, contract),
                     color = '#ffffff',
                     family = 'sans-serif',
                     fontsize = bar_text_size,
                     fontweight = 500,
                     horizontalalignment = 'center',
                     verticalalignment = 'center')


    bartext_width = bartext.get_window_extent(renderer=fig.canvas.get_renderer()).width

    if current < contract:
      if bartext_width > graybox_width:
        bartext.set_ha('right')
        bartext.set_x(0.99)


    ax.text(x = 0,
              y = 0.13,
              s = pcurrent,
              color = color_me_timbers(df),
              family = 'sans-serif',
              fontsize = bar_text_size - 5,
              fontweight = 250,
              horizontalalignment = 'left',
              verticalalignment = 'center')

    ax.text(x = 1,
              y = 0.13,
              s = pcontract,
              color = mediumgray if contract != np.inf else 'black',
              family = 'sans-serif',
              fontweight = 250,
              fontsize = bar_text_size - 5,
              horizontalalignment = 'right',
              verticalalignment = 'center')

    ax.text(x = 0,
              y = 0.06,
              s = 'Current',
              color = lightgray,
              family = 'sans-serif',
              fontsize = 15,
              horizontalalignment = 'left',
              verticalalignment = 'center')
    ax.text(x = 1,
              y = 0.06,
              s = 'Contract',
              color = lightgray,
              family = 'sans-serif',
              fontsize = 15,
              horizontalalignment = 'right',
              verticalalignment = 'center')

  return plt

periscope.image(kpi_chart(df, titletext = 'Feature 4'))