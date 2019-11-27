# Prepping a dataframe to hold your training and testing data - Machine Learning

Once you have optimized your hyperparameters, it may be nice to create a dataframe that has some of your testing and training data to train your model. Here, we are going to use a KNN model with n_neighbors = 6 and "distance" weights on the iris dataset. We will be creating a dataframe with the following columns:

- olumns for each of the features (a.k.a. the inputs of your model)
- Columns for the actual iris classification (the target)
- Columns for the predicted iris classification (note, this would be just be the actual iris classification for the data that was in the training dataset)
- A column that labels whether the row is in the "test" or "train" dataset

With this data, we can create charts like:

1. Plotting the training data against the testing data
2. Displaying the final accuracy / F1 score as a number overlay on a dashboard

With that, below is the Python 3.6 code used. We are building this in a [Periscope view](https://doc.periscopedata.com/article/views#article-title) so we can materialize our result on the Periscope cache and be able to refer to it in other future analyses. Note that if you have a very large training dataset, you may need to truncate the number of records in this dataframe. Alternatively, you can create a dataframe for just your test dataset.

First, we import our desired libraries

	import pandas as pd
	import numpy as np
	from sklearn.datasets import load_iris
	from sklearn.neighbors import KNeighborsClassifier
	from sklearn.utils import shuffle
	import random

Next, we set a random seed so we can use the same split from tuning our hyperparameters (see post here)

	random.seed(123)

Then, we create our dataset. Note that you can very easily skip this step and use your SQL output. Be sure that your SQL output has columns for your features (these are the elements used to predict the classification of your data), and the target (this is the classification)

	iris  = load_iris()
	df = pd.DataFrame(data= np.c_[iris['data'], iris['target']],
	                     columns= iris['feature_names'] + ['target'])
	df = df.drop('petal width (cm)', axis = 1)

We then shuffle the dataframe, also with a random_state to ensure we are consistent with the split from hyperparameter tuning

	df = shuffle(df, random_state = 300)

We then remove the target column to get just our feature names

	df_features = df.drop('target', axis = 1)
	features = df_features.values
	target = df["target"].values

Next, we split the data into testing and training data. We are using the split of 60% training data - 20% dev data, and 20% test data. We used dev data for tuning hyperparameters, so we won't be putting this in our final dataframe.

	num_rows = df.shape[0]
	train_cutoff = int(num_rows * 0.6)
	dev_cutoff = int(num_rows * 0.8)

	features_train = features[:train_cutoff,:]
	features_dev = features[train_cutoff:dev_cutoff,:]
	features_test = features[dev_cutoff:,:]

	target_train = target[:train_cutoff]
	target_dev = target[train_cutoff:dev_cutoff]
	target_test = target[dev_cutoff:]

Now, it's time to generate the model

	knn_dist = KNeighborsClassifier(n_neighbors = 6, weights = 'distance')
	pred_dist = knn_dist.fit(features_train, target_train).predict(features_test)

Then, we build our dataframe. Note that to do this, we are creating 2 dataframes (one for the test and one for the training data), and concatenating them together

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

Now, we finally materialize our output

	periscope.materialize(df_final)