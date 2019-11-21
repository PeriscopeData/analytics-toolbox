# SQL output is imported as a pandas dataframe variable called "df"
import pandas as pd
from scipy.stats import trim_mean
import numpy as np

my_result = trim_mean(df["amt_paid"].values, 0.1)