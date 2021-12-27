import glob
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
from scipy.optimize import curve_fit

directory2 = "./Data_24_12_Run2/"
directory = "./Data_24_12_Run1/"
shapiro_files = glob.glob(directory + "*")
shapiro_files2 = glob.glob(directory2 + "*")
for i in shapiro_files2:
    shapiro_files.append(i)
indexx = len(directory)
shapiro_list = []

for i in shapiro_files:
    j = i[indexx:]
    if j[0] == "S":
        shapiro_list.append(j)

freq = []
power = []
for i in shapiro_list:
    stuff = i.split("_")
    power.append(float(stuff[-1]))
    freq.append(float(stuff[1].split("q")[1]))

plt.scatter(power,freq)
plt.xlabel("Power [dB]")
plt.ylabel("Frequency [MHz]")
plt.show()
'''
plt.hist2d(power, freq, (20,80), cmap=plt.cm.jet)
plt.colorbar()
plt.show()

idx = Counter(power)
lists = sorted(idx.items()) # sorted by key, return a list of tuples
x, y = zip(*lists) # unpack a list of pairs into two tuples

plt.scatter(x, y)
plt.show()'''

keydict = dict(zip(freq, power))
freq.sort(key=keydict.get)

idx = np.argsort(power)
freq = np.array(freq)[idx]
power = np.array(power)[idx]

average_freqstep = []
power_freqstep = []
prev_power = 0
prev_freq = 0
count = 0
sum_tot = 0
indexs = 0

def line(x,a,b):
    return a*x+b

for i in power:
    if (i == prev_power) and (i>-19 and abs(freq[indexs]-prev_freq)>100):
        count += 1
        sum_tot += abs(freq[indexs]-prev_freq)
        prev_freq = freq[indexs]
    elif i == prev_power and i>-19 and abs(freq[indexs]-prev_freq)>800:
        count +=0
    else:
        if count != 0:
            average_freqs = sum_tot/count
            average_freqstep.append(average_freqs)
            power_freqstep.append(prev_power)
        else:
            average_freqs = 0
        count = 0
        sum_tot = 0
    prev_power = i
    indexs+=1

param, cov = curve_fit(line, power_freqstep, average_freqstep)
x2 = np.linspace(np.min(power_freqstep),np.max(power_freqstep),1000)
y2 = line(x2, *param)
plt.plot(x2, y2)
plt.scatter(power_freqstep, average_freqstep)
plt.show()
