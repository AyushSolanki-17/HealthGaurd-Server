import numpy as np
import pandas as pd 
from sklearn.ensemble import RandomForestClassifier
import pickle

dataset = pd.read_csv('Chikungunya.csv')

dataset = dataset.sample(frac=1)

training_data = dataset.iloc[:, :-1].to_numpy()
target_data = dataset.iloc[:, -1:].to_numpy()

clf = RandomForestClassifier(n_estimators=100)

clf.fit(training_data, target_data.flatten())

pickle.dump(clf, open('Chikungunya.sav', 'wb'))
