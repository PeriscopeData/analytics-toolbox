# SQL output is imported as a pandas dataframe variable called "df"
import pandas as pd

df2=df.T
df2.columns=['label 1', 'label 2','label 3','label 4']

# Use Periscope to visualize a dataframe or an image by passing data to periscope.output()
periscope.output(df2)