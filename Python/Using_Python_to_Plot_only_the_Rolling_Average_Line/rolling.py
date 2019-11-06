# SQL output is imported as a pandas dataframe variable called "df"
import pandas as pd

df["rolling"] = df["number_users"].rolling(10).mean()

# Use Periscope to visualize a dataframe or an image by passing data to periscope.output()
periscope.output(df)