# Calulate bacteria doubling time
Calculate bacteria doubling time from growth curve using fitted curve of sigmoid function. For web based acesss, please visit https://flask-double-time.herokuapp.com/. No installation is required for web based access.

## Table of Contents
  1. Installation
  2. Project motivation
  3. File description
  4. Licensing

## Installation
For local usage, the code runs with Python version **3**.

Required libraries:
numpy, pandas, pylab, scipy, os


## Project motivation
Bacteria doubling time is usually calculated by first measuring OD600nm absorbance and then plot the log2(OD600nm) readings against the time. The doubling time represents the time bateria takes to double their amount in cell number when they are within exponential growth phase. Once the log2(OD600nm)-time was plotted, the doubling time was calculated using two points in the most linear portion by using log2(OD2/OD1)/(T2-T1). Where OD2 is from time 2 or T2 and OD1 is from time 1 or T1.

However, the measurement of OD600nm often has variations and simply taking two time points might skew the final result. Here, I introduced a method to fit the growth curve (OD600nm against time plot) with modified sigmoid function and calculate the doubling time as the first derivative at sigmoid's midpoint. For more information regarding using sigmoid function to model population growth, please visit https://en.wikipedia.org/wiki/Logistic_function.

## File description
1. Growth_curve folder contains:

  a. cal.double.time.curve.fit.py: run with python version 3. This file is all you need for local usage.
  
  b. input_template: modify the min and hour according to experimental design; add as many sample names as needed and fill in OD600nm reading results.
  
  c. terminal look: what it looks like on your terminal after successful run of the code. It will first ask you the input file name, please paste the file name here. Then it will ask if you want to see the growth curve plotted out together with fitted curve, say 'yes/no'. Lastly, it will ask if you want to save the doubling time in a file, enter the file name if you want it to be save or press enter to skip otherwise.
  
  d. two pdf files: if you asked to see the growth curve plots, these will be what they look like

2. Doublint_time_Modularized folder contains the program in modularized form:

  a. setup.py : used for pip installation (to be used with Doubling_time_Modularized)
  
  b. Doubling_time.py: modularized python package to calculate doubling time.
  
  c. input_template2: provides template for input data, similar with the scenario above.
  
  To run without installing, save the Doubling_time.py in the working directory with data file. And run below:
    from Doubling_time import GrowthCurve
    test = GrowthCurve()
    test.read_data('input_template2.xlsx')
    test.fit_sigmoid()    # adding plot=True would enable onscreen plot
    test.show_result()    # this would print the result in a table on screen
    test.save_result('result.xlsx')   # just make sure the extension is xlsx
    
  d. Required libraries: pandas, numpy, pylab, scipy
  
  e. user_manual: contains all methods and attributes in the module.

## Licensing
Licensing: MIT license.