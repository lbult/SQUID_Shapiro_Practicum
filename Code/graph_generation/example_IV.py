import glob
from pickle import FALSE
import matplotlib.pyplot as plt
import random
import pandas as pd
import numpy as np


files = glob.glob("./Data_24_12_Run2_Partial/*")
#files = files[files.index("./New_Training_Shap/Shapiro_freq1660.0_power_-4.0"):]
#files = glob.glob("./Train_Shap/*")
#files = ["./Data_24_12_Run2_Full_Copy/Shapiro_freq4900.0_power_-3.0", "./Data_24_12_Run2_Full_Copy/Shapiro_freq4900.0_power_-24.0",
#        "./Data_24_12_Run2_Full_Copy/Shapiro_freq4900.0_power_-27.0", "./Data_24_12_Run2_Full_Copy/Shapiro_freq4900.0_power_-50.0"]
files = random.sample(files,4)
#dir = "./Data_24_12_Run2_Full_Copy/"
dir = "./Data_24_12_Run2_Partial/"

one = True
two = False
three = False
four = False
ax1 = 0
ax2 = 0

fig,axs = plt.subplots(2,2)

for i in files:
    df = pd.read_csv(i, sep=" ")
    indexx = len(dir)
    j = i[indexx:]
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
    bounds = [-40,-10]
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
    
    #set line parameters for the plots
    no_lines = 10
    start_lines = -20
    step = freq*10**12/(4*np.pi*2.4179671*10**14)
    
    if four:
        axs[1,1].scatter(I,V,s=0.05)
        #for m in range(0,5): #range(0,int((V_new[-1]-V_new[0])/step)):
        #    axs[1,1].axhline(y=start_lines+m*step, color='red', linestyle='--',linewidth=0.4)

    if three:
        axs[1,0].scatter(I,V,s=0.05,color='tab:orange')
        #for m in range(0,5): #range(0,int((V_new[-1]-V_new[0])/step)):
        #    axs[1,0].axhline(y=start_lines+m*step, color='red', linestyle='--',linewidth=0.4)
        three = False
        four = True

    if two:
        axs[0,1].scatter(I,V,s=0.05,color='tab:red')
        #for m in range(0,5): #range(0,int((V_new[-1]-V_new[0])/step)):
        #    axs[0,1].axhline(y=start_lines+m*step, color='red', linestyle='--',linewidth=0.4)
        two = False
        three = True
    
    if one:
        axs[0,0].scatter(I,V,s=0.05,color='tab:green')
        #for m in range(0,5): #range(0,int((V_new[-1]-V_new[0])/step)):
        #    axs[0,0].axhline(y=start_lines+m*step, color='red', linestyle='--',linewidth=0.4)
        one = False
        two = True


for ax in axs.flat:
    ax.set(xlabel='Current [\u03bcA]', ylabel='Voltage [\u03bcV]')

# Hide x labels and tick labels for top plots and y ticks for right plots.
for ax in axs.flat:
    ax.label_outer()

plt.show()