import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import xlrd
import os

import GUI.Library as Library
import GUI.FILEPATHS as FILEPATHS
import Main


# fit curve based on the data in database
def fit(sheet, TID_level, DR, H2, bias):
    # choose which equation we need to fit
    choice = 5
    # fit curve with 3-paras function (a + b * x + c * x^2) without log-scaled
    if choice == 1:
        Ve, Ib = excel_table_byname(sheet, TID_level, DR, H2)
        xdata = np.array(Ve)
        ydata = np.array(Ib)
        popt, pcov = curve_fit(func_eabxcx2, xdata, ydata)

        # plot_log_scale(xdata, ydata, popt, func_eabxcx2)
        return popt
    # fit curve with 3-paras function (a + b * x + c * x^2) with log-scaled
    elif choice == 2:
        Ve, Ib = excel_table_byname(sheet, TID_level, DR, H2)
        xdata = np.array(Ve)
        logged_ydata = np.array(np.log(Ib))
        popt, pcov = curve_fit(func_loged_abxcx2, xdata, logged_ydata)

        # plot_data(xdata, logged_ydata, popt, func_loged_abxcx2)
        return popt
    # fit curve with 2-paras function (a * e^(b * x)) without log-scaled
    elif choice == 3:
        Ve, Ib = excel_table_byname(sheet, TID_level, DR, H2)
        scale = 1e10
        xdata = np.array(Ve)
        ydata = np.array(Ib) * scale
        popt, pcov = curve_fit(func_aebx, xdata, ydata)

        # plot_data(xdata, ydata, popt, func_aebx)
        # plot_log_scale(xdata, ydata, popt, func_aebx)
        popt[0] = popt[0]/scale
        return popt
    # fit curve with 2-paras function (a * e^(b * x)) with log-scaled
    elif choice == 4:
        Ve, Ib = excel_table_byname(sheet, TID_level, DR, H2)
        xdata = np.array(Ve)
        logged_ydata = np.array(np.log(Ib))
        popt, pcov = curve_fit(func_loged_logabx, xdata, logged_ydata)
        # if TID_level != Library.TPRE_RAD:
        #     plot_data(xdata, logged_ydata, popt, func_loged_logabx)
        return popt
    # fit curve with 2-paras function (a * e^(b * x)) with log-scaled from the original data
    elif choice == 5:
        Ve, Delta_Ib = excel_table_byname2delta(sheet, TID_level, DR, H2, bias)
        xdata = np.array(Ve)
        logged_ydata = np.array(np.log(Delta_Ib))
        popt, pcov = curve_fit(func_loged_logabx, xdata, logged_ydata)
        # if TID_level != Library.TPRE_RAD:
        #     plot_data(xdata, logged_ydata, popt, func_loged_logabx)
        return popt

# get titles from a given table
def get_titles(table):
    col_dict = {}
    for i in range(table.ncols):
        title = table.cell_value(0,i)
        if title != '':
            col_dict[title] = i
    return col_dict

# get data from a given table, not in use in current version
def excel_table_byname(sheet, TID_level, DR, H2):
    file_path = FILEPATHS.NPN_IB_DATABASE_FILE_PATH if sheet == "NPN" else FILEPATHS.PNP_IB_DATABASE_FILE_PATH
    file = Main.relative_path(file_path)
    data = xlrd.open_workbook(file)
    table = data.sheet_by_name("DR=" + str(DR) + "_H2=" + str(H2))

    Ve = []
    Ib = []
    nrows = table.nrows
    col_dict = get_titles(table)
    lower_bound = 0.3 if sheet == "NPN" else 0.1
    upper_bound = 0.8 if sheet == "NPN" else 0.7
    for row in range(1, nrows):
        ve = table.cell(row,col_dict[Library.COL_NAME['VE']]).value
        ib = table.cell(row, col_dict[Library.COL_NAME[TID_level]]).value
        # print(ve)
        if lower_bound <= ve <= upper_bound and ib > 0:
            Ve.append(ve)
            Ib.append(ib)
    return Ve, Ib

# get data from a given table and calculate delta from pre-rad to current TID level
def excel_table_byname2delta(sheet, TID_level, DR, H2, bias):
    file_path = FILEPATHS.NPN_IB_DATABASE_FILE_PATH if sheet == "NPN" else FILEPATHS.PNP_IB_DATABASE_FILE_PATH
    file = Main.relative_path(file_path)
    data = xlrd.open_workbook(file)
    table = data.sheet_by_name("DR=" + str(DR) + "_H2=" + str(H2) + "_B=" + str(bias))

    Ve = []
    Delta_Ib = []
    nrows = table.nrows
    col_dict = get_titles(table)
    lower_bound = 0.3 if sheet == "NPN" else 0.1
    upper_bound = 0.8 if sheet == "NPN" else 0.7
    for row in range(1, nrows):
        # print(Library.COL_NAME['VE'])
        ve = table.cell(row,col_dict[Library.COL_NAME['VE']]).value
        ib_column_name = Library.COL_NAME[TID_level] if Library.COL_NAME[TID_level] is not None else TID_level + 'rad'
        ib = table.cell(row, col_dict[ib_column_name]).value
        ib_pre = table.cell(row, col_dict[Library.COL_NAME[Library.TPRE_RAD]]).value
        delta_ib = ib - ib_pre
        # print(ve)
        if lower_bound <= ve <= upper_bound and delta_ib > 0:
            Ve.append(ve)
            Delta_Ib.append(delta_ib)
    return Ve, Delta_Ib

# plot data in a graph, debugging use only
def plot_data(xdata, ydata, popt, function):
    plt.figure(1)
    plt.plot(xdata, ydata, 'b*', label='data')
    if len(popt) == 3:
        plt.plot(xdata, function(xdata, *popt), 'r-', label='fit:a=%5.3f, b=%5.3f, c=%5.3f' % tuple(popt))
    else:
        plt.plot(xdata, function(xdata, *popt), 'r-', label='fit:a=%e, b=%5.3f' % tuple(popt))
    plt.legend()
    # plt.show(block=False)
    plt.show()
    return

# plot data in a graph in log scale, debugging use only
def plot_log_scale(xdata, y2, popt, function):
    plt.subplot()
    plt.plot(xdata, y2, 'b*', label='data')
    if len(popt) == 3:
        plt.plot(xdata, function(xdata, *popt), 'r-', label='fit:a=%5.3f, b=%5.3f, c=%5.3f' % tuple(popt))
    else:
        plt.plot(xdata, function(xdata, *popt), 'r-', label='fit:a=%5.18f, b=%5.3f' % tuple(popt))
    # plt.plot(xdata, f(xdata, -41.935,47.6314,-11.045), 'y-', label='fit:a=-41.935, b=47.6314, c=-11.045')

    plt.yscale('log')
    plt.legend(loc='upper left')
    plt.show(block=False)
    return

def func_loged_abxcx2(x, a, b, c):
    return a + b * x + c * x**2

def func_eabxcx2(x, a, b, c):
    return np.exp(a + b * x + c * x**2)

def func_aebx(x, a, b):
    return a * np.exp(b * x)

def func_loged_logabx(x, a, b):
    return np.log(a) + b * x

# sheet = 'PNP'
# TID_level = Library.TID_LEVEL[6]
# file_path = Library.EXCEL_FILE_PATH['TL431']
#
# fit(sheet, TID_level, file_path)
