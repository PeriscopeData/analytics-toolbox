import pandas as pd
import numpy as np
from sklearn.datasets import load_iris
from sklearn.neighbors import KNeighborsClassifier
from sklearn.utils import shuffle
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

knn_dist = KNeighborsClassifier(n_neighbors = 6, weights = 'distance')
pred_dist = knn_dist.fit(features_train, target_train).predict(features_test)

train_data = np.concatenate((features_train,np.array([target_train]).T, np.array([target_train]).T), axis = 1)
test_data = np.concatenate((features_test,np.array([pred_dist]).T, np.array([target_test]).T), axis = 1)

cols = list(df.columns.values)
cols.remove('target')
cols.extend(['estimated_target','actual_target'])

d_train = pd.DataFrame(train_data, columns = cols)
d_train['dataset'] = 'train'

d_test = pd.DataFrame(test_data, columns = cols)
d_test['dataset'] = 'test'

# Combine Dataframes
df_final = pd.concat([d_train, d_test])

periscope.materialize(df_final)