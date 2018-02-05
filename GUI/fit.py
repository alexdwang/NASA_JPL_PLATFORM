import numpy as np
import matplotlib.pyplot as plt
import xlrd
from scipy.optimize import curve_fit


def fit():

    return

def get_titles(table):
    col_dict = {}
    for i in range(table.ncols):
        title = table.cell_value(1,i)
        if title != '':
            col_dict[title] = i
    return col_dict


def excel_table_byname(file='../FitCurve/Fit_Curve.xlsx'):
    data = xlrd.open_workbook(file)
    table_npn = data.sheet_by_name('NPN_FIT_Xyce')
    table_pnp = data.sheet_by_name('PNP_FIT_Xyce')

    Ve = []
    Ib_Pre_Rad = []
    nrows = table_npn.nrows
    col_dict = get_titles(table_npn)
    for row in range(2, nrows):
        ve = table_npn.cell(row,col_dict['Ve_PRE_RAD']).value
        if 0.3 <= ve <= 0.7:
            Ve.append(ve)
            Ib_Pre_Rad.append(table_npn.cell(row,col_dict['Ib_Pre_Rad']).value)
    return Ve, Ib_Pre_Rad


def plot_data(xdata, ydata, popt):
    plt.figure(1)
    plt.plot(xdata, ydata, 'b*', label='data')
    plt.plot(xdata, func(xdata, *popt), 'r-', label='fit:a=%5.3f, b=%5.3f, c=%5.3f' % tuple(popt))
    plt.legend()
    plt.show()
    return


def plot_log_scale(xdata, y2, popt):
    plt.subplot()
    plt.plot(xdata, y2, 'b*', label='data')
    plt.plot(xdata, f(xdata, *popt), 'r-', label='fit:a=%5.3f, b=%5.3f, c=%5.3f' % tuple(popt))
    plt.plot(xdata, f(xdata, -41.935,47.6314,-11.045), 'y-', label='fit:a=-41.935, b=47.6314, c=-11.045')

    plt.yscale('log')
    plt.legend(loc='upper left')
    plt.show()
    return


def func(x, a, b, c):
    return a + b * x + c * x**2


def f(x, a, b, c):
    return np.exp(a + b * x + c * x**2)

Ve, Ib_Pre_Rad = excel_table_byname()
xdata = np.array(Ve)
ydata = np.array(np.log(Ib_Pre_Rad))
popt, pcov = curve_fit(func, xdata, ydata)
# plot_data(xdata, ydata, popt)
y2 = np.array(Ib_Pre_Rad)
plot_log_scale(xdata, y2, popt)
