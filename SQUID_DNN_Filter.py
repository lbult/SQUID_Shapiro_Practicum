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
import glob
import os
from support_func import clean_dataset

not_shapiro_files = glob.glob("./Data_24_12_Run3/*")
print(len(not_shapiro_files))

x = pd.read_csv('training_inputs_filter.csv', delimiter=',')
#y = pd.read_csv('training_outputs.csv', delimiter=',')

# take away any infinities and NaN, gather clean lists
x = clean_dataset(x)
xlabels = x.columns

#format the data
X = []
m = 0
for i in xlabels:
    X.append(x[xlabels[m]].to_list())
    m+=1

# load and execute the model from file
filename = 'finalized_model_4.sav'
#filename = 'finalized_model_3_good_question_mark.sav'
indexx = 0
loaded_model = pickle.load(open(filename, 'rb'))
for i in X:
    shap = loaded_model.predict([i])
    print(shap)
    print(indexx)
    if shap[0] != 1:
        os.remove(str(not_shapiro_files[indexx]))
        print("Delete file")
    indexx += 1


