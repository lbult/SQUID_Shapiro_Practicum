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
from support_func import clean_dataset

#load and plot IV curves files
#files = glob.glob("./Data_24_12_Run2_Full_copy/Shapiro_freq4900.0_power_*") #this one is important
#files = files[files.index("./Data_24_12_Run2_Full\Shapiro_freq4900.0_power_-28.0"):]

# load files and their corresponding directories
dir = "./Data_24_12_Run2_Full_copy/"
files = glob.glob("./Data_24_12_Run2_Full_copy/Shapiro_freq3400.0_power_*")

indexx = len(dir)
shapiro_list = []
#print(dir)
for i in files:
    j = i[indexx:]
    if j[0] == "S":
        shapiro_list.append(j)

freq = []
power = []
for i in shapiro_list:
    stuff = i.split("_")
    power.append(float(stuff[-1]))
    freq.append(float(stuff[1].split("q")[1]))
idx = np.argsort(power)
file = np.array(shapiro_list)[idx]
files= []
for j in file:
    files.append(dir + j)
#files = files[::-1]

files = files[files.index("./Data_24_12_Run2_Full_copy/Shapiro_freq3400.0_power_-36.0"):]

for i in files: 
    file = i
    df = pd.read_csv(i, sep=" ")
    df = clean_dataset(df)
    indexx = len(dir)
    j = i[indexx:]
    if j[0] == "S":
        name = j
        stuff = name.split("_")
        power = float(stuff[-1])
        freq = float(stuff[1].split("q")[1])
        
        #find data labels
        labels = df.columns
        # load correct I,V,t
        I = df[labels[1]]
        V = df[labels[2]]

        on1 = False
        on2 = True
        count = 0 
        V_new = []
        I_new = []

        # set current selection range 
        bounds = [-60,20]
        for g in range(0, len(I)):
            if g+1 < len(I):
                if I[g] < bounds[1] and I[g] > bounds[0] and on1 and on2:
                    V_new.append(V[g])
                    I_new.append(I[g]) 
                    count+=1
                if I[g+1] <= bounds[0] and I[g] > bounds[0]:
                    on1 = True
                if I[g+1] <= bounds[1] and I[g] > bounds[1] and on1:
                    on1 = False
                    on2 = False
        V = V_new
        I = I_new

        # create axis
        fig, axs = plt.subplots(1,2)
        
        #set histogram parameters
        V_bounds = [-50, -15]
        no_bins = 100
        
        #set line parameters for the plots
        no_lines = 10
        start_lines = -25
        step = freq*10**12/(4*np.pi*2.4179671*10**14)
        
        # make histogram
        bins = np.arange(V_bounds[0]-(V_bounds[1]-V_bounds[0])/no_bins, V_bounds[1], (V_bounds[1]-V_bounds[0])/no_bins)
        counts, bins = np.histogram(V, bins=bins)
        axs[1].hist(bins[:-1], bins, weights=counts, density=True,orientation="horizontal")

        #plot horizontal Shapiro step lines
        #for m in range(0,no_lines):
        #    axs[0].axhline(y=start_lines+m*step, color='red', linestyle='--',linewidth=0.4)
        #    axs[1].axhline(y=start_lines+m*step, color='red', linestyle='--',linewidth=0.4)
        axs[0].scatter(I, V, s=0.05, color="black")
        
        #print some relevant information
        print(step*10**-6, step, freq)
        print(file)
        
        #set plot boundaries, set axis labels and show
        limit = True
        if limit:
            axs[0].set_ylim(V_bounds)
            axs[1].set_ylim(V_bounds)
        for ax in axs.flat:
            ax.set(xlabel='Current [\u03bcA]', ylabel='Voltage [\u03bcV]')
        plt.show()

    else:
        print("Wrong files or directory specified")