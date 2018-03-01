import matplotlib.pyplot as plt
import os
import tkinter.filedialog as filedialog
from tkinter import *
from tkinter import ttk
from itertools import cycle
import importlib

from GUI import execute, NetListGenerator, Library


class Interface(object):
    def __init__(self):
        element_width = 18
        element_height = 2

        self.window = Tk()
        self.window.title('Platform')
        self.window.geometry('1000x500')

        self.label_topline = Label(self.window, text=Library.TITLE, font=('Arial', 20), width=30, height=element_height)

        self.label_parts = Label(self.window, text='parts:', font=('Arial', 0), width=element_width, height=element_height)
        self.parts_options = StringVar()
        self.parts_options_tuple = (Library.PARTS)
        self.cb_parts = ttk.Combobox(self.window, textvariable=self.parts_options, exportselection=False, state='readonly')
        self.cb_parts['values'] = self.parts_options_tuple

        self.label_simulation = Label(self.window, text='simulation:', font=('Arial', 0), width=element_width, height=element_height)
        self.simulation_options = StringVar()
        self.simulation_options_tuple = (Library.SIMULATION)
        self.cb_simulation = ttk.Combobox(self.window, textvariable=self.simulation_options, exportselection=False, state='readonly')
        self.cb_simulation['values'] = self.simulation_options_tuple

        self.label_TID_level_lower_bound = Label(self.window, text='TID level lower bound:', font=('Arial', 0), width=element_width, height=element_height)
        self.TID_options_lower = StringVar()
        self.TID_options_tuple = ()
        self.cb_TID_lower_bound = ttk.Combobox(self.window, textvariable=self.TID_options_lower, exportselection=False, state='readonly')
        self.cb_TID_lower_bound['values'] = self.TID_options_tuple

        self.label_TID_level_upper_bound = Label(self.window, text='TID level upper bound:', font=('Arial', 0), width=element_width, height=element_height)
        self.TID_options_upper = StringVar()
        self.cb_TID_upper_bound = ttk.Combobox(self.window, textvariable=self.TID_options_upper, exportselection=False, state='readonly')
        self.cb_TID_upper_bound['values'] = self.TID_options_tuple

        self.label_spec_min = Label(self.window, text='min Y:', font=('Arial', 0), width=element_width, height=element_height)
        self.entry_spec_min = FloatEntry(self.window, width=element_width)

        self.label_spec_max = Label(self.window, text='max Y:', font=('Arial', 0), width=element_width, height=element_height)
        self.entry_spec_max = FloatEntry(self.window, width=element_width)


        self.label_output_x = Label(self.window, text='X Label:', font=('Arial', 0), width=element_width, height=element_height)
        self.output_options_x = StringVar()
        self.output_options_tuple_x = ()
        self.cb_output_x = ttk.Combobox(self.window, textvariable=self.output_options_x, exportselection=False, state='readonly')
        self.cb_output_x['values'] = self.output_options_tuple_x

        self.label_output_y = Label(self.window, text='Y Label:', font=('Arial', 0), width=element_width, height=element_height)
        self.output_options_y = StringVar()
        self.output_options_tuple_y = ()
        self.cb_output_y = ttk.Combobox(self.window, textvariable=self.output_options_y, exportselection=False, state='readonly')
        self.cb_output_y['values'] = self.output_options_tuple_y

        self.button_import = Button(self.window, text='Import', width=15, height=2, command=self.import_hit)
        self.button_execute = Button(self.window, text='Execute', width=15, height=2, command=self.execute_hit)

        self.result_text = StringVar()
        self.label_result_text = Label(self.window, textvariable=self.result_text, font=('Arial', 12), width=80, height=5)

        self.netlist_filepath = relative_path('Netlist/test.cir')
        self.output_filepath = ''
        self.color_gen = cycle('bgrcmyk')

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
                print('Missing title')
        title = line.split(':')[1].replace(' ', '').split('/')
        my_simulation = title[0]
        my_part = title[1]
        my_voltage_source = list()
        my_circuit_core = list()
        my_input = list()
        my_output = list()
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
                    elif line.find('**') == -1 and line.find('.print') == -1:
                        my_output.append(line.replace('\n', ''))
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
        elif len(my_output) == 0:
            print('ERROR!!! Missing \'*Output\', abort import')
            return
        elif len(my_subcircuit) == 0:
            print('ERROR!!! Missing \'*Subcircuit\', abort import')
            return

        if my_simulation == 'source' and (len(my_parameters) == 0 or len(my_functions) == 0 or len(my_scales) == 0):
            print('ERROR!!! Missing \'*Parameters\' , \'*Scales\' or \'*Functions\' for Current Source simulation, abort import')
            return
        Library.PARTS.append(my_part)
        Library.PARTS = list(set(Library.PARTS))
        count = 0;
        if my_simulation == "source":
            for line in my_parameters:
                if line.replace(" ","") != "":
                    count += 1;
            num_of_para = int(count / 3)
            Library.NUM_OF_PARAMETER[my_part] = num_of_para
        Library.save_name_to_json(Library.TITLE, Library.PARTS, Library.SIMULATION, Library.TID_LEVEL, Library.TID_LIST,
                          Library.EXCEL_FILE_PATH, Library.COL_NAME, Library.SHEET_NAME, Library.NUM_OF_PARAMETER)
        Library.INPUT_VOLTAGE_SOURCE[my_part] = my_voltage_source
        Library.CIRCUIT_CORE[my_part] = my_circuit_core
        Library.SCALE[my_part] = my_scales
        Library.FUNCTIONS[my_part] = my_functions
        Library.INPUT[my_part] = my_input
        Library.OUTPUT_OPTION[my_part] = my_output
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
                                      Library.FUNCTIONS, Library.INPUT, Library.OUTPUT_OPTION, Library.SUBCIRCUIT,
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
            part = self.cb_parts.get()
            simulation = self.cb_simulation.get()
            TID_level_lower = self.cb_TID_lower_bound.get()
            TID_level_upper = self.cb_TID_upper_bound.get()
            output_option_x = self.cb_output_x.get()
            output_option_y = self.cb_output_y.get()
            num_TID_lower = self.get_num_TID(TID_level_lower)
            num_TID_upper = self.get_num_TID(TID_level_upper)

            spec_min = float(self.entry_spec_min.get())
            spec_max = float(self.entry_spec_max.get())

            X_list = list()
            Y_list = list()
            for TID_level in Library.TID_LEVEL:
                num_TID = self.get_num_TID(TID_level)
                if num_TID_lower <= num_TID <= num_TID_upper:
                    self.output_filepath = relative_path('Output/' + part + '_' + TID_level + '_test.txt')
                    netListGenerator.generate(part, simulation, TID_level, output_option_x, output_option_y,
                                              self.output_filepath, self.netlist_filepath)
                    my_result = execute.execute_module3(self.netlist_filepath)
                    print(my_result)
                    X_label, Y_label, X, Y = self.load_and_finalize_output(part, TID_level)
                    self.plotfigure(X_label, Y_label, X, Y, part, simulation, TID_level)
                    X_list.append(num_TID)
                    Y_list.append(Y[5])
            self.plotfigure(X_label='TID level', Y_label=Y_label, X=X_list, Y=Y_list, part=part, simulation=simulation,
                            TID_level=TID_level_lower, TID_level2=TID_level_upper, spec_min=spec_min, spec_max=spec_max)
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
        self.TID_options_lower.set('')
        self.TID_options_upper.set('')
        self.output_options_x.set('')
        self.output_options_y.set('')
        self.result_text.set('')
        return

    def input_check(self):
        if self.cb_TID_lower_bound.get() == '' or \
                self.cb_TID_upper_bound.get() == '' or \
                self.cb_parts.get() == '' or \
                self.cb_simulation.get() == '' or \
                self.entry_spec_min.get() == '' or \
                self.entry_spec_max.get() == '' or \
                self.cb_output_x.get() == '' or \
                self.cb_output_y.get() == '':
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
            self.output_options_tuple_x = (Library.OUTPUT_OPTION[part])
            self.cb_output_x['values'] = self.output_options_tuple_x
            self.output_options_x.set('')
            self.output_options_tuple_y = (Library.OUTPUT_OPTION[part])
            self.cb_output_y['values'] = self.output_options_tuple_y
            self.output_options_y.set('')
        except:
            pass
        return

    def simulation_onselect(self, evt):
        try:
            self.TID_option_update()
        except:
            pass
        return

    def start(self):
        # row 0
        row = 0
        self.label_topline.grid(row=row, columnspan=3)

        # row 1
        row = 1
        self.label_parts.grid(row=row)
        self.label_simulation.grid(row=row, column=1)
        self.label_TID_level_lower_bound.grid(row=row, column=2)
        self.label_TID_level_upper_bound.grid(row=row, column=3)

        # row 2
        row = 2
        self.cb_parts.grid(row=row)
        self.cb_simulation.grid(row=row, column=1)
        self.cb_TID_lower_bound.grid(row=row, column=2)
        self.cb_TID_upper_bound.grid(row=row, column=3)

        # row 3
        row = 3
        self.label_spec_min.grid(row=row, column=0, pady=(20,0))
        self.label_spec_max.grid(row=row, column=1, pady=(20,0))
        # row 4
        row = 4
        self.entry_spec_min.grid(row=row, column=0)
        self.entry_spec_max.grid(row=row, column=1)
        # row 5
        row = 5
        self.label_output_x.grid(row=row, column=0, pady=(20, 0))
        self.label_output_y.grid(row=row, column=1, pady=(20, 0))

        # row 6
        row = 6
        self.cb_output_x.grid(row=row, column=0)
        self.cb_output_y.grid(row=row, column=1)

        # row 7
        row = 7
        # row 8
        row = 8
        self.button_import.grid(row=row, column=0)
        self.button_execute.grid(row=row, sticky='E', columnspan=3, pady=10)

        # row 9
        row = 9
        self.label_result_text.grid(row=row, column=0, columnspan=3)


        # bind onselect function with widget
        self.cb_parts.bind('<<ComboboxSelected>>', self.part_onselect)
        self.cb_simulation.bind('<<ComboboxSelected>>', self.simulation_onselect)

        self.window.mainloop()
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

    def plotfigure(self, X_label, Y_label, X, Y, part, simulation, TID_level, TID_level2=None, spec_min=None, spec_max=None):
        plt.figure(part + simulation + ' X=' + X_label + ' Y=' + Y_label, figsize=(10,8))
        if TID_level2:
            plt.clf()
            plt.axhline(y=spec_max, color='r', linestyle='-')
            plt.axhline(y=spec_min, color='r', linestyle='-')
            plt.plot(X, Y, next(self.color_gen), label="Part=" + part + "TID level=" + TID_level + '~' + TID_level2)
            plt.ylim(min(min(Y), spec_min) - 0.3, max(max(Y), spec_max) + 0.3)
        else:
            plt.plot(X, Y, next(self.color_gen), label="Part=" + part + "TID level=" + TID_level)
        plt.xlabel(X_label)
        plt.ylabel(Y_label)
        # plt.plot(X, Y, 'b*')
        plt.legend(loc='upper left')
        plt.show(block=False)
        return

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
            self.__variable.set(self.newvalue)
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
