# SQL output is imported as a pandas dataframe variable called "df"
import pandas as pd
import matplotlib.pyplot as plt

# Function: funnel_chart, creates a funnel chart image from a dataframe of steps
# Inputs: (1) dataframe with 2 columns. The first is the "step", and the second is the "val" corresponding to each step. (2) Optional boolean parameter show_n (displays the n size of each step). (3) Optional paramater show_pct which allows the user to show each step of the funnel as a percent of the original n size ('of whole') or a percent or the previous step ('of last step')
# Output: matplotlib image representing a funnel chart
def funnel_chart(df, show_n=True,show_pct='NA'):
  #set up data frame
  df['val']=df['val'].astype(int)
  my_max=df['val'][0]
  df = df.sort_values('val',ascending=False).reset_index(drop=True)
  df['pct_of_whole']=round((df['val']/my_max)*100).astype(int)
  pct_change=[100]
  for j in range(1,len(df['val'])):
    pct_change.append(int(round(df['val'][j]/df['val'][j-1]*100)))
  df['pct_change']=pct_change
  df = df.sort_values('val').reset_index(drop=True)
  df['left']=(my_max-df['val'])/2
  df['col']=['indigo','purple','darkviolet','DarkOrchid','MediumOrchid','orchid','plum','thistle']

  #initialize plot
  fig, ax = plt.subplots()
  for i in range(len(df['step'])):
    ax.barh(0.5*i+0.5, df['val'][i], height=0.3, left=df['left'][i], align='center', color=df['col'][i],alpha = 1.0, label=df['step'][i])
    if(show_n==True):
      ax.annotate(' ' + df['step'][i] + ': ' + str(df['val'][i]),xy=(my_max,0.5*i+0.45),horizontalalignment='left')
    else:
      ax.annotate(' ' + df['step'][i],xy=(my_max,0.5*i+0.45),horizontalalignment='left')
    if(show_pct=='of whole'):
      ax.annotate(str(df['pct_of_whole'][i]) + '%' ,xy=(my_max/2,0.5*i+0.45),horizontalalignment='center',color='white')
    elif(show_pct=='of last step'):
      ax.annotate(str(df['pct_change'][i]) + '%' ,xy=(my_max/2,0.5*i+0.45),horizontalalignment='center',color='white')


  #remove border and align chart
  ax.axis('off')
  fig.subplots_adjust(right=0.8)

  return fig

# Use Periscope to visualize a dataframe or an image by passing data to periscope.output()
periscope.output(funnel_chart(df,show_n=True,show_pct='of last step'))