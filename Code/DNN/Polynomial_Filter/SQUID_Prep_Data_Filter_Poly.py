from os import defpath
import pandas as pd
import glob
from scipy.optimize import curve_fit
from sklearn import preprocessing

def ShapiroFunc(x,a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p):
    return a + b*x + c*x**2 + d*x**3 + e*x**4 + f*x**5 + g*x**6 + h*x**7 + i*x**8 # + j*x**9 + k*x**10 + l*x**11 + m*x**12 + n*x**13 + o*x**14 + p*x**15

#load and plot IV curves files
shapiro_files = glob.glob("./Data_24_12_Run3/*")

#define training sets
shapiro_input = []

for i in shapiro_files: #replace shapiro_files by not_shapiro_files
    df = pd.read_csv(i, sep=" ")
    #find data labels
    labels = df.columns
    # load t, I, V
    t = df[labels[0]]
    t = t[:5000]
    I = df[labels[1]]
    I = I[:5000]
    V = df[labels[2]]
    V = V[:5000]
    V = V * 0.1 # scale voltage data 
    
    # for each bit of data save the parameters of the polynomial expansion
    param, cov = curve_fit(ShapiroFunc, I, V)
    param = preprocessing.minmax_scale(param, feature_range=(-1, 1), axis=0, copy=True)
    params = []
    for i in param:
        params.append(i)
    shapiro_input.append(params)

shapiro_input = pd.DataFrame(shapiro_input)
shapiro_input = shapiro_input.T

shapiro_input.to_csv('training_inputs_deux.csv', index = False, header= False)