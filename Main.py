import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, FigureCanvasAgg
import matplotlib.backends.tkagg as tkagg
import matplotlib
matplotlib.use("TkAgg")

import tkinter.filedialog as filedialog
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from itertools import cycle
from time import sleep
import numpy as np
import importlib
import xlsxwriter
import os

from GUI import execute, NetListGenerator, Library, FILEPATHS


class Interface(object):
    def __init__(self):
        element_width = 22
        element_height = 2
        element_half_width = int(element_width/2 + 2)
        background_color = '#87CEFA'
        my_font = ('Arial', 18)

        self.window = Tk()
        self.window.title('Platform')
        self.window.configure(background=background_color)
        # self.window.geometry('1150x700')

        self.label_topline = Label(self.window, text=Library.TITLE, font=my_font, width=30, height=element_height, bg=background_color)
        self.label_input_header = Label(self.window, text="Input: ", font=my_font, width=element_half_width, height=element_height, bg=background_color)
        self.label_output_header = Label(self.window, text="Output: ", font=my_font, width=element_half_width, height=element_height, bg=background_color)
        self.label_spec_header = Label(self.window, text="Specification: ", font=my_font, width=element_half_width, height=element_height, bg=background_color)

        self.empty = Label(self.window, text="", font=my_font, width=element_width, height=element_height, bg=background_color)

        self.label_parts = Label(self.window, text='parts:', font=my_font, width=element_width, height=element_height, bg=background_color)
        self.parts_options = StringVar()
        self.parts_options_tuple = (Library.PARTS)
        self.cb_parts = ttk.Combobox(self.window, textvariable=self.parts_options, exportselection=False, state='readonly')
        self.cb_parts['values'] = self.parts_options_tuple

        self.label_simulation = Label(self.window, text='simulation mode:', font=my_font, width=element_width, height=element_height, bg=background_color)
        self.simulation_options = StringVar()
        self.simulation_options_tuple = (Library.SIMULATION)
        self.cb_simulation = ttk.Combobox(self.window, textvariable=self.simulation_options, exportselection=False, state='readonly')
        self.cb_simulation['values'] = self.simulation_options_tuple

        self.label_TID_level_lower_bound = Label(self.window, text='TID level lower bound(rad):', font=my_font, width=element_width, height=element_height, bg=background_color)
        # self.TID_options_lower = StringVar()
        # self.TID_options_tuple = ()
        # self.cb_TID_lower_bound = ttk.Combobox(self.window, textvariable=self.TID_options_lower, exportselection=False, state='readonly')
        # self.cb_TID_lower_bound['values'] = self.TID_options_tuple
        self.entry_TID_lower_bound = TIDEntry(self.window, width=element_width)

        self.label_TID_level_upper_bound = Label(self.window, text='TID level upper bound(rad):', font=my_font, width=element_width, height=element_height, bg=background_color)
        # self.TID_options_upper = StringVar()
        # self.cb_TID_upper_bound = ttk.Combobox(self.window, textvariable=self.TID_options_upper, exportselection=False, state='readonly')
        # self.cb_TID_upper_bound['values'] = self.TID_options_tuple
        self.entry_TID_upper_bound = TIDEntry(self.window, width=element_width)

        self.label_output = Label(self.window, text='Output:', font=my_font, width=element_width, height=element_height, bg=background_color)
        self.output_options = StringVar()
        self.output_options_tuple = ()
        self.cb_output = ttk.Combobox(self.window, textvariable=self.output_options, exportselection=False, state='readonly')
        self.cb_output['values'] = self.output_options_tuple

        self.label_spec_min = Label(self.window, text='min Y:', font=my_font, width=element_width, height=element_height, bg=background_color)
        self.entry_spec_min = FloatEntry(self.window, width=element_width)

        self.label_spec_max = Label(self.window, text='max Y:', font=my_font, width=element_width, height=element_height, bg=background_color)
        self.entry_spec_max = FloatEntry(self.window, width=element_width)


        self.button_import = Button(self.window, text='Import', font=my_font, width=15, height=2, command=self.import_hit)
        self.button_execute = Button(self.window, text='Execute', font=my_font, width=15, height=2, command=self.execute_hit)
        self.button_save = Button(self.window, text='Save', font=my_font, width=15, height=2, command=self.save)
        self.button_change_scale = Button(self.window, text='Change Scale', font=my_font, width=15, height=2, command=self.change_scale)

        self.canvas_plot = Canvas(self.window, width=600, height=500, bg=background_color, highlightbackground=background_color)

        self.result_text = StringVar()
        self.label_result_text = Label(self.window, textvariable=self.result_text, font=my_font, width=2 * element_width, height=5, bg=background_color)

        self.X_list = list()
        self.Y_list = list()
        self.figure_input = list()
        self.image = PhotoImage()  # keep a reference to ploted photo. Otherwise, the ploted photo will disappear
        self.netlist_filepath = relative_path('Library/temp/myNetlist.cir')
        self.output_filepath = ''
        self.color_gen = cycle('bgcmyk')

        return

    def import_hit(self):
        filename = filedialog.askopenfilename(initialdir=relative_path('Netlist'))
        # print(filename)
        if filename == () or filename == '':
            return
        f = open(filename, 'r')
        line = next(f)
        while line[0:5] != 'Title':
            line = next(f, None)
            if line is None:
                print('Missing Title')
                return
        title = line.split(':')[1].replace(' ', '').split('/')
        if len(title) < 3:
            print('Missing simulation type, part name or parameter in Title')
            return
        my_simulation = title[0]
        if my_simulation == 'source':
            my_simulation = Library.SIMULATION_SOURCE
        elif my_simulation == 'model':
            my_simulation = Library.SIMULATION_MODEL
        my_part = title[1]
        my_parameter = title[2]
        my_voltage_source = list()
        my_circuit_core = list()
        my_input = list()
        my_output = list()
        my_output_option = list()
        my_subcircuit = list()
        my_library = list()

        my_parameters = list()
        my_scales = list()
        my_functions = list()

        line = next(f)
        while line is not None:
            if line.find('*Input Voltage Source') != -1:
                line = next(f)
                while line.find('*End Input Voltage Source') == -1:
                    if line is None:
                        print('ERROR!!! Missing \'*End Input Voltage Source\', abort import')
                        return
                    elif line.find('*****') == -1:
                        my_voltage_source.append(line.replace('\n', ''))
                    line = next(f)
            elif line.find('*Circuit Core') != -1:
                line = next(f)
                while line.find('*End Circuit Core') == -1:
                    if line is None:
                        print('ERROR!!! Missing \'*End Circuit Core\', abort import')
                        return
                    elif line.find('*****') == -1:
                        my_circuit_core.append(line.replace('\n', ''))
                    line = next(f)
            elif line.find('*Input') != -1:
                line = next(f)
                while line.find('*End Input') == -1:
                    if line is None:
                        print('ERROR!!! Missing \'*End Input\', abort import')
                        return
                    elif line.find('*****') == -1:
                        my_input.append(line.replace('\n', ''))
                    line = next(f)
            elif line.find('*Output') != -1:
                line = next(f)
                while line.find('*End Output') == -1:
                    if line is None:
                        print('ERROR!!! Missing \'*End Output\', abort import')
                        return
                    elif line.find('*****') == -1 and line.find('.print') == -1:
                        my_output.append(line.replace('\n', ''))
                        my_output_option.append(line.replace('\n', ''))
                    line = next(f)
            elif line.find('*Subcircuit') != -1:
                line = next(f)
                while line.find('*End Subcircuit') == -1:
                    if line is None:
                        print('ERROR!!! Missing \'*End Subcircuit\', abort import')
                        return
                    elif line.find('*****') == -1:
                        my_subcircuit.append(line.replace('\n', ''))
                    line = next(f)
            elif line.find('*Library') != -1:
                line = next(f)
                while line.find('*End Library') == -1:
                    if line is None:
                        print('ERROR!!! Missing \'*End Library\', abort import')
                        return
                    elif line.find('*****') == -1:
                        my_library.append(line.replace('\n', ''))
                    line = next(f)
            elif line.find('*Parameters') != -1:
                line = next(f)
                while line.find('*End Parameters') == -1:
                    if line is None:
                        print('ERROR!!! Missing \'*End Parameters\', abort import')
                        return
                    elif line.find('*****') == -1:
                        my_parameters.append(line.replace('\n', ''))
                    line = next(f)
            elif line.find('*Scales') != -1:
                line = next(f)
                while line.find('*End Scales') == -1:
                    if line is None:
                        print('ERROR!!! Missing \'*End Scales\', abort import')
                        return
                    elif line.find('*****') == -1:
                        my_scales.append(line.replace('\n', ''))
                    line = next(f)
            elif line.find('*Function') != -1:
                line = next(f)
                while line.find('*End Function') == -1:
                    if line is None:
                        print('ERROR!!! Missing \'*End Function\', abort import')
                        return
                    elif line.find('*****') == -1:
                        my_functions.append(line.replace('\n', ''))
                    line = next(f)
            line = next(f, None)
        f.close()
        if len(my_voltage_source) == 0:
            print('ERROR!!! Missing \'*Input Voltage Source\', abort import')
            return
        elif len(my_circuit_core) == 0:
            print('ERROR!!! Missing \'*Circuit Core\', abort import')
            return
        elif len(my_input) == 0:
            print('ERROR!!! Missing \'*Input\', abort import')
            return
        elif len(my_output_option) == 0:
            print('ERROR!!! Missing \'*Output\', abort import')
            return
        elif len(my_subcircuit) == 0:
            print('ERROR!!! Missing \'*Subcircuit\', abort import')
            return

        if my_simulation == Library.SIMULATION_SOURCE and (len(my_parameters) == 0 or len(my_functions) == 0 or len(my_scales) == 0):
            print('ERROR!!! Missing \'*Parameters\' , \'*Scales\' or \'*Functions\' for Current Source simulation, abort import')
            return
        Library.PARTS.append(my_part)
        Library.PARTS = list(set(Library.PARTS))
        count = 0;
        if my_simulation == Library.SIMULATION_SOURCE:
            for line in my_parameters:
                if line.replace(" ", "") != "":
                    count += 1;
            num_of_para = int(count / 3)
            Library.NUM_OF_PARAMETER[my_part] = num_of_para
            Library.SCALE[my_part] = my_scales
            Library.FUNCTIONS[my_part] = my_functions
        Library.save_name_to_json(Library.TITLE, Library.PARTS, Library.SIMULATION, Library.TID_LEVEL, Library.TID_LIST,
                          Library.EXCEL_FILE_PATH, Library.COL_NAME, Library.SHEET_NAME, Library.NUM_OF_PARAMETER)
        Library.INPUT_VOLTAGE_SOURCE[my_part] = my_voltage_source
        Library.CIRCUIT_CORE[my_part] = my_circuit_core
        Library.INPUT[my_part] = my_input
        m_output_dict = Library.OUTPUT.get(my_part)
        if m_output_dict is not None:
            m_output_dict[my_parameter] = my_output
        else:
            temp = dict()
            temp[my_parameter] = my_output
            Library.OUTPUT[my_part] = temp
        Library.OUTPUT_OPTION[my_part] = my_output_option
        # temp = dict()
        # temp[my_simulation] = my_subcircuit
        # Library.SUBCIRCUIT[my_part] = temp
        m_dict = Library.SUBCIRCUIT.get(my_part)
        if m_dict is not None:
            m_dict[my_simulation] = my_subcircuit
        else:
            temp = dict()
            temp[my_simulation] = my_subcircuit
            Library.SUBCIRCUIT[my_part] = temp
        if Library.LIBRARY_JFET.get(my_part) is None:
            Library.LIBRARY_JFET[my_part] = []

        Library.save_library_to_json(Library.INPUT_VOLTAGE_SOURCE, Library.CIRCUIT_CORE, Library.SCALE,
                                      Library.FUNCTIONS, Library.INPUT, Library.OUTPUT_OPTION, Library.OUTPUT, Library.SUBCIRCUIT,
                                      Library.LIBRARY_TID_LEVEL_MODEL, Library.LIBRARY_JFET)
        self.refresh()
        self.result_text.set("Import complete")
        return

    def get_num_TID(self, str_TID):
        if str_TID == Library.TPRE_RAD:
            return 0
        num_TID = float(re.findall(r"\d+\.?\d*", str_TID)[0])
        if str_TID.find("k") != -1:
            num_TID = num_TID * 1000
        return num_TID

    def execute_hit(self):
        # try:
        if self.input_check():
            execute.rm_all()
            part = self.cb_parts.get()
            simulation = self.cb_simulation.get()
            TID_level_lower = self.entry_TID_lower_bound.get()
            TID_level_upper = self.entry_TID_upper_bound.get()
            output_option = self.cb_output.get()
            num_TID_lower = self.get_num_TID(TID_level_lower)
            num_TID_upper = self.get_num_TID(TID_level_upper)
            if num_TID_lower > num_TID_upper:
                num_TID_lower = num_TID_lower + num_TID_upper
                num_TID_upper = num_TID_lower - num_TID_upper
                num_TID_lower = num_TID_lower - num_TID_upper

            spec_min = float(self.entry_spec_min.get()) if self.entry_spec_min.get() != '' else None
            spec_max = float(self.entry_spec_max.get()) if self.entry_spec_max.get() != '' else None

            self.X_list.clear()
            self.Y_list.clear()
            oneMore = True
            Tid_Levels_dict = {self.get_num_TID(tid): tid for tid in Library.TID_LEVEL}
            Tid_Levels = [(k, Tid_Levels_dict[k]) for k in sorted(Tid_Levels_dict.keys())]
            for i in range(len(Tid_Levels)):
                num_TID = Tid_Levels[i][0]
                str_TID = Tid_Levels[i][1]
                if (num_TID < num_TID_lower and i + 1 < len(Tid_Levels) and Tid_Levels[i + 1][0] > num_TID_lower) or \
                        (num_TID_lower <= num_TID and (num_TID < num_TID_upper or oneMore)):
                    self.output_filepath = relative_path(FILEPATHS.OUTPUT_DIR_PATH + part + '_' + str_TID + '_test.txt')
                    result = netListGenerator.generate(part, simulation, str_TID, output_option,
                                              self.output_filepath, self.netlist_filepath)
                    if result == False:
                        continue
                    if num_TID >= num_TID_upper:
                        oneMore = False
                    my_result = execute.execute_module3(self.netlist_filepath)
                    # print(my_result)
                    X_label, Y_label, X, Y = self.load_and_finalize_output(part, str_TID)
                    # self.plotfigure(X_label, Y_label, X, Y, part, simulation, TID_level)
                    self.X_list.append(num_TID)
                    lengthX = len(X)
                    for i in range(len(X)):
                        if X[i] == X[int(lengthX / 2)]:
                            self.Y_list.append(Y[i])
                            break
                    # print(X[20])
            unit = ''
            if Y_label[0] == 'V':
                unit = ' (V)'
            elif Y_label[0] == 'I':
                unit = ' (A)'
            Y_label = output_option + unit
            if len(self.X_list) == 0 or len(self.Y_list) == 0:
                message = "No result to show"
                self.result_text.set(message)
                return
            self.figure_input.clear()
            self.figure_input.extend(['TID level (rad)', Y_label, self.X_list, self.Y_list, part, simulation,
                                      num_TID_lower, num_TID_upper, TID_level_lower, TID_level_upper, None, None,
                                      spec_min, spec_max, False, False])
            self.plotfigureTK(self.figure_input[0], self.figure_input[1], self.figure_input[2], self.figure_input[3],
                              self.figure_input[4], self.figure_input[5], self.figure_input[6], self.figure_input[7],
                              self.figure_input[8], self.figure_input[9], self.figure_input[10], self.figure_input[11],
                              self.figure_input[12], self.figure_input[13], self.figure_input[14], self.figure_input[15])
            message = 'part: ' + part + ', TID level = ' + TID_level_lower + ' ~ ' + TID_level_upper + '\n'
            # message = my_result
            self.result_text.set(message)

        # except Exception as error:
        #     print(error)
        #     self.result_text.set('Error! Do you have ' + str(error) + ' data in excel?')
        return

    def refresh(self):
        importlib.reload(Library)
        self.parts_options_tuple = (Library.PARTS)
        self.parts_options.set('')
        self.cb_parts['values'] = self.parts_options_tuple
        self.simulation_options_tuple = (Library.SIMULATION)
        self.simulation_options.set('')
        self.cb_simulation['values'] = self.simulation_options_tuple
        self.output_options.set('')
        # self.TID_options_lower.set('')
        # self.TID_options_upper.set('')
        # self.output_options_x.set('')
        # self.output_options_y.set('')
        self.result_text.set('')
        return

    def input_check(self):
        if self.entry_TID_upper_bound.get() == '' or \
                self.entry_TID_upper_bound.get() == '' or \
                self.cb_parts.get() == '' or \
                self.cb_simulation.get() == '' or \
                self.cb_output.get() == '':
            self.result_text.set('please check your input')
            return False
        self.result_text.set('in process, please wait...')
        return True

    def TID_option_update(self):
        cur_sim = self.cb_simulation.get()
        self.TID_options_tuple = Library.TID_LIST[cur_sim]
        self.TID_options_lower.set('')
        self.TID_options_upper.set('')
        self.cb_TID_lower_bound['values'] = self.TID_options_tuple
        self.cb_TID_upper_bound['values'] = self.TID_options_tuple

    def part_onselect(self, evt):
        try:
            part = self.cb_parts.get()
            self.output_options_tuple = (list(Library.OUTPUT[part].keys()))
            self.cb_output['values'] = self.output_options_tuple
            self.output_options.set('')
        except:
            pass
        return

    def simulation_onselect(self, evt):
        try:
            self.TID_option_update()
        except:
            pass
        return

    def output_onselect(self, evt):
        part = self.cb_parts.get()
        output = self.cb_output.get()
        spec_lib = Library.SPECIFICATION.get(part)
        if spec_lib is not None:
            spec = spec_lib.get(output)
            if spec is not None and len(spec) == 2:
                self.entry_spec_min.insert(0, spec[0])
                self.entry_spec_max.insert(0, spec[1])
        return

    def callback(self, event):
        self.execute_hit()
        return

    def start(self):
        # row 0
        row = 0
        # self.label_topline.grid(row=row, columnspan=3)

        # row 1
        row = 1
        self.label_input_header.grid(row=row, rowspan=3)
        self.label_parts.grid(row=row, column=1)
        self.label_simulation.grid(row=row, column=2)
        self.label_TID_level_lower_bound.grid(row=row, column=3)
        self.label_TID_level_upper_bound.grid(row=row, column=4)

        # row 2
        row = 2
        self.cb_parts.grid(row=row, column=1)
        self.cb_simulation.grid(row=row, column=2)
        self.entry_TID_lower_bound.grid(row=row, column=3)
        self.entry_TID_upper_bound.grid(row=row, column=4)
        # self.cb_TID_lower_bound.grid(row=row, column=2)
        # self.cb_TID_upper_bound.grid(row=row, column=3)

        # row 3
        row = 3
        self.button_import.grid(row=row, column=1, pady=10)

        # row 4
        row = 4
        self.label_spec_header.grid(row=row, column=0, rowspan=2, pady=(20, 0))
        self.label_output.grid(row=row, column=1, pady=(20, 0))
        self.canvas_plot.grid(row=row, column=2, rowspan=10, columnspan=4, padx=(20, 0))

        # row 5
        row = 5
        self.cb_output.grid(row=row, column=1)

        # row 6
        row = 6
        self.label_spec_max.grid(row=row, column=1, pady=(20, 0))

        # row 7
        row = 7
        self.entry_spec_max.grid(row=row, column=1)

        # row 8
        row = 8
        self.label_spec_min.grid(row=row, column=1)

        # row 9
        row = 9
        self.entry_spec_min.grid(row=row, column=1)

        # row 10
        row = 10
        self.button_execute.grid(row=row, column=1, pady=10)

        # row 11
        row = 11
        self.button_save.grid(row=row, column=1)

        # row 12
        row = 12
        self.button_change_scale.grid(row=row, column=1)

        # row 13
        row = 13
        self.label_result_text.grid(row=row, column=1)

        self.button_execute.focus_set()
        # bind onselect function with widget
        self.cb_parts.bind('<<ComboboxSelected>>', self.part_onselect)
        self.cb_simulation.bind('<<ComboboxSelected>>', self.simulation_onselect)
        self.cb_output.bind('<<ComboboxSelected>>', self.output_onselect)
        self.window.bind('<Return>', self.callback)
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        testmode = True
        if testmode is True:
            self.cb_parts.set('LT1175')
            self.cb_simulation.set('compact model')
            self.cb_output.set('Line Regulation')
            self.entry_TID_lower_bound.insert(0, "0")
            self.entry_TID_upper_bound.insert(0, "300k")
        else:
            self.button_import.grid_remove()
        self.window.mainloop()
        return

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.window.destroy()
            self.window.quit()
        return

    def load_and_finalize_output(self, part, TID_level):

        X_label = ''
        Y_label = ''
        XnY = []
        X = []
        Y = []
        f = open(self.output_filepath, 'r')
        # lines = f.readlines()

        # n = open(self.output_filepath, 'w')
        # n.write('part: ' + part + ', TID level = ' + TID_level + '\n')
        # n.writelines(lines)
        for line in f:
            line = line.strip('\n')
            my_line = line.split(' ')
            cnt = 0
            for word in my_line:
                if cnt < 2 and word != '':
                    if X_label == '':
                        X_label = word
                    elif Y_label == '':
                        Y_label = word
                    else:
                        try:
                            XnY.append(float(word))
                            cnt += 1
                        except:
                            cnt = cnt
        f.close()

        for i in range(len(XnY)):
            if i % 2 == 0:
                X.append(XnY[i])
            else:
                Y.append(XnY[i])
        return X_label, Y_label, X, Y

    '''
    ' plot figure in a pop up window
    '''
    def plotfigure(self, X_label, Y_label, X, Y, part, simulation, TID_level, TID_level2=None, spec_min=None, spec_max=None):
        plt.figure(part + simulation + ' X=' + X_label + ' Y=' + Y_label, figsize=(10,8))
        if TID_level2:
            plt.clf()
            y_min = min(Y)
            y_max = max(Y)
            if spec_max is not None:
                plt.axhline(y=spec_max, color='r', linestyle='--')
                y_max = max(y_max, spec_max)
                y_min = min(y_min, spec_max)
            if spec_min is not None:
                plt.axhline(y=spec_min, color='r', linestyle='--')
                y_min = min(y_min, spec_min)
                y_max = min(y_max, spec_min)
            plt.plot(X, Y, next(self.color_gen), label="Part=" + part + "TID level=" + TID_level + '~' + TID_level2)
            plt.plot(X, Y, 'r*')
            gap = y_max - y_min
            plt.ylim(y_min - 0.1 * gap, y_max + 0.1 * gap)
        else:
            plt.plot(X, Y, next(self.color_gen), label="Part=" + part + "TID level=" + TID_level)
        plt.xlabel(X_label)
        plt.ylabel(Y_label)
        plt.legend(loc='upper left')
        plt.show(block=False)
        return

    ''' 
    ' plot figure in the main window
    ' X_label: 
    '''
    def plotfigureTK(self, X_label, Y_label, X, Y, part, simulation, X_min, X_max, TID_level, TID_level2=None,
                     Y_min=None, Y_max=None, spec_min=None, spec_max=None, x_logscale=False, y_logscale=False):
        # preprocessing input
        if X_min > X_max:
            tmp = X_min
            X_min = X_max
            X_max = tmp
        if Y_min is not None and Y_max is not None:
            if Y_min > Y_max:
                tmp = Y_min
                Y_min = Y_max
                Y_max = tmp

        figure = mpl.figure.Figure(figsize=(8, 6))
        figure.clf()
        subplot = figure.add_subplot(111)
        if x_logscale is True:
            subplot.set_xscale('symlog')
        else:
            subplot.set_xscale('linear')
            # subplot.set_yscale('log')
        if y_logscale is True:
            subplot.set_yscale('log', nonposy='clip')
            # Y = np.log(Y)
        else:
            subplot.set_yscale('linear')
        # subplot.plot([1,2,3,4],[5,6,7,8])
        y_min = min(Y)
        y_max = max(Y)
        if spec_max is not None:
            subplot.axhline(y=spec_max, color='r', linestyle='--')
            y_max = max(y_max, spec_max)
        if spec_min is not None:
            subplot.axhline(y=spec_min, color='r', linestyle='--')
            y_min = min(y_min, spec_min)
        subplot.plot(X, Y, next(self.color_gen), label="Part=" + part + " TID level=" + TID_level + '~' + TID_level2)
        subplot.plot(X, Y, 'r*')
        y_gap = y_max - y_min
        y_lower_bound = float(Y_min) if Y_min is not None else y_min - 0.1 * y_gap
        y_upper_bound = float(Y_max) if Y_max is not None else y_max + 0.15 * y_gap
        if y_lower_bound != y_upper_bound:
            subplot.set_ylim([y_lower_bound, y_upper_bound])
        x_gap = X_max - X_min
        if x_gap != 0:
            subplot.set_xlim([X_min, X_max])
        subplot.set_xlabel(X_label)
        subplot.set_ylabel(Y_label)
        # subplot.set_xticks(list(X))
        # subplot.get_xaxis().get_major_formatter().labelOnlyBase = False
        subplot.legend(loc='upper left')

        figure_canvas_agg = FigureCanvasAgg(figure)
        figure_canvas_agg.draw()
        figure_x, figure_y, figure_w, figure_h = figure.bbox.bounds
        figure_w, figure_h = int(figure_w), int(figure_h)
        photo = PhotoImage(master=self.canvas_plot, width=figure_w, height=figure_h)
        self.canvas_plot.create_image(figure_w / 2, figure_h / 2, image=photo)
        self.image = photo  # make a reference to our plot. If not, the image will disappear because Python's garbage collection is like shit
        tkagg.blit(photo, figure_canvas_agg.get_renderer()._renderer, colormode=2)
        # self.canvas_plot = FigureCanvasTkAgg(figure, self.window)
        # self.canvas_plot.show()
        # self.canvas_plot.get_tk_widget().grid(row=4, column=2, rowspan=10, columnspan=4, padx=(20,0))
        return

    def change_scale(self):
        if len(self.figure_input) != 0:
            changeScaleDialog = ChangeScaleWindow()
            self.window.wait_window(changeScaleDialog)
            try:
                scaleinfo = changeScaleDialog.scaleinfo
                if scaleinfo is None:
                    return
            except:
                return
            x_upper, x_lower, x_log, y_upper, y_lower, y_log = scaleinfo
            # x upper bound
            if x_upper != '':
                self.figure_input[7] = self.get_num_TID(x_upper)
            # x lower bound
            if x_lower != '':
                self.figure_input[6] = self.get_num_TID(x_lower)
            # x log scale
            if min(self.figure_input[3]) <= 0 and y_log is True:
                self.result_text.set("can not use log scale on y axis \n negative value detected")
            else:
                self.figure_input[15] = y_log
            # y upper bound
            if scaleinfo[3] != '':
                self.figure_input[11] = y_upper
            # y lower bound
            if scaleinfo[4] != '':
                self.figure_input[10] = y_lower
            # y log scale
            self.figure_input[14] = x_log

            self.plotfigureTK(self.figure_input[0], self.figure_input[1], self.figure_input[2], self.figure_input[3],
                              self.figure_input[4], self.figure_input[5], self.figure_input[6], self.figure_input[7],
                              self.figure_input[8], self.figure_input[9], self.figure_input[10], self.figure_input[11],
                              self.figure_input[12], self.figure_input[13], self.figure_input[14], self.figure_input[15])
        return

    def save(self):
        path = relative_path(FILEPATHS.OUTPUT_DIR_PATH)
        files = os.listdir(path)
        result_path = relative_path(FILEPATHS.OUTPUT_DIR_PATH + 'Result.xlsx')
        part_name = ''
        TIDs = []
        try:
            for file in files:
                if '.txt' in file:
                    part_name = file.split('_')[0]
                    TIDs.append(file.split('_')[1])
        except:
            return
        assign_col = 0
        col_dict = {}
        if TIDs.count('pre') != 0:
            col_dict['pre'] = assign_col
            assign_col += 3
        if TIDs.count('2.5k') != 0:
            col_dict['2.5k'] = assign_col
            assign_col += 3
        if TIDs.count('5k') != 0:
            col_dict['5k'] = assign_col
            assign_col += 3
        if TIDs.count('10k') != 0:
            col_dict['10k'] = assign_col
            assign_col += 3
        if TIDs.count('20k') != 0:
            col_dict['20k'] = assign_col
            assign_col += 3
        if TIDs.count('30k') != 0:
            col_dict['30k'] = assign_col
            assign_col += 3
        if TIDs.count('50k') != 0:
            col_dict['50k'] = assign_col
            assign_col += 3
        if TIDs.count('100k') != 0:
            col_dict['100k'] = assign_col
            assign_col += 3
        if TIDs.count('200k') != 0:
            col_dict['200k'] = assign_col
            assign_col += 3
        if TIDs.count('300k') != 0:
            col_dict['300k'] = assign_col
            assign_col += 3

        workbook = xlsxwriter.Workbook(result_path)
        worksheet = workbook.add_worksheet(part_name)
        for file in files:
            if '.txt' not in file:
                continue
            TID_level = file.split('_')[1]

            f = open(path + '/' + file)
            isX = True
            X_label = ''
            Y_label = ''
            X = []
            Y = []
            for line in f:
                line = line.strip('\n')
                my_line = line.split(' ')
                cnt = 0
                for word in my_line:
                    if cnt < 2 and word != '':
                        if X_label == '':
                            X_label = word
                        elif Y_label == '':
                            Y_label = word
                        else:
                            try:
                                if isX is True:
                                    X.append(float(word))
                                    cnt += 1
                                    isX = False
                                else:
                                    Y.append(float(word))
                                    isX = True
                            except:
                                cnt = cnt
            f.close()
            row = 0
            col = col_dict.get(TID_level)
            worksheet.write(row, col, 'TID level:')
            worksheet.write(row, col + 1, TID_level)
            row += 1
            worksheet.write(row, col, X_label)
            worksheet.write(row, col + 1, Y_label)
            row += 1
            for index in range(len(X)):
                worksheet.write(row, col, X[index])
                worksheet.write(row, col + 1, Y[index])
                row += 1
        workbook.close()
        message = 'File saved at ./' + FILEPATHS.OUTPUT_DIR_PATH + 'Result.xlsx'
        self.result_text.set(message)
        return


class ChangeScaleWindow(Toplevel):
    def __init__(self):
        super().__init__()
        self.title('change scale')
        self.attributes('-topmost', 'true')
        element_width = 16
        my_font = ('Arial', 15)
        self.label_x_upper = Label(self, text='x upper bound(rad)', font=my_font, width=element_width)
        self.entry_x_upper = TIDEntry(self, width=element_width)
        self.label_x_lower = Label(self, text='x lower bound(rad)', font=my_font, width=element_width)
        self.entry_x_lower = TIDEntry(self, width=element_width)
        self.xlog = IntVar()
        self.checkbutton_x = Checkbutton(self, text="log scale x", font=my_font, variable=self.xlog)

        self.label_y_upper = Label(self, text='y upper bound', font=my_font, width=element_width)
        self.entry_y_upper = FloatEntry(self, width=element_width)
        self.label_y_lower = Label(self, text='y lower bound', font=my_font, width=element_width)
        self.entry_y_lower = FloatEntry(self, width=element_width)
        self.ylog = IntVar()
        self.checkbutton_y = Checkbutton(self, text="log scale y", font=my_font, variable=self.ylog)

        self.button_ok = Button(self, text='OK', font=my_font, width=5, height=2, command=self.ok)
        self.button_cancel = Button(self, text='Cancel', font=my_font, width=5, height=2, command=self.cancel)
        self.start()

    def start(self):
        # row 0
        row = 0
        self.label_x_upper.grid(row=row, column=0)
        self.entry_x_upper.grid(row=row, column=1)
        self.label_y_upper.grid(row=row, column=2)
        self.entry_y_upper.grid(row=row, column=3)

        # row 1
        row = 1
        self.label_x_lower.grid(row=row, column=0)
        self.entry_x_lower.grid(row=row, column=1)
        self.label_y_lower.grid(row=row, column=2)
        self.entry_y_lower.grid(row=row, column=3)

        # row 2
        row = 2
        self.checkbutton_x.grid(row=row, column=0, sticky=W)
        self.checkbutton_y.grid(row=row, column=2, sticky=W)
        # row 5
        row = 5
        self.button_cancel.grid(row=row, column=2)
        self.button_ok.grid(row=row, column=3)


    def ok(self):
        x_upper = self.entry_x_upper.get()
        x_lower = self.entry_x_lower.get()
        x_log = (self.xlog.get() == 1)
        y_upper = self.entry_y_upper.get()
        y_lower = self.entry_y_lower.get()
        y_log = (self.ylog.get() == 1)

        self.scaleinfo = [x_upper, x_lower, x_log, y_upper, y_lower, y_log]
        self.destroy()

    def cancel(self):
        self.scaleinfo = None
        self.destroy()


class ValidatingEntry(Entry):
    # base class for validating entry widgets

    def __init__(self, master, value="", **kw):
        Entry.__init__(self, master, kw)
        self.__value = value
        self.__variable = StringVar()
        self.__variable.set(value)
        self.__variable.trace("w", self.__callback)
        self.config(textvariable=self.__variable)

    def __callback(self, *dummy):
        value = self.__variable.get()
        newvalue = self.validate(value)
        if newvalue is None:
            self.__variable.set(self.__value)
        elif newvalue != value:
            self.__value = newvalue
            self.__variable.set(newvalue)
        else:
            self.__value = value

    def validate(self, value):
        # override: return value, new value, or None if invalid
        return value


class FloatEntry(ValidatingEntry):

    def validate(self, value):
        try:
            if len(value) == 1 and value == '-':
                return value
            elif value:
                v = float(value)
            return value
        except ValueError:
            return None


class TIDEntry(ValidatingEntry):

    def validate(self, value):
        try:
            if len(value) > 1 and value[-1] == 'k' and value.find('k', 0, len(value) - 1) == -1:
                if float(value[0:-1]) > 300:
                    return '300k'
                return value
            elif len(value) > 1 and value[-1] != 'k' and value.find('k') != -1:
                return None
            elif value:
                v = float(value)
                if v > 300000:
                    return '300000'
            return value
        except ValueError:
            return None


def relative_path(path):
    dirname = os.path.dirname(os.path.realpath('__file__'))
    path = os.path.join(dirname, path)
    return os.path.normpath(path)


if __name__ == "__main__":
    interface = Interface()
    execute = execute.Execute()
    netListGenerator = NetListGenerator.NetListGenerator()
    execute.mkdirs()
    interface.start()
