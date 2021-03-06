import pickle
from matplotlib.pyplot import xlabel
import pandas as pd
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
import glob

"""
Testing a neural network on a verification set
"""

def clean_dataset(df):
    assert isinstance(df, pd.DataFrame), "df needs to be a pd.DataFrame"
    df.dropna(inplace=True)
    indices_to_keep = ~df.isin([np.nan, np.inf, -np.inf]).any(1)
    return df[indices_to_keep].astype(np.float64)

files = glob.glob("./New_Training_Not_Shap/*")

x = pd.read_csv('training_inputs.csv', delimiter=',')
y = pd.read_csv('training_outputs.csv', delimiter=',')

# take away any infinities and NaN
x = clean_dataset(x)
y = clean_dataset(y)

#gather the data in clean lists
xlabels = x.columns
ylabels = y.columns

X = []
m = 0
for i in xlabels:
    X.append(x[xlabels[m]].to_list())
    m+=1
Y = []
m = 0
for i in ylabels:
    Y.append(y[ylabels[m]].to_list())
    m+=1

Ys = []
for i in Y:
    for j in i:
        Ys.append(j)

x_trains = X
y_trains = Y
filename = 'finalized_model_3.sav'

DNN_model = pickle.load(open(filename, 'rb'))

print(DNN_model.score(x_trains, y_trains))

predicted = DNN_model.predict(x_trains)

# create a Boolean index for the wrong classifications
classification_is_wrong = y_trains != predicted

for i in range(len(classification_is_wrong[0])):
    if classification_is_wrong[0][i]:
        files.pop(i)

# print the file names of the wrongly classified mails
#print(files)