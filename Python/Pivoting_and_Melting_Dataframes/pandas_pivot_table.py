# SQL output is imported as a pandas dataframe variable called "df"
import pandas as pd
df=pd.pivot_table(df,index='mydate',columns='platform',values='count')
df=df.reset_index()
# Use Periscope to visualize a dataframe or an image by passing data to periscope.output()
periscope.output(df)