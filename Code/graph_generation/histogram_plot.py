import glob
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
        V = df[labels[2]]
        V = V*0.1

        hist, biness = np.histogram(V, bins=300, density=True)
        hist = preprocessing.minmax_scale(hist, feature_range=(0, 255), axis=0, copy=True)
        k=0
        kt = 0
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


    # cv2 imshow code
    img = img.astype(np.uint8)
    #calculate the 50 percent of original dimensions
    width = int(img.shape[1] * 13.33)
    height = int(img.shape[0] * 1.33)
    # dsize
    dsize = (width, height)

    # resize image
    #img = img[:, 30:]
    img = cv2.resize(img, dsize)
    img = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
    cv2.imshow('image',img)
    cv2.imwrite("Imshow_1660MHz.jpg", img)
    cv2.waitKey(0)

    #plt plot
    plt.scatter(power, bins, c=hists, s=4)
    #plt.title(str(f*10))
    plt.xlabel("RF Transmitter Power [dB]")
    plt.ylabel("Normalised Voltage [-]")
    #plt.show()
    f+=1