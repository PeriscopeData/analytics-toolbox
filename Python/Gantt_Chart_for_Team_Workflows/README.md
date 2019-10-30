# Gantt Chart for Team Workflows

![Gantt_Chart1](/Python/Gantt_Chart_for_Team_Workflows/Images/Gantt_Chart1.png)

Gantt charts are a great way to show which projects and tasks different teams are working on at a given time. This chart type is heavily used by Project Managers, Task Managers, and anyone else managing multiple workflows.

Using Periscope Data's [Python Integration](https://doc.periscopedata.com/article/r-and-python#content), we have built a function that allows users to create Gantt charts, with the flexibility to alter a few parameters:

    gantt_chart(df, show_today=True, groupby='team')

* df: a dataframe object containing the following 4 columns: project, team, start_date, and end_date
* show_today: boolean value to display a vertical line on the Gantt chart for the current date. Default value is set to True
* groupby: either 'team' to group the y axis by the team, or 'project' to group by y axis by project. This value defaults to 'project' if not explicitly defined. The above chart uses the default 'project' groupby. Updating this to 'team' generates the chart below. 
 
![Gantt_Chart2](/Python/Gantt_Chart_for_Team_Workflows/Images/Gantt_Chart2.png)

Below is the Python snippet used to create the function for the Gantt chart above.

    # SQL output is imported as a pandas dataframe variable called "df"
    # primary reference: https://sukhbinder.wordpress.com/2016/05/10/quick-gantt-chart-with-matplotlib/
    # reference http://www.clowersresearch.com/main/gantt-charts-in-matplotlib/

    #######################################################################
    ### LIBRARIES ###
    #######################################################################

    import pandas as pd
    import datetime as dt
    import matplotlib.dates as dates
    import matplotlib.pyplot as plt
    from matplotlib.dates import MONTHLY, DateFormatter, rrulewrapper, RRuleLocator
    from collections import OrderedDict
    import numpy as np
    import datetime as dt

    #######################################################################
    ### HELPER FUNCTIONS ###
    #######################################################################

    # Function: prepare dataframe for gantt visualization
    # Input: dataframe with a column for project, team, start_date, and end_date
    # Output: matplot ax.text object and a dataframe of

    def df_gantt(df):

        df['project']=df['project'].astype('category')
        df['team']=df['team'].astype('category')
        df['end_date2']=dates.date2num(df['end_date'])
        df['start_date2']=dates.date2num(df['start_date'])
        df['duration']=df['end_date2']-df['start_date2']

        #assign colors for each series
        colors=['rebeccapurple','mediumslateblue','mediumorchid','m','plum']
        allgrps=df['team'].drop_duplicates().sort_values().reset_index(drop=True)
        se=pd.DataFrame(colors[0:len(allgrps)])
        se.columns=['col']
        colormatrix=pd.concat([allgrps,se],axis=1)
        df = df.merge(colormatrix,on='team',how='inner').sort_values('project').reset_index(drop=True)
        return df, allgrps

    # Function: Return distinct projects/phases
    # Input: dataframe with a column indicating project names
    # Output: dataframe of all distinct phases

    def all_phases(df):
      phases=df['project'].drop_duplicates().values.tolist()
      return phases

    # Function: Return x tick marks locations
    # Input: dataframe with columns for 'start_date' and 'end_date'
    # Output: list of x tick marks

    def get_x_dates(df):
      mindate=df['start_date'].min().replace(day=1)
      maxdate=df['end_date'].max().replace(day=1).replace(month=df['end_date'].max().month+1)
      x_dates=[]
      counter=mindate
      while (counter<maxdate):
        x_dates.append(counter)
        counter=counter.replace(month=counter.month+1)

      return x_dates

    ##########################################################################
    ### MAIN PLOT
    ##########################################################################

    def gantt_chart(df, show_today = True,groupby = 'project'):

      df, allgrps=df_gantt(df)
      phases = all_phases(df)

      fig, ax = plt.subplots()

      if (groupby=='project'):
        df=df.sort_values(by=['project','team']).reset_index(drop=True)
      else:
        df=df.sort_values(by=['team','project']).reset_index(drop=True)

      #initialize variables
      j=''
      change=0
      ylocs=[]
      shade_end=0

      #plot chart
      for i in range(len(df['start_date2'])):
        ax.barh(0.5*i+0.5, df['duration'][i], left=df['start_date2'][i],height=0.3, align='center', color=df['col'][i], alpha = 1.0, label=df['team'][i])
        if(j!=df[groupby][i]):
          change=change+1
          if (change%2==1):
            shade_start=i*1.0/2.0+0.25
            ylocs.append((shade_start+shade_end)/2.0)
          else:
            shade_end=i*1.0/2.0+0.25
            plt.axhspan(shade_start, shade_end, facecolor='0.2', alpha=0.1)
            ylocs.append((shade_start+shade_end)/2.0)
        j=df[groupby][i]
      if (shade_end<shade_start):
        shade_end=len(df['start_date2'])*1.0/2.0+0.25
        plt.axhspan(shade_start, shade_end, facecolor='0.2', alpha=0.1)
        ylocs.append((shade_start+shade_end)/2.0)
      else:
        ylocs.append((len(df['start_date2'])*1.0/2.0+0.25+shade_end)/2.0)
      ylocs.pop(0)

      #format x axis
      rule = rrulewrapper(MONTHLY, interval=1)
      ax.xaxis.set_major_locator(RRuleLocator(rule))
      ax.set_xticks(get_x_dates(df))
      print(rule)
      ax.xaxis.set_major_formatter(DateFormatter("%b '%y"))
      labelsx = ax.get_xticklabels()
      ax.xaxis.grid(which="major", color='k', linestyle='-.', linewidth=0.2)
      ax.xaxis_date()
      plt.tick_params(
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        top='off',      # ticks along the bottom edge are off
        bottom='off',
        rotation=0)         # ticks along the top edge are off

     #format y axis
     ax.invert_yaxis()
      ax.set_ylim(top=0.25, bottom=0.5*len(df['start_date2'])+0.25)
      if (groupby=='project'):
        ax.set_yticks(ylocs)
        ax.set_yticklabels(phases)
      else:
        ax.set_yticks(np.arange(len(df))/2.0+0.5)
        ax.set_yticklabels(df['project'])
     plt.tick_params(
        axis='y',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        left='off',      # ticks along the bottom edge are off
        right='off')        # ticks along the top edge are off

      #format legend
      handles, labels = plt.gca().get_legend_handles_labels()
      by_label = OrderedDict(zip(labels, handles))
      plt.legend(by_label.values(), by_label.keys())

      #format border
      ax.spines['bottom'].set_linewidth(0.2)
      ax.spines['left'].set_linewidth(0.2)
      ax.spines['top'].set_linewidth(0.2)
      ax.spines['right'].set_linewidth(0.2)

      #plot a line showing current date
      if show_today == True:
        plt.axvline(x=dt.date.today(),color='gray')

      return fig

    # Use Periscope to visualize a dataframe or an image by passing data to periscope.output()
    periscope.output(gantt_chart(df, show_today=True))

