import pandas as pd
df=pd.melt(df,id_vars='mydate',var_name='platform',value_name='count')
# Use Periscope to visualize a dataframe or an image by passing data to periscope.output()
periscope.output(df)