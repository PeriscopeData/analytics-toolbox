# Using R to Plot only the Rolling Average Line

![graph1](/R/Using_R_to_Plot_only_the_Rolling_Average_Line/Images/graph1.png)
    
Want to show a rolling average to your data? Using the Periscope Data [Python / R integration](https://doc.periscopedata.com/article/r-and-python#article-title), we can use a few quick lines in R to accomplish this.

Here are the first few rows of our SQL output - a list of dates with the number of users created on a fictional gaming platform.

![chart1](/R/Using_R_to_Plot_only_the_Rolling_Average_Line/Images/chart1.png)

We now use the rollmean() function from the zoo library in R, as shown below. Note from the [rollmean() documentation](https://www.rdocumentation.org/packages/zoo/versions/1.8-4/topics/rollmean) that you can just as easily calculate a host of other rolling calculations, such as a rolling median or sum.

    library(zoo)

    # Calculating the rolling average. Window is set to 3 here, corresponding to an average of the current row and the 2 preceding rows
    window <- 10
    padding <- rep(NA, window - 1)
    df$rollingavg <- c(padding, rollmean(df$number_users, k = window))

    periscope.table(df)

Now, we make this chart a line graph to visualize the rolling average line by itself!

![graph2](/R/Using_R_to_Plot_only_the_Rolling_Average_Line/Images/graph2.png)

**Tip:** If you want to display both the raw data and the rolling average, Periscope's built-in visualizations has a quick "Show Rolling Average" check box that you can toggle on.

![format](/R/Using_R_to_Plot_only_the_Rolling_Average_Line/Images/format.png)
