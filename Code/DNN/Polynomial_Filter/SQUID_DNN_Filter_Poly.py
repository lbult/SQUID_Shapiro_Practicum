import pickle
import pandas as pd
import glob
import os
from DNN.Test.support_func import clean_dataset

not_shapiro_files = glob.glob("./Data_24_12_Run3/*")
print(len(not_shapiro_files))

x = pd.read_csv('training_inputs_deux.csv', delimiter=',')

# take away any infinities and NaN, gather clean lists
x = clean_dataset(x)
xlabels = x.columns

#format the data
X = []
m = 0
for i in xlabels:
    X.append(x[xlabels[m]].to_list())
    m+=1

# load and execute the model from file
filename = 'poly_model_v4.sav'
indexx = 0
loaded_model = pickle.load(open(filename, 'rb'))
for i in X:
    shap = loaded_model.predict([i])
    print(shap)
    print(indexx)
    if shap[0] != 1:
        os.remove(str(not_shapiro_files[indexx]))
        print("Delete file")
    indexx += 1