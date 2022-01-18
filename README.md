# SQUID_Shapiro_Practicum
Code written for the course Research Project for the Minor (Modern Physics)
Programmed by Lennart Bult and Bram Wagemakers

Before running a script, make sure that the correct file directory is specified. If you want more data to make graphs, please contact us.


------------------------------ ------------------------------ ------------------------------
All code written for this project can be found in the Code folder. It is divided into three different folders.
The DNN folder contains all code required to train and execute the neural networks. 
1. > Polynomial_Filter: the polynomial filter data preparation generates a polynomial approximation
of the IV curve, its coefficients are used as input in the neural network.
2. > MLP_DNN: this map contains all code required to prepare data, train the MLP model, and subsequently filter data.
3. > Test: this contains a support file in addition to a file to test DNN performance on a training set.

The eh_analysis folder contains again the support function script, a method to calculate the mean, std and uncertainty for a given amount of
Shapiro step data (calc_he.py), and a file which plots IV curves and histograms side-by-side (analyse_steps.py).

The graphs generation folder contains a script to combine histograms at different powers of one frequency (comb_hist.py), a script to click through IV curves
or select data for DNN training (SQUID_GenGraph.py), Freq_Pow_Shap.py creates a 2D histogram using the files names specified (it selects the power and frequency 
in their file names), and histogram_plot.py generates a histogram of multiple IV curves for all powers selected.
------------------------------ ------------------------------ ------------------------------
The Data folder:
Train_Shap and Train_NotShap contains data for the 330 input nodes DNN. 
Selected_Shapiro contains data selected by the 330 input nodes DNN.

Training_Shap and Training_NotShap contains data for the 8000 input nodes DNN and the polynomial DNN.
Filtered_Data containsd data selected by the 8000 input nodes DNN and the polynomial DNN.
------------------------------ ------------------------------ ------------------------------
The models folder contains trained models. Their training performance can be seen in the report written for this course.
------------------------------ ------------------------------ ------------------------------
The photos folder contains interesting plots of IV curves and their corresponding histograms. 
It can be seen that the theoretical Shapiro step lines match the steps observed.
------------------------------ ------------------------------ ------------------------------
The folder Plots contains some misc/interesting plots.
