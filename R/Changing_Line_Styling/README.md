# Changing Line Styling — R Plot.ly in Periscope Data

![line_styling](/R/Changing_Line_Styling/Images/line_styling.png)

Wanted to alter the thickness of the lines in your series, add markers to your lines, and make them dashed or dotted? The [plot.ly library support](https://doc.periscopedata.com/article/plot-ly#article-title) on [Periscope's Python/R integration](https://doc.periscopedata.com/article/r-and-python#article-title) allows you to tailor these parameters to your heart's desire!

For reference, here are the first few rows of our SQL output. This is data from a hypothetical gaming company

![rawdata](/R/Changing_Line_Styling/Images/rawdata.png)

And below is the annotated R code! Note we need to first pivot the data such that each series gets its own column. [Plot.ly has great documentation](https://plot.ly/r/reference/) going into different examples related to styling. Much of the below options were outlined in the documentation itself!

	# SQL output is imported as a dataframe variable called 'df'
	# Use Periscope to visualize a dataframe or show text by passing data to periscope.table() or periscope.text() respectively. Show an image by calling periscope.image() after your plot.

	# Use tidyr to pivot the data. We want a column per series
	library(tidyr)
	# Use plot.ly for visualziation
	library(plotly)

	# Pivoting data, see this post for further details https://community.periscopedata.com/t/q5gk76/pivoting-and-melting-dataframes
	df=spread(df,source,count)

	admob_trace <- df$admob
	leadbolt_trace <- df$leadbolt
	organic_trace <- df$organic
	tapjoy_trace <- df$tapjoy

	x <- df$week

	data <- data.frame(x, admob_trace, leadbolt_trace, organic_trace, tapjoy_trace)

	# Check out Plot.ly's documentation to find more options! https://plot.ly/r/reference/

	p <- plot_ly(data, x = ~x) %>%
	  add_trace(y = ~admob_trace, name = 'admob', type = 'scatter', mode = 'lines',
	            line = list(shape = 'linear', color = 'rgb(205, 12, 24)', width= 4, dash = 'dash'),
	            connectgaps = TRUE) %>%
	  add_trace(y = ~leadbolt_trace, name = 'leadbolt',type = 'scatter', mode = 'lines+markers',
	            line = list(shape = 'linear', color = 'rgb(10, 12, 240)', dash = 'dash'),
	            marker = list(symbol = "star-diamond", color = 'rgb(17, 157, 255)',size = 12),
	            connectgaps = TRUE) %>%
	  add_trace(y = ~organic_trace, name = 'organic', type = 'scatter', mode = 'lines',
	            line = list(shape = 'linear', color = 'rgb(10, 120, 24)', dash = 'dot'),
	            connectgaps = TRUE) %>%
	  add_trace(y = ~tapjoy_trace, name = 'tapjoy', type = 'scatter', mode = 'lines',
	            line = list(shape = 'linear', color = 'rgb(100, 10, 100)', width = 2, dash = 'dot'),
	            connectgaps = TRUE) %>%
	  layout(xaxis = list(title = 'Week'), yaxis = list(title = 'Source'))

	periscope.plotly(p)