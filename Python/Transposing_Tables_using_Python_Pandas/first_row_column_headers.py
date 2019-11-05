# SQL output is imported as a pandas dataframe variable called "df"
import pandas as pd
df2=df.T
header=df2.iloc[0]
df2=df2[1:]
df2.columns=header
# Use Periscope to visualize a dataframe or an image by passing data to periscope.output()
periscope.output(df2)