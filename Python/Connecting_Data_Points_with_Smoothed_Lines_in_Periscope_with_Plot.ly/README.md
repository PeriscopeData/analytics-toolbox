# Connecting Data Points with Smoothed lines (Spline Curves) in Periscope with Plot.ly (Python and R)

![Smooth lines](/R/Connecting_Data_Points_with_Smoothed_Lines_in_Periscope_with_Plot.ly/Images/smooth_lines.png)

Ever looked at a chart like this:

![Pointy lines](/R/Connecting_Data_Points_with_Smoothed_Lines_in_Periscope_with_Plot.ly/Images/pointy_lines.png)

and thought to yourself that the data would make much more sense with curved lined connecting the points, rather than straight lines? Well fear not, because [plot.ly](https://plot.ly/) makes it easy to adjust this using the spline shape of line objects!

To start, let's assume the following data from a fictional gaming company is the head of our SQL output:

![table](/R/Connecting_Data_Points_with_Smoothed_Lines_in_Periscope_with_Plot.ly/Images/table.png)

Then, we use either [R or Python's plot.ly libraries](https://doc.periscopedata.com/article/plot-ly#article-title) via the [Periscope Python and R integration](https://doc.periscopedata.com/article/r-and-python) to generate our chart. Notice the reference to "spline," which gives us those nice smooth lines. (other options for connecting lines can be found on the [plot.ly documentation and example here](https://plot.ly/~NiloTCC/30/linear-spline-vhv-hvh-vh-hv/#/)).

We've included both R and Python code below for reference. Either achieves the desired output.

#### R

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
    
#### Python 3.6

    # SQL output is imported as a dataframe variable called 'df'
    import pandas as pd
    import plotly.plotly as py
    import plotly.graph_objs as go

    # Create trace. Notice the reference to shape in the line argument of the trace. This is set to spline, generating smoothed connectors
    trace = dict(
        x = df.week,
        y = df['count'],
        mode = 'lines+markers',
        type = 'scatter',
        name = 'count',
        line = dict(shape = 'spline', color = 'rgb(205, 12, 24)', width= 4, dash = 'dash'),
        marker = dict(symbol = "star-diamond", color = 'rgb(17, 157, 255)',size = 8),
        connectgaps = True
    )

    # Create layout parameter to assing axes titles and set margins
    layout =  dict(
        xaxis = dict(title = 'Week'),
        yaxis = dict(title = 'Count'),
        margin = dict(
            l=70,
            r=10,
            b=50,
            t=10
        )
    )

    # Compose the final figure
    data = [trace]
    fig =  go.Figure(data = data, layout = layout)

    # Use Periscope to visualize a dataframe, text, or an image by passing data to periscope.table(), periscope.text(), or periscope.image() respectively.
    periscope.plotly(fig)
