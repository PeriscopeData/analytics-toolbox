# Using Python to Plot only the Rolling Average Line

![graph1](/Python/Using_Python_to_Plot_only_the_Rolling_Average_Line/Images/graph1.png)
    
Want to show a rolling average to your data? Using the Periscope Data [Python / R integration](https://doc.periscopedata.com/article/r-and-python#article-title), we can accomplish this with a single line of Python code.

Here are the first few rows of our SQL output - a list of dates with the number of users created on a fictional gaming platform.

![chart1](/Python/Using_Python_to_Plot_only_the_Rolling_Average_Line/Images/chart1.png)

We now use the [rolling() function](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.rolling.html) from Python pandas, as shown below.  Note that by changing the .mean() to a .sum(), we can now make this a rolling sum calculation. Neat, huh?

    # SQL output is imported as a pandas dataframe variable called "df"
    import pandas as pd

    df["rolling"] = df["number_users"].rolling(10).mean()

    # Use Periscope to visualize a dataframe or an image by passing data to periscope.output()
    periscope.output(df)
  
Now, we make this chart a line graph to visualize the rolling average line by itself!

![graph2](/Python/Using_Python_to_Plot_only_the_Rolling_Average_Line/Images/graph2.png)

**Tip:** If you want to display both the raw data and the rolling average, Periscope's built-in visualizations has a quick "Show Rolling Average" check box that you can toggle on. 

![format](/Python/Using_Python_to_Plot_only_the_Rolling_Average_Line/Images/format.png)