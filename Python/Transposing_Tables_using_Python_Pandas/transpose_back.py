# SQL output is imported as a pandas dataframe variable called "df"
import pandas as pd

df = df.T.reset_index()
df.columns = ["source", "count"]

# Use Periscope to visualize a dataframe or an image by passing data to periscope.output()
periscope.output(df)