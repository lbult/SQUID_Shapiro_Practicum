import os
import glob
import matplotlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, Button, Frame
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import re
import shutil
from matplotlib.tri import Triangulation

#load and plot IV curves files
#files = glob.glob("./alg_data/*.csv")
#files = glob.glob("./Training_Shap/*")
files = glob.glob("./Data_24_12_Run2_Full_copy\Shapiro_freq3010*")
#files = glob.glob("./Data_24_12_Run1_Full\Shapiro_freq1550.0_power_0.0")

def move_to_notshapiro(file):
    plt.close()
    string = re.sub(r'[\W]', " ", file)
    string = file.split("/")
    string = string[-1].split("\\")
    if len(string) == 2:
        shutil.move("./"+string[0]+"/"+string[1], "./Train_NotShap/" + str(string[-1]))
    else:
        shutil.move(file, "./Train_NotShap/" + str(string[-1]))

def move_to_shapiro(file):
    plt.close()
    string = re.sub(r'[\W]', " ", file)
    string = file.split("/")
    string = string[-1].split("\\")
    if len(string) == 2:
        shutil.move("./"+string[0]+"/"+string[1], "./Train_Shap/" + str(string[-1]))
    else:
        shutil.move(file, "./Train_Shap/" + str(string[-1]))

def remove(file):
    plt.close()
    os.remove(file)

def nothing(file):
    plt.close()

class createButton:
    def __init__(self, master, funcs, text, keybind, grid):
       self.button = Button(master, text=text, command=funcs).grid(row=1,column=grid) 
       #self.button.pack(side='left')

class Render():
    def __init__(self, files):
        self.files = files
        self.file = []

    def press(self, event):
        print('press', event.key)
        if event.key == 'y':
            move_to_shapiro(self.file)
            print("Has been moved to Shapiro")
        if event.key == 'n':
            move_to_notshapiro(self.file)
            print("Has been moved to Not Shapiro")
        if event.key == 'r':
            remove(self.file)
            print("Has been removed")
        if event.key == 'h':
            nothing(self.file)
            print("Doing nothing")
    
    def Run(self):
        for i in self.files:
            self.file = i
            fig,ax = plt.subplots()
            matplotlib.use('TkAgg')
            #canvas = FigureCanvasTkAgg(fig, master=root)
            #plot_widget = canvas.get_tk_widget()
            #plot_widget.grid(row=0,column=0)
            df = pd.read_csv(i, sep=" ")
            
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
            bounds = [0,30]
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

            fig.canvas.mpl_connect('key_press_event', self.press)
            ax.scatter(I, V, s=0.05, color='red')
            freqw = 1555

            #for m in range(0,5):
            #     plt.axhline(y=(10*(m-1)*freqw*10**12/(2*2.4179671*10**14)), color='black', linestyle='--', linewidth=0.7)
            #plt.title("IV-curve") # at f = 1440 Hz, power = -3.2d B")
            #plt.xlabel("Current" + i)
            print(i)
            plt.xlabel("Current [\u03bcA]")
            plt.ylabel("Voltage [\u03bcV]")
            plt.show()
        #B = Button(root,  text="Not Shapiro", command= lambda i=i: move_to_notshapiro(i)).grid(row=1,column=0)
        #C = Button(root,  text="Shapiro", command= lambda i=i: move_to_shapiro(i)).grid(row=1,column=1)
        #D = Button(root, text="Remove", command= lambda i=i: remove(i)).grid(row=1,column=2)
        #E = Button(root, text="Nothing", command= lambda i=i: nothing(i)).grid(row=1,column=3) 
        #createButton(root, move_to_shapiro(i), "Shapiro", "y", 0)
        #chreateButton(root, move_to_notshapiro(i), "Not Shapiro", "n", 1)
        #createButton(root, remove(i), "Remove", "r", 2)
        #createButton(root, nothing(i), "Nothing", "h", 3)
        #root.bind("<y>", move_to_shapiro(i))
        #root.bind("<n>", move_to_notshapiro(i))
        #root.bind("<r>", remove(i))
        #root.bind("<h>", nothing(i))'
        
        #root.mainloop()

#files = glob.glob("./Data_24_12_Run2_Full/Shapiro*") 
#files = glob.glob("./Train_Shap/*") 
#files = random.sample(files, 100)
#files = files[files.index("./Data_24_12_Run2\Shapiro_freq4170.0_power_-9.0"):]
#dir = random.sample(dir, 4)

#dir = glob.glob("./Data_24_12_Run2_Full/Shapiro_freq.0_power_*")
directory = "./Data_24_12_Run2_Full_copy/"

indexx = len(directory)
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
    files.append(directory + j)
#files = files[::-1]

this = Render(files=files)
this.Run()