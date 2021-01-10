import pandas as pd
import numpy as np
from sklearn.metrics import f1_score, r2_score
from sklearn.model_selection import cross_val_score
from sklearn import tree
from joblib import dump, load

data = pd.read_csv("murb.csv", sep=r'\s*,\s*', header=0, encoding='ascii', engine='python')

# Shuffle Data
data = data.sample(frac=1)

# Split into training and test data (80 and 20% each)
training_data, test_data = np.split(data, [int(0.8 * len(data))])

# Define X and Y
X = training_data[['hour', 'month', 'average_power_for_condo', 'min_power_for_condo', 'max_power_for_condo']]
X_test = test_data[['hour', 'month', 'average_power_for_condo', 'min_power_for_condo', 'max_power_for_condo']]
Y = training_data['power']
Y_test = test_data['power']

# Fit Regression Model

clf = tree.DecisionTreeRegressor()

# Fit and Predict
clf.fit(X, Y)
Y_predict = clf.predict(X_test)

# Predictor scores
test = r2_score(Y_predict, Y_test)
test2 = cross_val_score(clf, X_test, Y_test)
print(test)
print(test2)

# Export Model
dump(clf, 'murb.csv.joblib')
