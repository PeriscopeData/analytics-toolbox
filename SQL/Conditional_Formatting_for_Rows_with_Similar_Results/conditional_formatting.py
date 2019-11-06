# SQL output is imported as a pandas dataframe variable called "df"

import pandas as pd

import matplotlib.pyplot as plt

from pandas.tools.plotting import table


#Purpose:
#Inputs:
##dataframe (df) containing the table of data to be visualized
##column (col) to be conditionally formatted
##optional parameters to specify the hex code of the desired coloring (color1 and color2)
#Output: a matplotlib plot, plt


def color_block_formatting(df,col,color1="#e5c2fe",color2="#c2fefa"):
 plt.figure(figsize=(10,15))
 ax = plt.subplot(111, frame_on=False)
 ax.xaxis.set_visible(False)
 ax.yaxis.set_visible(False)


 the_table=table(ax, df, rowLabels=['']*df.shape[0], bbox=[-0.1,0.1,1.2,1])
 ax.axis('tight')


 change=0
 val=df[col][0]
 for i in range(df.shape[0]):
   if val!=df[col][i]:
     change+=1
   if (change%2==0):
     the_table._cells[(i+1, 0)].set_facecolor(color1)
   else:
     the_table._cells[(i+1, 0)].set_facecolor(color2)
   val=df[col][i]


 return plt


# Use Periscope to visualize a dataframe or an image by passing data to periscope.output()
periscope.output(color_block_formatting(df,col="user_id"))