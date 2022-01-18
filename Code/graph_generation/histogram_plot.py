from cmath import nan
import glob
from pickle import FALSE
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import preprocessing
import cv2

no_bins = 140
power_range = [-50,0]
freqw = 3500

files = glob.glob("./Data_24_12_Run2_Full/Shapiro_freq"+ str(freqw) + ".0_power_*")
#files = ["./Data_24_12_Run2_Full\Shapiro_freq4900.0_power_-25.0","./Data_24_12_Run2_Full\Shapiro_freq4900.0_power_-27.0","./Data_24_12_Run2_Full\Shapiro_freq4900.0_power_-28.0", "./Data_24_12_Run2_Full\Shapiro_freq4900.0_power_-29.0", "./Data_24_12_Run2_Full\Shapiro_freq4900.0_power_-30.0"]
#sort files
directory = "./Data_24_12_Run2_Full/"
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

m = 0
hists = []
bins = []
power = []

img = np.full((no_bins,(abs(power_range[1]-power_range[0]))), 1)
ct = 0
for i in files:
    df = pd.read_csv(i, sep=" ")
    labels = df.columns
    # load I, V
    I = df[labels[1]]
    In = []
    V = df[labels[2]] 
    V_new = []
    I_new = []

    I = preprocessing.minmax_scale(I, feature_range=(-10, 200), axis=0, copy=True)
    for i in I:
        In.append(i)


    on1 = False
    on2 = True
    count = 0
    bounds = [0,190]
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

    hist, biness = np.histogram(V_new, bins=no_bins, density=True)
    hist = preprocessing.minmax_scale(hist, feature_range=(0, 255), axis=0, copy=True)
    hist = hist[~np.isnan(hist)]
    k=0
    kt=0

    for j in hist:
        if power_range[0] < (m-50) < power_range[1]:
            # np arrays
            img[kt][ct] = j
            kt+=1
            # lists
            bins.append( -16.258155906593405 + (7.7535+16.258155906593405)/len(hist))
            power.append(m-50)
            hists.append(j)
            k+=1
    m+=1
    ct += 1

#for m in range(0,300):
#    plt.axhline(y=(9+(m-100)*freqw*10**12/(2*2.4179671*10**14)), color='black', linestyle='--', linewidth=0.7)

#print(freqw*10**12/(2*2.4179671*10**14))


img = img.astype(np.uint8)
plt.imshow(img, aspect="auto", cmap=plt.cm.pink, extent=[power_range[0],power_range[1],-160.258155906593405,70.7535])
plt.colorbar()
plt.xlabel("RF transmitter power [dBm]")
plt.ylabel("Voltage [\u03bcV]")
plt.show()