from os import defpath
import pandas as pd
import glob
from sklearn import preprocessing
import numpy as np

# linear function
def func(x,a,b):
    return a*x+b

# polynomial expansion
def ShapiroFunc(x,a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p):
    return a + b*x + c*x**2 + d*x**3 + e*x**4 + f*x**5 + g*x**6 + h*x**7 + i*x**8 + j*x**9 + k*x**10 + l*x**11 + m*x**12 + n*x**13 + o*x**14 + p*x**15

def jacobian(x,a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p):
    db = b
    dc = 2*c*x 
    dd = 3*d*x**2
    de = 4*e*x**3
    df = 5*f*x**4
    dg = 6*g*x**5
    dh = 7*h*x**6
    di = 8*i*x**7
    dj = 9*j*x**8
    dk = 10*k*x**9
    dl = 11*l*x**10
    dm = 12*m*x**11
    dn = 13*n*x**12
    do = 14*o*x**13
    dp = 15*p*x**14
    return np.transpose([[0*a],[db],[dc],[dd],[de],[df],[dg],[dh],[di],[dj],[dk],[dl],[dm],[dn],[do],[dp]])
    #return np.array([0*a,db,dc,dd,de,df,dg,dh,di,dj,dk,dl,dm,dn,do,dp,0,0,0,0])
#load and plot IV curves files
#not_shapiro_files = glob.glob("./Training_Data_NotShap/*.dat")
shapiro_files = glob.glob("./Data_24_12_Run3/*")

#define filter set
shapiro_input = []

for i in shapiro_files: #replace shapiro_files by not_shapiro_files
    df = pd.read_csv(i, sep=" ")
    #find data labels
    labels = df.columns
    # load t, I, V
    t = df[labels[0]]
    t = t[:8000]
    I = df[labels[1]]
    I = I[:8000]
    V = df[labels[2]]
    V = V[:8000]
    V = V * 0.1 # scale voltage data 
    
    params = []
    for i in V:
        params.append(i)
    params = preprocessing.minmax_scale(params, feature_range=(-1, 1), axis=0, copy=True)
    shapiro_input.append(params)

shapiro_input = pd.DataFrame(shapiro_input)
shapiro_input = shapiro_input.T

shapiro_input.to_csv('training_inputs_filter.csv', index = False, header= False)