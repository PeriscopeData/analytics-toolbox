# SQL output is imported as a dataframe variable called 'df'
# Use Periscope to visualize a dataframe or show text by passing data to periscope.table() or periscope.text() respectively. Show an image by calling periscope.image() after your plot.

# Use plot.ly for visualziation
library(plotly)

# Assign variables
trace <- df$count
x <- df$week
data <- df[order(df$week),]

# Check out Plot.ly's documentation to find more options! https://plot.ly/r/reference/
# The line paramater inside add_trace contains a shape parameter. Set this to spline for smoothed connectors
p <- plot_ly(data, x = ~x) %>%
  add_trace(y = ~trace, name = 'count', type = 'scatter', mode = 'lines+markers',
            line = list(shape = 'spline', color = 'rgb(205, 12, 24)', width= 4, dash = 'dash'),
            marker = list(symbol = "star-diamond", color = 'rgb(17, 157, 255)',size = 8),
            connectgaps = TRUE) %>%
  layout(xaxis = list(title = 'Week'), yaxis = list(title = 'Count'))  %>% config(displayModeBar = TRUE)

# Output the chart in Periscope
periscope.plotly(p)