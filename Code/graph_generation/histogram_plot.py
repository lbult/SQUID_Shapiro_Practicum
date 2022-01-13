from cmath import nan
import glob
from pickle import FALSE
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import preprocessing
import cv2

f = 1
while f < 10:
    files = glob.glob("./Data_24_12_Run1_Full/Shapiro_freq1660"+ str() + ".0_power_*")
    
    #sort files
    directory = "./Data_24_12_Run1_Full/"
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

    img = np.full((300,51), 1)
    ct = 0
    for i in files:
        df = pd.read_csv(i, sep=" ")
        labels = df.columns
        # load I, V
        I = df[labels[1]]
        I = I
        V = df[labels[2]]
        V = V*0.1  
        V_new = []
        I_new = []

        I = preprocessing.minmax_scale(I, feature_range=(-10, 200), axis=0, copy=True)
        
        on1 = False
        on2 = True
        count = 0 
        for g in range(0, len(I)):
            if I[g] < 160 and I[g] > 50 and on1 and on2:
                V_new.append(V[g]) 
                I_new.append(I[g])
                count+=1
            if I[g-1] <= 50 and I[g] > 50:
                on1 = True
            if I[g-1] <= 160 and I[g] > 160 and on1:
                on1 = False
                on2 = False

        hist, biness = np.histogram(V_new, bins=300, density=True)
        hist = preprocessing.minmax_scale(hist, feature_range=(0, 255), axis=0, copy=True)
        hist = hist[~np.isnan(hist)]
        
        k=0
        kt=0
        for j in hist:
            # np arrays
            img[kt][ct] = j
            kt+=1
            # lists
            bins.append((-1+2*k)/len(hist))
            power.append(m-50)
            hists.append(j)
            k+=1
        m+=1
        ct += 1

    #offset = 10
    #for i in range(0,len(hists)):
    #    plt.plot(V, bins[i]+offset*i)
    
    img = img.astype(np.uint8)
    plt.imshow(img, aspect="auto", cmap=plt.cm.RdPu)
    plt.colorbar()
    plt.show()

    #plt.scatter(power, bins, c=hists, s=4)
    #plt.title(str(f*10))
    plt.xlabel("RF Transmitter Power [dB]")
    plt.ylabel("Normalised Voltage [-]")
    #plt.show()
    f+=1