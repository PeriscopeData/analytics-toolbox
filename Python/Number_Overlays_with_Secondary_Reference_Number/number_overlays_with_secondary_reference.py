import pandas as pd
import matplotlib.pyplot as plt

fig = plt.figure()
plt.axis('off')

plt.gcf().set_size_inches(8, 2)
plt.xticks([])
plt.yticks([])

if(df.iat[0,1][0]=='-'):
  col='red'
  dir="\u25bc"
  val=df.iat[0,1][1:]
else:
  col='green'
  dir='\u25b2'
  val=df.iat[0,1]

plt.text(.5, .95, 'New Users', fontsize=25, color='black', ha='center')
plt.text(.5, .75, 'This Week', fontsize=12, color='black', ha='center')
plt.text(.5, .25, str(df.iat[0,0]), fontsize=50, color='black', ha='center')
plt.text(.5, 0, dir + ' ' + val +' from prior week', fontsize=15, color=col, ha='center')

periscope.image(plt)