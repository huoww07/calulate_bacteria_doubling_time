class doubling_time.GrowthCurve

Methods:
1.  read_data(data_file): data_file has to be xlsx format, first two columns are
time in minutes and time in hours, followed by as many samples as needed.
2.  fit_sigmoid(plot=False): fit the sigmoid function to read data.
3.  show_result: print result table to screen. With 'plot=True', the plot will be
printed on screen.
4.  save_result('result.xlsx'): save the result table in file named 'result.xlsx'.

Attributes:
1.  data: DataFrame, shape (n_time_points, n_samples+2). input data file in pandas
DataFrame float_format
2.  doubling_time: array, shape(n_samples). Calculated doubling time for each samples as input order
3.  max_growth_time: array, shape(n_samples). The time point (in hours) along the
growth curve that the doubling time was calculated, which represents the maximum growth rate.  
4.  r2: array, shape(n_samples). Calculated r-square using fitted sigmoid
function


How to run:
1.  python3
2.  // within python3 shell, run below:
3.  import Doubling_time
4.  data = Doubling_time.GrowthCurve()
5.  data.read_data("input_template2.xlsx")
6.  data.fit_sigmoid(plot=True)
7.  data.show_result()
8.  data.save_result("/Users/Wenwen/Downloads/20200707_doubling_time.xlsx")
