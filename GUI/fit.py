import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import xlrd
import os

import GUI.Library as Library


def fit(sheet, TID_level, file_path):
    Ve, Ib_Pre_Rad = excel_table_byname(sheet, TID_level, file_path)
    xdata = np.array(Ve)
    ydata = np.array(np.log(Ib_Pre_Rad))
    popt, pcov = curve_fit(func, xdata, ydata)
    # plot_data(xdata, ydata, popt)
    # y2 = np.array(Ib_Pre_Rad)
    # plot_log_scale(xdata, y2, popt)
    return popt

def relative_path(path):
    dirname = os.path.dirname(os.path.realpath('__file__'))
    path = os.path.join(dirname, path)
    return os.path.normpath(path)

def get_titles(table):
    col_dict = {}
    for i in range(table.ncols):
        title = table.cell_value(1,i)
        if title != '':
            col_dict[title] = i
    return col_dict


def excel_table_byname(sheet, TID_level, file_path='FitCurve/Fit_Curve.xlsx'):
    file = relative_path(file_path)
    data = xlrd.open_workbook(file)
    table = data.sheet_by_name(Library.SHEET_NAME[sheet])

    Ve = []
    Ib = []
    nrows = table.nrows
    col_dict = get_titles(table)
    for row in range(2, nrows):
        ve = table.cell(row,col_dict[Library.COL_NAME['VE']]).value
        ib = table.cell(row, col_dict[Library.COL_NAME[TID_level]]).value
        if 0.3 <= ve <= 0.7 and ib > 0:
            Ve.append(ve)
            Ib.append(ib)
    return Ve, Ib


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
    # plt.plot(xdata, f(xdata, -41.935,47.6314,-11.045), 'y-', label='fit:a=-41.935, b=47.6314, c=-11.045')

    plt.yscale('log')
    plt.legend(loc='upper left')
    plt.show()
    return


def func(x, a, b, c):
    return a + b * x + c * x**2


def f(x, a, b, c):
    return np.exp(a + b * x + c * x**2)
