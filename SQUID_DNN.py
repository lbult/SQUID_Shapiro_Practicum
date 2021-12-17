"""
@article{scikit-learn,
 title={Scikit-learn: Machine Learning in {P}ython},
 author={Pedregosa, F. and Varoquaux, G. and Gramfort, A. and Michel, V.
         and Thirion, B. and Grisel, O. and Blondel, M. and Prettenhofer, P.
         and Weiss, R. and Dubourg, V. and Vanderplas, J. and Passos, A. and
         Cournapeau, D. and Brucher, M. and Perrot, M. and Duchesnay, E.},
 journal={Journal of Machine Learning Research},
 volume={12},
 pages={2825--2830},
 year={2011}
}
"""
import pickle
from matplotlib.pyplot import xlabel
import pandas as pd
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split

def clean_dataset(df):
    assert isinstance(df, pd.DataFrame), "df needs to be a pd.DataFrame"
    df.dropna(inplace=True)
    indices_to_keep = ~df.isin([np.nan, np.inf, -np.inf]).any(1)
    return df[indices_to_keep].astype(np.float64)

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

x_trains = [X[0], X[1], X[2]]
y_trains = [Y[0], Y[1], Y[2]]

# split data in a training and test set
x_train, x_test, y_train, y_test = train_test_split(X, Ys, test_size=6, random_state=1, shuffle=True)
clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(1200), random_state=1)

#train the neural network
clf.fit(x_train, y_train)

#see how wel it performs on train, test, shapiro datasets
print(clf.score(x_train, y_train))
print(clf.score(x_test, y_test))
print(clf.score(x_trains, y_trains))


# save the model to disk
filename = 'finalized_model.sav'
pickle.dump(clf, open(filename, 'wb'))

'''
# some time later...
 
# load the model from disk
loaded_model = pickle.load(open(filename, 'rb'))
result = loaded_model.score(X_test, Y_test)
print(result)'''


