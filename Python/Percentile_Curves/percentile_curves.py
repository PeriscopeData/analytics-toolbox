# SQL output is imported as a pandas dataframe variable called "df"
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import scoreatpercentile

a=list(range(1,101))

b = [scoreatpercentile(df["amt_paid"],i) for i in a]

df2 = pd.DataFrame({'percentile': a, 'value': b}, columns=['percentile', 'value'])

# Use Periscope to visualize a dataframe, text, or an image by passing data to periscope.table(), periscope.text(), or periscope.image() respectively.
periscope.table(df2)