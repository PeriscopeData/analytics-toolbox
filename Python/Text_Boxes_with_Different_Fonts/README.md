# Text Boxes with Different Fonts

Periscope has a feature called Text on Dashboards that allow users to add text boxes as banners, announcements, and descriptions of charts! However, they currently only support one font. 

With the R and Python integration, users can use Plotly to replicate the Text on Dashboard feature but change the font! 

By using this Python snippet, users can add the custom text, color, position and font to get something like the following: 

![font_format](/Python/Text_Boxes_with_Different_Fonts/Images/font_format.png)

**Step 1:** Create a New Chart

**Step 2:** Make the chart name blank

**Step 3:** Add "select 0" or any other valid sql code in the SQL editor

**Step 4:** Add this snippet to your Python editor and edit the text, position (x and y), font family, size, and color. 

import plotly.graph_objs as go

	layout = go.Layout(
	      title=dict(
	      text= 'Welcome to my Dashboard!',
	      y = .3,
	      x = .5
	    ),
	    font=dict(
	        family='Cursive',
	        size=48,
	        color='#7A33FF'
	    ),
	    xaxis=dict(
	        showgrid=False,
	        ticks='',
	        showticklabels=False
	    ),
	    yaxis=dict(
	        showgrid=False,
	        zeroline=False,
	        showticklabels=False
	    )
	)
	fig = go.Figure(layout=layout)
	periscope.plotly(fig)

**Note:** So far the fonts I've seen supported are: 

Cursive, Times New Roman, Courier New, PT Sans Narrow, Helvetica, Arial, Arial Bold, and Comic Sans.