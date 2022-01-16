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
import seaborn as sns

first = True

frequencies_to_check = np.arange(4080,4090,10)

for freq in frequencies_to_check:
    files = glob.glob("./Data_24_12_Run2_Full/Shapiro_freq"+ str(freq) + ".0_power_*")
    directory = "./Data_24_12_Run2_Full/"
    
    files = ["./Data_24_12_Run2_Full\Shapiro_freq4900.0_power_-25.0","./Data_24_12_Run2_Full\Shapiro_freq4900.0_power_-27.0","./Data_24_12_Run2_Full\Shapiro_freq4900.0_power_-28.0", "./Data_24_12_Run2_Full\Shapiro_freq4900.0_power_-29.0", "./Data_24_12_Run2_Full\Shapiro_freq4900.0_power_-30.0"]

    indexx = len(directory)
    shapiro_list = []

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
        files.append(directory + j)

    #files = ["./New_Training_Shap\Shapiro_freq1555.5555555555557_power_-14.0"]
    for i in files: 
        df = pd.read_csv(i, sep=" ")
        df = clean_dataset(df)
        indexx = len(directory)
        j = i[indexx:]
        if j[0] == "S":
            name = j
            stuff = name.split("_")
            power = float(stuff[-1])
            freq = float(stuff[1].split("q")[1])
            
            #find data labels
            labels = df.columns
            # load t, I, V
            I = df[labels[1]]
            V = df[labels[2]]

            on1 = False
            on2 = True
            count = 0 
            V_new = []
            I_new = []
            bounds = [0,25]
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

            V0 = freq*10**12/(2*2.4179671*10**14)
            
            V_bounds = [-20,0]
            no_bins = 50
            bins = np.arange(V_bounds[0]-30/no_bins, V_bounds[1], (V_bounds[1]-V_bounds[0])/no_bins)
            if first:
                counts, bins = np.histogram(V_new, bins=bins)
                first=False
            else:
                counts1, bins1 = np.histogram(V_new, bins=bins)
                for i in range(0, len(counts)):
                    counts[i] = counts[i]+counts1[i]
    
    #weights = [1,0.66,0.33,0.66,0.33]
    #countss = counts
    #for i in range(0, len(counts)):
    #    if i-2>=0 and i+3<len(counts):
    #        llist = [counts[i],counts[i-1],counts[i-2],counts[i+1],counts[i+2]]
    #        countss[i] = np.average(llist, weights=weights)
    
    #sns.distplot(counts, bins=bins, hist=True)
    plt.hist(bins[:-1], bins, weights=counts)
    for m in range(0,int((V_bounds[1]-V_bounds[0])/(freq*10**12/(4*np.pi*2.4179671*10**14)))):
        plt.axvline(x=(V_bounds[0]+(m)*freq*10**12/(4*np.pi*2.4179671*10**14)), color='black', linestyle='--', linewidth=0.6)
    plt.xlabel("Voltage [\u03bcV]")
    plt.ylabel("Bin Counts")
    #plt.savefig("./Saved_Figs/CombHist"+str(freq)+".jpg")
    plt.show()
    plt.clf()