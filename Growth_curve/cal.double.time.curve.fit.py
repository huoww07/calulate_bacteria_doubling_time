import os


# take input file name through prompt
# please make sure the file is in the same directory with this script
file_name = input("Please enter your file name: ") # example response: input_template.xlsx
plot_option = input('Do you want to generate the growth curve? ') # yes/no
file_path = os.path.dirname(__file__)
input_file = os.path.join(file_path, file_name)
try:
                output_name = input('Output file name: ')
                output_file = os.path.join(file_path, output_name)
except:
                print('skipping output file')


print("Input file: " + input_file)
print("Calculating doubling time...")

import pandas as pd
import numpy as np
import pylab
from scipy.optimize import curve_fit


def cal_slope(time, generation):
                time_mean = np.mean(time)
                generation_mean = np.mean(generation)
                top = 0
                bottom = 0
                for i in range(len(time)):
                                new_top = (time[i] - time_mean) * (generation[i] - generation_mean)
                                top += new_top
                                new_bottom = (generation[i] - generation_mean)**2
                                bottom += new_bottom
                slope = top / bottom
                return slope


def cal_rsq(time, generation):
                time_mean = np.mean(time)
                generation_mean = np.mean(generation)
                top =0
                bottom_one=0
                bottom_two=0
                for i in range(len(time)):
                                new_top = (time[i] - time_mean) * (generation[i] - generation_mean)
                                top += new_top
                                new_bottom_one = (time[i] - time_mean)**2
                                bottom_one +=new_bottom_one
                                new_bottom_two = (generation[i] - generation_mean)**2
                                bottom_two +=new_bottom_two
                bottom = np.sqrt(bottom_one * bottom_two)
                rsq = top / bottom
                return rsq


#test def functions
x=(1, 2, 3, 4, 5)
y=(5, 6, 7, 8, 9)
assert cal_slope(x,y) == 1
assert cal_rsq(x,y) == 1


#define sigmoid function
def sigmoid(x, x0, k, L1, L2):
    y = (L1 / (1 + np.exp(-k*(x-x0)))) -L2
    return y
def sigmoid_x(y, x0, k, L1, L2):
    x = x0 - (np.log(L1-y-L2) - np.log(y+L2))/k
    return x
def linear(x, a, b):
    y = a*x +b
    return y
#define sigmoid derivative
def sigmoid_derivative(x, x0, k, L1, L2):
                y = k*L1*np.exp(-k*x)*((1 + np.exp(-k*(x-x0)))**(-2))
                return y

#define mean square error function
def mse(y_test, y_fit):
	total = 0
	total = np.sum((y_test - y_fit) * (y_test-y_fit)) / len(y_test)
	return total

#read csv file
data = pd.read_excel(input_file)
#transform data into log(OD)/log(2), default 1st column is time in minutes, 2nd column is time in hours
data_od = data.iloc[:,2:]
data_od_log = np.log(data_od) / np.log(2)
data_transform = pd.concat([data.iloc[:, :2], data_od_log], axis=1)

#initialize slope table and rsq table
doubling_time = np.zeros(data.shape[1])
mse_all = np.zeros(data.shape[1])
max_growth_time = np.zeros(data.shape[1])
strain_name = data.columns[2:]
#loop through column
for strain in range(2, data.shape[1]):
                ydata = np.array(data_transform.iloc[1:, strain])
                xdata = np.array(data_transform.iloc[1:, 1])  #column 1 is time in hours, row 1 is 0 hrs
                popt, pcov = curve_fit(sigmoid, xdata, ydata, p0=[2,1,9,8]) #set p0 to avoid going to local minimal
                print(popt)
                #previously, was using x_median and y_median to calculate doubling time
                #y_median = -popt[-1]/2
                #x_median = sigmoid_x(y_median, *popt)
                x0 = popt[0]
                max_growth_time[strain]=x0
                e = max(xdata) / 1000
                #previously, was using x_median and y_median to calculate doubling time
                #y2 = sigmoid(x_median+e, *popt)
                #y1 = sigmoid(x_median-e, *popt)
                y2 = sigmoid(x0 + e, *popt)
                y1 = sigmoid(x0 - e, *popt)
                y0 = sigmoid(x0, *popt)
                doubletime = 2*e*60 / (y2-y1)   #doubletime in minutes
                doubling_time[strain] = doubletime
                #calculate fit curve
                x = np.linspace(0, 12, 120)
                y = sigmoid(x, *popt)
                #y_derivative = sigmoid_derivative(x, *popt)

                #calculate mean square error
                x_test=np.array(data_transform.iloc[:,1])
                y_test=np.array(data_transform.iloc[:,strain])
                y_fit = sigmoid(x_test, *popt)
                mse_value = mse(y_test, y_fit)
                mse_all[strain] = mse_value

                #calculate slope
                #x_linear_data = np.array([x_median-e, x_median, x_median+e])
                #y_linear_data = np.array([y1, y_median, y2])
                x_linear_data = np.array([x0-e, x0, x0+e])
                y_linear_data = np.array([y1, y0, y2])
                popttt, pcovvv = curve_fit(linear, x_linear_data, y_linear_data)
                xtt = np.linspace(x0 - x0/2, x0 + x0/2, 4)
                ytt = linear(xtt, *popttt)
                #xtt = np.linspace(x_median - x_median/2, x_median + x_median/2, 4)
                #ytt = linear(xtt, *popttt)

                #plot
                if plot_option in ['yes', 'y', 'Y', 'Yes', 'YES']:
                    pylab.plot(xdata, ydata, 'o', label='data')
                    pylab.plot(x,y, label='fit')
                    #pylab.plot(x,y_derivative,label='derivative')
                    pylab.plot(xtt,ytt, label='slope:'+ str('%.3f' % popttt[0]))
                    pylab.xlabel('Time in hrs')
                    pylab.ylabel('Log2 transformed OD600nm')
                    pylab.legend(loc='best')
                    pylab.title(strain_name[strain-2])
                    #pylab.savefig('%s.png' % strain_name[strain-2])
                    pylab.show()
print('Doubling time results:')
for i in range(len(strain_name)):
                print('%s : %.3f min' % (strain_name[i], doubling_time[i+2]))
                print('Mean square error durint %s fitting: %.3f' % (strain_name[i], mse_all[i+2]))
print('Saving to file...')
result_zip = list(zip(strain_name, doubling_time[2:], max_growth_time[2:],mse_all[2:]))
col_names=['strain','doubling time','max growth time point','mean square error']
result = pd.DataFrame(result_zip, columns=col_names)
result.sort_values(by=['strain'], inplace=True)
print(result)
try:
                result.to_excel(output_file, header=True, index=False,float_format="%.3f")
except:
                print('No output file saved!')
print("Calculation done. Good day!")
