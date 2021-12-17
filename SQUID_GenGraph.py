from typing_extensions import ParamSpec
import os
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit, minimize
from scipy.sparse.base import SparseEfficiencyWarning

#load and plot IV curves files
not_shapiro_files = glob.glob("./No_Shapiro_Steps/*.dat")
shapiro_files = glob.glob("./Shapiro_Steps/*.dat")
for i in not_shapiro_files: #replace shapiro_files by not_shapiro_files
    df = pd.read_csv(i, sep=" ")
    #find data labels
    labels = df.columns
    # load t, I, V
    t = df[labels[0]]
    I = df[labels[1]]
    V = df[labels[2]]
    V = V*0.1 # scale voltage data 
    plt.scatter(I, V, s=0.05)
    plt.title("IV-curve at f = 1440 Hz, power = -3.2d B")
    plt.xlabel("Current" + i)
    plt.ylabel("Voltage")
    plt.show()