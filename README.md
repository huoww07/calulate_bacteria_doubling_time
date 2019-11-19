# calulate_bacteria_doubling_time
Calculate bacteria doubling time from growth curve using fitted curve of sigmoid function

## Table of Contents
  1. Installation
  2. Project motivation
  3. File description
  4. Summary
  5. Licensing, Authors, Acknowledgements

## Installation
The package can be installed via pip:
pip install .

## Project motivation
Bacteria doubling time is usually calculated by first measuring OD600nm absorbance and then plot the log2(OD600nm) readings against the time. The doubling time represents the time bateria takes to double their amount in cell number when they are within exponential growth phase. Once the log2(OD600nm)-time was plotted, the doubling time was calculated using two points in the most linear portion by using log2(OD2/OD1)/(T2-T1). Where OD2 is from time 2 or T2 and OD1 is from time 1 or T1.

However, the measurement of OD600nm often has variations and simply taking two time points might skew the final result. Here, I introduced a method to fit the growth curve (OD600nm against time plot) with modified sigmoid function and calculate the doubling time as the first derivative at sigmoid's midpoint. For more information regarding using sigmoid function to model population growth, please visit https://en.wikipedia.org/wiki/Logistic_function.

## File description
setup.py : used for pip installation
(to be continued)
