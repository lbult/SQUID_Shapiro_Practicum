from os import defpath
import pandas as pd
import glob
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