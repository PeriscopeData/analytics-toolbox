# Transposing Tables using Python Pandas

Pandas makes transposing tables beautifully simple! Below are a couple examples using the example SQL output below:

![table1](/Python/Transposing_Tables_using_Python_Pandas/Images/table1.png)

This first Python snippet allows you to define your own column headers:

    # SQL output is imported as a pandas dataframe variable called "df"
    import pandas as pd

    df2=df.T
    df2.columns=['label 1', 'label 2','label 3','label 4']

    # Use Periscope to visualize a dataframe or an image by passing data to periscope.output()
    periscope.output(df2)

![table2](/Python/Transposing_Tables_using_Python_Pandas/Images/table2.png)

And this Python snippet makes the first row your column headers

    # SQL output is imported as a pandas dataframe variable called "df"
    import pandas as pd
    df2=df.T
    header=df2.iloc[0]
    df2=df2[1:]
    df2.columns=header
    # Use Periscope to visualize a dataframe or an image by passing data to periscope.output()
    periscope.output(df2)
    
![table3](/Python/Transposing_Tables_using_Python_Pandas/Images/table3.png)

Transposing back to the original table is a little different!

Suppose your SQL output is something like this:

![table4](/Python/Transposing_Tables_using_Python_Pandas/Images/table4.png)


And you wanted your output to look like this:

![table5](/Python/Transposing_Tables_using_Python_Pandas/Images/table5.png)

In this case, you'd need to reset the index to preserve the original column titles as well as rename the resulting columns. The following Python code will do nicely!

    # SQL output is imported as a pandas dataframe variable called "df"
    import pandas as pd

    df = df.T.reset_index()
    df.columns = ["source", "count"]

    # Use Periscope to visualize a dataframe or an image by passing data to periscope.output()
    periscope.output(df)