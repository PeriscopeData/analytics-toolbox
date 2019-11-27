import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris
from sklearn.neighbors import KNeighborsClassifier
from sklearn.utils import shuffle
from sklearn.metrics import f1_score
import matplotlib.pyplot as plt
import random

random.seed(123)

iris  = load_iris()
df = pd.DataFrame(data= np.c_[iris['data'], iris['target']],
                     columns= iris['feature_names'] + ['target'])
df = df.drop('petal width (cm)', axis = 1)

df = shuffle(df, random_state = 300)

df_features = df.drop('target', axis = 1)
features = df_features.values
target = df["target"].values

num_rows = df.shape[0]
train_cutoff = int(num_rows * 0.6)
dev_cutoff = int(num_rows * 0.8)

features_train = features[:train_cutoff,:]
features_dev = features[train_cutoff:dev_cutoff,:]
features_test = features[dev_cutoff:,:]

target_train = target[:train_cutoff]
target_dev = target[train_cutoff:dev_cutoff]
target_test = target[dev_cutoff:]

all_k = range(1,11)
uniform = []
distance = []

# Looping through all values of k
for nbrs in all_k:
  knn_uni = KNeighborsClassifier(n_neighbors = nbrs, weights = 'uniform')
  knn_dist = KNeighborsClassifier(n_neighbors = nbrs, weights = 'distance')
  pred_uni = knn_uni.fit(features_train, target_train).predict(features_dev)
  pred_dist = knn_dist.fit(features_train, target_train).predict(features_dev)
  f1_uni = f1_score(target_dev, pred_uni, average = 'macro')
  f1_dist = f1_score(target_dev, pred_dist, average = 'macro')
  uniform.append(f1_uni)
  distance.append(f1_dist)

fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
ax1.plot(all_k, uniform)
ax1.set_title('Uniform Weights')
ax1.set_ylabel('F1 Score')
ax2.plot(all_k, distance)
ax2.set_title('Distance Weights')

# Use Periscope to visualize a dataframe, text, or an image by passing data to periscope.table(), periscope.text(), or periscope.image() respectively.
periscope.image(fig)