# calulate_bacteria_doubling_time
Calculate bacteria doubling time from growth curve using fitted curve of sigmoid function

## Table of Contents
  1. Installation
  2. Project motivation
  3. File description
  4. Summary
  5. Licensing

## Installation
The code runs with Python version **3**.

Required libraries:
numpy, pandas, pylab, scipy, os


## Project motivation
Bacteria doubling time is usually calculated by first measuring OD600nm absorbance and then plot the log2(OD600nm) readings against the time. The doubling time represents the time bateria takes to double their amount in cell number when they are within exponential growth phase. Once the log2(OD600nm)-time was plotted, the doubling time was calculated using two points in the most linear portion by using log2(OD2/OD1)/(T2-T1). Where OD2 is from time 2 or T2 and OD1 is from time 1 or T1.

However, the measurement of OD600nm often has variations and simply taking two time points might skew the final result. Here, I introduced a method to fit the growth curve (OD600nm against time plot) with modified sigmoid function and calculate the doubling time as the first derivative at sigmoid's midpoint. For more information regarding using sigmoid function to model population growth, please visit https://en.wikipedia.org/wiki/Logistic_function.

## File description
setup.py : used for pip installation (to be continued)
Growth_curve folder contains:
1. cal.double.time.curve.fit.py: run with python version 3
2. input_template: modify the min and hour according to experimental design; add as many sample names as needed and fill in OD600nm reading results.
3. terminal look: what it looks like on your terminal after successful run of the code. It will first ask you the input file name, please paste the file name here. Then it will ask if you want to see the growth curve plotted out together with fitted curve, say 'yes/no'. Lastly, it will ask if you want to save the doubling time in a file, enter the file name if you want it to be save or press enter to skip otherwise.
4. two pdf files: if you asked to see the growth curve plots, these will be what they look like

## Summary
(to be continued)

## Licensing
Licensing: MIT license. Acknowledgement would be appreciated.
