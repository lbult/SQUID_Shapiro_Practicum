import glob
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import preprocessing

f = 0
while f < 10:
    files = glob.glob("./Data_24_12_Run1_Full/Shapiro_freq15"+ str(f*10)+ ".0_power_*")
    
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
        files.append("./Data_24_12_Run1_Full/"+ j)

    m = 0
    hists = []
    bins = []
    power = []
    for i in files:
        df = pd.read_csv(i, sep=" ")
        labels = df.columns
        # load I, V
        I = df[labels[1]]
        V = df[labels[2]]
        V = V*0.1

        hist, biness = np.histogram(V, bins=200, density=True)
        hist = preprocessing.minmax_scale(hist, feature_range=(0, 1), axis=0, copy=True)
        k=0
        for j in hist:
            bins.append((-1+2*k)/len(hist))
            power.append(m-50)
            hists.append(j)
            k+=1 
        m+=1
    plt.scatter(power, bins, c=hists, s=4)
    plt.title(str(f*10))
    plt.show()
    f+=1