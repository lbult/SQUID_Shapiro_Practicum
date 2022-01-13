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

# linear function
def func(x,a,b):
    return a*x+b

def ShapiroFunc(x,a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q):
    return a + b*x + c*x**2 + d*x**3 + e*x**4 + f*x**5 + g*x**6 + h*x**7 + i*x**8 + j*x**9 + k*x**10 + l*x**11 + m*x**12 + n*x**13 + o*x**14 + p*x**15 + q*x**16

#load and plot IV curves files
dir = "./Data_24_12_Run1_Full/"
dir = "./New_Training_Shap/"
files = ["./New_Training_Shap\Shapiro_freq2111.1111111111113_power_-13.0"]
#files = ["./Data_24_12_Run1_Full/Shapiro_freq1640.0_power_-7.0"]

"""
Exp                     Pred
6.115784171814094e-06 4.887652035539202e-06 2363.636363636364Hz ./Training_Shap\Shapiro_freq2363.636363636364_power_-10.0
4.287667317427189e-06 4.365466989007236e-06 2111.1111111111113MHz ./Training_Shap\Shapiro_freq2111.1111111111113_power_-13.0
3.311896038487763e-06 3.2166598866369103e-06 1555.5555555555557Mhz ./Training_Shap\Shapiro_freq1555.5555555555557_power_-14.0
4.05427764624777e-06 4.900811098711807e-06 2370.0MHz ./Data_24_12_Run1_Full\Shapiro_freq2370.0_power_-12.0
3.110094708501369e-06 2.502101868962568e-06 1210.0Mhz ./Data_24_12_Run1_Full/Shapiro_freq1210.0_power_-14.0 [500:3000]
2.8138013337849888e-06 2.9983865371865486e-06 1450.0Mhz ./Data_24_12_Run1_Full\Shapiro_freq1450.0_power_-2.0 [1600:4600]
3.2668074659962633e-06 3.246528871298539e-06 1570.0Mhz ./Data_24_12_Run1_Full\Shapiro_freq1570.0_power_-14.0 [1600:4600]
2.694686583560705e-06 3.0397435928718803e-06 1470.0Mhz ./Data_24_12_Run1_Full\Shapiro_freq1470.0_power_-8.0 [600:2700]
3.11663456050873e-06 3.3912785661972e-06 1640.0MHz ./Data_24_12_Run1_Full\Shapiro_freq1640.0_power_-7.0 [1500:3865]
3.3777108929421115e-06 3.4326356218825316e-06 1660.0MHz ./Data_24_12_Run1_Full/Shapiro_freq1660.0_power_-8.0 [:4500]
3.411996848849081e-06 3.494671205410529e-06 1690.0MHz ./Data_24_12_Run1_Full/Shapiro_freq1690.0_power_-9.0 [:4500]
3.5520232916290446e-06, 3.5567067889385267e-06, 1720.0MHz ./Data_24_12_Run1_Full/Shapiro_freq1720.0_power_-9.0 [:5000]

Width of the shapiro steps, that varies with RF power, makes it difficult to consistently get good results
with the current method of data gathering

Candidates: ./Data_24_12_Run2\Shapiro_freq4670.0_power_-4.0", "./Data_24_12_Run2\Shapiro_freq4300.0_power_-7.0, ./Data_24_12_Run2\Shapiro_freq4790.0_power_-11.0
"./Data_24_12_Run1\Shapiro_freq2230.0_power_-8.0", "./Data_24_12_Run1\Shapiro_freq1750.0_power_-17.0" ./Data_24_12_Run1\Shapiro_freq1470.0_power_-1.0
"""


#define training sets
shapiro_input = []

for i in files: 
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
        # load t, I, V
        I = df[labels[1]]
        V = df[labels[2]]
        #I = I[500:3000]
        #V = V[500:3000]
        V = 0.1*V

        on1 = False
        on2 = True
        count = 0 
        V_new = []
        I_new = []
        for g in range(0, len(I)):
            if g+1 < len(I):
                if I[g] < 100 and I[g] > -150 and on1 and on2:
                    V_new.append(V[g])
                    I_new.append(I[g]) 
                    count+=1
                if I[g+1] <= -150 and I[g] > -150:
                    on1 = True
                if I[g+1] <= 100 and I[g] > 100 and on1:
                    on1 = False
                    on2 = False
        V = V_new
        I = I_new

        param, cov = curve_fit(func, I, V)
        x1 = np.linspace(np.min(I),np.max(I),1000)
        y = func(x1, *param)

        param2, cov2 = curve_fit(ShapiroFunc, I, V)
        x2 = np.linspace(np.min(I),np.max(I),1000)
        y2 = ShapiroFunc(x2, *param2)

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
                #if i <= V_new[j-1] and i <= V_new[j+1]:
                #    indx = V_new.index(i)
                #    V_list.append(y2[indx])
            j+= 1
        
        #V_list = V_list[0:2]
        #V_list[0] = V_list[0]  + 0
        #V_list[1] = V_list[1] + .5
        #print(abs(V_list[1]-V_list[0])/2)

        prev_v = 0
        if len(V_list) == 2:
            count = 1
        else:
            count = 0
        
        V_list = V_list[:]
        tot_sum = 0
        for m in V_list:
            if count != 0:
                plt.axhline(y=m, color='r', linestyle='--')
                tot_sum += abs(m-prev_v)
                prev_v = m
            count += 1
        step = tot_sum/count
        print(step*10**-6, freq*10**6/(2*2.4179671*10**14), freq)
        print(V_list)
        #plt.plot(x1,y, linewidth=1, color='r')
        plt.plot(x1,y2, linewidth=1, color='b')
        plt.scatter(I, V, s=0.05)
        #plt.title("IV-curve at f = "+ str(freq) + " Hz, power = " + str(power) + " dB")
        plt.xlabel("Current [\u03bcA]")
        plt.ylabel("Voltage [\u03bcV]")
        plt.show()