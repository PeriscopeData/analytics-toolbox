import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

def ecdf(data):
    """Compute ECDF for a one-dimensional array of measurements."""

    # Number of data points: n
    n = len(data)

    # x-data for the ECDF: x
    x = np.sort(data)

    # y-data for the ECDF: y
    y = np.arange(1, n+1) / n

    return x, y

x, y = ecdf(df["temperature"])

plt.figure(figsize=(8,7))
sns.set()
plt.plot(x, y, marker=".", linestyle="none")
plt.xlabel("Body Temperature (F)")
plt.ylabel("Cumulative Distribution Function")


samples = np.random.normal(np.mean(df["temperature"]), np.std(df["temperature"]), size=10000)

x_theor, y_theor = ecdf(samples)

plt.plot(x_theor, y_theor)
plt.legend(('Normal Distribution', 'Empirical Data'), loc='lower right')

print(stats.normaltest(df["temperature"]))

periscope.output(plt)


