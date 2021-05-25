import numpy as np
import pandas as pd 
import pickle
from sklearn.neighbors import KNeighborsClassifier

dataset = pd.read_csv('General.csv')

dataset = dataset.sample(frac=1)

training_data = dataset.iloc[:, :-1].to_numpy()
target_data = dataset.iloc[:, -1:].to_numpy()

clf = KNeighborsClassifier()

clf.fit(training_data, target_data.flatten())

pickle.dump(clf, open('General.sav', 'wb'))
