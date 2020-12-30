import pandas as pd
import numpy as np
import pylab
from scipy.optimize import curve_fit

class GrowthCurve:
    """
    Run samples:
        import Doubling_time
        data = Doubling_time.GrowthCurve()
        data.read_data("/Users/Wenwen/Downloads/20200707.xlsx")
        data.fit_sigmoid(plot=True)
        data.show_result()
        data.save_result("20200707_doubling_time.xlsx")
    """
    def __init__(self, data=None, doubling_time=None, \
                r2=None, max_growth_time=None):
        self.data = pd.DataFrame()
        self.doubling_time = pd.DataFrame()
        self.r2 = pd.DataFrame()
        self.max_growth_time = pd.DataFrame()

    def read_data(self, data_file):
        '''
        Read data file from Excel file
        Return data frame with time (min) and OD readings
        '''
        data = pd.read_excel(data_file)
        data_od = data.iloc[:,2:]
        data_od_log = np.log(data_od) / np.log(2)
        data_transform = pd.concat([data.iloc[:, :2], data_od_log], axis=1)
        self.data = data_transform
        strain_name = data.columns[2:]
        self.strain_name = strain_name
        print('Import data successful!')
        print('Input samples are: ' + ','.join(strain_name))

    #define sigmoid function and linear function
    def sigmoid(self, x, x0, k, L1, L2):
        y = (L1 / (1 + np.exp(-k*(x-x0)))) -L2
        return y
    def linear(self, x, a, b):
        y = a*x +b
        return y
    #define r_square function
    def r_square(self, y_true, y_predict):
        SStotal = np.sum((y_true - np.mean(y_true)) ** 2)
        SSresidual = np.sum((y_predict - y_true) ** 2)
        r2 = 1 - SSresidual/SStotal
        return r2

    def fit_sigmoid(self, plot=False):
        #initialize slope table and rsq table
        doubling_time = np.zeros(self.data.shape[1])
        r2_all = np.zeros(self.data.shape[1])
        max_growth_time = np.zeros(self.data.shape[1])
        strain_name = list(self.data.columns[2:])
        #loop through column
        for strain in range(2, self.data.shape[1]):
            ydata = np.array(self.data.iloc[1:, strain])
            #column 1 is time in hours, row 1 is 0 hrs
            xdata = np.array(self.data.iloc[1:, 1])
            #set p0 to avoid going to local minimal
            popt, pcov = curve_fit(self.sigmoid, xdata, ydata, p0=[1,1,9,8], 
                                                 bounds=(0, [10, 10, 30, 30]))
            #print(strain_name[strain-2], popt)
            #popt[0] is midpoint
            x0 = popt[0]
            max_growth_time[strain] = x0
            e = max(xdata) / 1000
            #calculate slope using a small change of y around midpoint
            y2 = self.sigmoid(x0 + e, *popt)
            y1 = self.sigmoid(x0 - e, *popt)
            y0 = self.sigmoid(x0, *popt)
            doubletime = 2*e*60 / (y2-y1)   #doubletime in minutes
            doubling_time[strain] = doubletime
            #calculate fit curve
            x = np.linspace(-6, 12, 120)
            y = self.sigmoid(x, *popt)
            #y_derivative = sigmoid_derivative(x, *popt)
            #calculate r square
            x_test=np.array(self.data.iloc[:,1])
            y_test=np.array(self.data.iloc[:,strain])
            y_fit = self.sigmoid(x_test, *popt)
            r_square = self.r_square(y_test, y_fit)
            r2_all[strain] = r_square
            #plot
            if plot:
                #calculate slope
                x_linear_data = np.array([x0-e, x0, x0+e])
                y_linear_data = np.array([y1, y0, y2])
                popttt, pcovvv = curve_fit(self.linear, \
                                           x_linear_data, y_linear_data)
                xtt = np.linspace(x0 - x0/2, x0 + x0/2, 4)
                ytt = self.linear(xtt, *popttt)
                #plot
                pylab.plot(np.array(self.data.iloc[:, 1]), np.array(self.data.iloc[:, strain]), 'o', label='data')
                pylab.plot(x,y, label='fit')
                #pylab.plot(x,y_derivative,label='derivative')
                pylab.plot(xtt,ytt, label='slope:'+ str('%.3f' % popttt[0]))
                pylab.xlim(-6,12)
                pylab.xlabel('Time in hrs')
                pylab.ylabel('Log2 transformed OD600nm')
                pylab.legend(loc='best')
                pylab.title(strain_name[strain-2])
                #pylab.savefig('%s.png' % strain_name[strain-2])
                pylab.show()
        self.r2 = r2_all[2:]
        self.max_growth_time = max_growth_time[2:]
        self.doubling_time = doubling_time[2:]

    def show_result(self, sort_name=False):
        result_zip = list(zip(self.strain_name, self.doubling_time, \
                              self.max_growth_time,self.r2))
        col_names=['strain','doubling time (min)', \
                   'max growth time point (hr)','r2 square']
        result = pd.DataFrame(result_zip, columns=col_names)
        if sort_name:
            result.sort_values(by=['strain'], inplace=True)
        self.result = result
        return result

    def save_result(self, output_file):
        try:
            self.result.to_excel(output_file, header=True, \
                                index=False,float_format="%.3f")
            print("Results saved. Good day!")
        except:
            print('Can not save result to file!')
