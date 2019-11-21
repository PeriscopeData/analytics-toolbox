# SQL output is imported as a pandas dataframe variable called "df"

# Source:  https://stackoverflow.com/questions/19441730/trimmed-mean-with-percentage-limit-in-python
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import tmean, scoreatpercentile
import numpy as np

def trimmean(arr, percent):
    lower_limit = scoreatpercentile(arr, percent)
    upper_limit = scoreatpercentile(arr, 100-percent)
    return tmean(arr, limits=(lower_limit, upper_limit), inclusive=(False, False))

my_result = trimmean(df["amt_paid"].values,10)