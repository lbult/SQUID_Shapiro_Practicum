from os import defpath
from typing_extensions import ParamSpec
import pandas as pd
import glob
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit, minimize
from scipy.sparse import dok
from scipy.sparse.base import SparseEfficiencyWarning
from sklearn import preprocessing
import random

#load and plot IV curves files
not_shapiro_files = glob.glob("./New_Training_Not_Shap/*")
shapiro_files = glob.glob("./New_Training_Shap/*")

#define training sets
shapiro_input = []
shapiro_output = []

for i in shapiro_files: #replace shapiro_files by not_shapiro_files
    df = pd.read_csv(i, sep=" ")
    #find data labels
    labels = df.columns
    # load t, I, V
    t = df[labels[0]]
    t = t[:8000]
    I = df[labels[1]]
    I = I[:8000]
    V = df[labels[2]]
    V = V[:8000]
    V = V * 0.1 # scale voltage data 

    # for each bit of data save the parameters of the polynomial expansion
    #param, cov = curve_fit(ShapiroFunc, I, V)
    #param = preprocessing.minmax_scale(param, feature_range=(-1, 1), axis=0, copy=True)
    #params = []
    params = []
    for i in V:
        params.append(i)
    params = preprocessing.minmax_scale(params, feature_range=(-1, 1), axis=0, copy=True)
    shapiro_input.append(params)
    shapiro_output.append([1])

not_shapiro_files = random.sample(not_shapiro_files, int(len(not_shapiro_files)/2))

for i in not_shapiro_files: #replace shapiro_files by not_shapiro_files
    df = pd.read_csv(i, sep=" ")
    #find data labels
    labels = df.columns
    # load t, I, V
    t = df[labels[0]]
    t = t[:8000]
    I = df[labels[1]]
    I = I[:8000]
    V = df[labels[2]]
    V = V[:8000]
    V = V * 0.1 # scale voltage data 

    # for each bit of data save the parameters of the polynomial expansion
    #param, cov = curve_fit(ShapiroFunc, I, V, jac=ShapiroDiff)
    #param = preprocessing.minmax_scale(param, feature_range=(-1, 1), axis=0, copy=True)
    params = []
    for i in V:
        params.append(i)
    params = preprocessing.minmax_scale(params, feature_range=(-1, 1), axis=0, copy=True)
    shapiro_input.append(params)
    shapiro_output.append([0])


m = 0
for i in shapiro_output:
    shapiro_output[m].insert(0,m)
    m+=1
'''
n = 0
for i in shapiro_input:
    shapiro_input[n].insert(0,n)
    n+=1'''

shapiro_input = pd.DataFrame(shapiro_input)
shapiro_input = shapiro_input.T
shapiro_output = pd.DataFrame(shapiro_output)
shapiro_output = shapiro_output.T

shapiro_input.to_csv('training_inputs.csv', index = False, header= False)
shapiro_output.to_csv('training_outputs.csv',index = False, header= False)

'''
param, cov = curve_fit(func, I, V)
x1 = np.linspace(np.min(I),np.max(I),1000)
y = func(x1, *param)

param2, cov2 = curve_fit(ShapiroFunc, I, V)
x2 = np.linspace(np.min(I),np.max(I),1000)
y2 = ShapiroFunc(x2, *param2)

shapiro_input.append(param2)
print(shapiro_input)

V_new = []
j=0
for i in y2:
    V_new.append(i-y[j])
    j+=1

V_list = []
j=0
for i in V_new:
    if j>0 and j<len(V_new)-1:
        if i >= V_new[j-1] and i >= V_new[j+1]:
            indx = V_new.index(i)
            V_list.append(y2[indx])
        if i <= V_new[j-1] and i <= V_new[j+1]:
            indx = V_new.index(i)
            V_list.append(y2[indx])
    j+= 1

print(V_list)

plt.plot(x1,y, linewidth=1, color='r')
plt.plot(x1,y2, linewidth=1, color='b')
plt.scatter(I, V, s=0.05)
plt.title("IV-curve at f = 1440 Hz, power = -3.2d B")
plt.xlabel("Current")
plt.ylabel("Voltage")

'''
'''y = -7.5
while y < 5:
    if y <7.5:
        plt.axhline(y=y, color='r', linestyle='--')
        y += 2.5'''
#plt.show()