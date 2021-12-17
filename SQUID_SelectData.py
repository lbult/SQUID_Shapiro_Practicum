import pickle
import time
from matplotlib.pyplot import xlabel
import pandas as pd
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn import preprocessing

# load neural network, takes 0.008579730987548828s for one graph
filename = 'finalized_model.sav'
DNN_model = pickle.load(open(filename, 'rb'))

# choose number of frequencies to sample
freq_samples = 100
frequencies = np.linspace(1000,6000,freq_samples)

# choose number of powers to sample
power_samples = 51
powers = np.linspace(-50,0,power_samples)

# generated dataset
dataset_I = []
dataset_V = []

for i in range(len(frequencies)):
    freq = frequencies[i]
    snv.write("f%.2f" % freq)
    for j in range(len(powers)):
        power = powers[j]
        snv.write("W%.2f" % power)
        I,Vs,t = get_IV_t()
        V=0.1*Vs[:8000]
        V=preprocessing.minmax_scale(V, feature_range=(-1, 1), axis=0, copy=True)
        # determine if shapiro or not
        shapiro = DNN_model.predict([V])
        if shapiro[0] == 1:
            dataset_I.append(I)
            dataset_V.append(Vs)

dataset_I = pd.DataFrame(dataset_I)
dataset_I = dataset_I.T
dataset_V = pd.DataFrame(dataset_V)
dataset_V = dataset_V.T

dataset_I.to_csv('I_shapiro.csv', index = False, header= False)
dataset_V.to_csv('V_shapiro.csv',index = False, header= False)