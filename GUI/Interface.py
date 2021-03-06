import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, FigureCanvasAgg
import matplotlib.backends.tkagg as tkagg
from matplotlib import ticker as mticker
import matplotlib
matplotlib.use("TkAgg")

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from itertools import cycle
import importlib
import xlsxwriter
import os
import datetime
import xlrd

from GUI import execute, NetListGenerator, Library, FILEPATHS, Entry, ChangeScaleWindow, reset, createSaSJson, createNaLJson
import Main

'''
Interface class uses tk and ttk to implement the GUI for this program. 
'''

class Interface(object):
    def __init__(self):
        part_element_width = 20                             # elements' width in part frame
        element_width = 18                                  # elements' width in other frames
        element_height = 2                                  # elements' hight in all frames
        element_half_width = int(element_width/2 + 2)       # smaller width for some of the elements
        self.backgroundcolor = '#CBE7CE'                    # background color for the main interface and the figure
        self.figsize = (8, 4)                               # size of the graph on main interface
        my_font = ('Arial', 10)                             # font size for all elements on main interface

        # tk main interface configuration
        self.window = Tk()
        self.window.title('Platform')
        self.window.configure(background=self.backgroundcolor)
        self.window.option_add("*Font", my_font)
        # self.window.geometry('1150x700')

        # menu configuration on top
        menubar = Menu(self.window, bg="DarkSeaGreen1")
        filemenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Import", command=self.import_hit)
        filemenu.add_command(label="Reset", command=self.reset_hit)
        filemenu.add_command(label="refresh spec", command=self.refresh_spec_hit)
        self.window.config(menu=menubar)

        # header for each section, not in use in current version
        self.label_topline = Label(self.window, text=Library.TITLE, font=my_font, width=30, height=element_height,
                                   bg=self.backgroundcolor)
        self.label_input_header = Label(self.window, text="Input: ", font=my_font, width=element_half_width,
                                        height=element_height, bg=self.backgroundcolor)
        self.label_output_header = Label(self.window, text="Output: ", font=my_font, width=element_half_width,
                                         height=element_height, bg=self.backgroundcolor)
        self.label_spec_header = Label(self.window, text="Specification: ", font=my_font, width=element_half_width,
                                       height=element_height, bg=self.backgroundcolor)

        # part frame, place all elements related to part in this frame
        self.frame_part = Frame(height=element_height * 9, width=part_element_width, bg=self.backgroundcolor, bd=2,
                                relief=RIDGE)
        # self.frame_part.config(highlightbackground="black", highlightthickness=1)

        # part selection combobox and help button (open datasheet)
        self.frame_part_help = Frame(self.frame_part, height=element_height, width=part_element_width,
                                     bg=self.backgroundcolor)
        self.label_parts = Label(self.frame_part_help, text='Parts:', font=my_font, width=element_half_width,
                                 height=element_height, bg=self.backgroundcolor)
        self.button_part_help = Button(self.frame_part_help, text='?', font=my_font, width=1, height=1,
                                       command=self.part_help_hit)
        self.parts_options = StringVar()
        self.parts_options_tuple = (Library.PARTS)
        self.cb_parts = ttk.Combobox(self.frame_part, width=part_element_width, textvariable=self.parts_options,
                                     exportselection=False, state='readonly')
        self.cb_parts['values'] = self.parts_options_tuple

        # simulation selection combobox, not in use in current version
        self.label_simulation = Label(self.frame_part, text='Simulation Mode:', font=my_font, width=element_width,
                                      height=element_height, bg=self.backgroundcolor)
        self.simulation_options = StringVar()
        self.simulation_options_tuple = (Library.SIMULATION)
        self.cb_simulation = ttk.Combobox(self.frame_part, width=part_element_width,
                                          textvariable=self.simulation_options, exportselection=False, state='readonly')
        self.cb_simulation['values'] = self.simulation_options_tuple

        # output(specification) selection combobox
        self.label_output = Label(self.frame_part, text='Specification:', font=my_font, width=part_element_width,
                                  height=element_height, bg=self.backgroundcolor)
        self.output_options = StringVar()
        self.output_options_tuple = ()
        self.cb_output = ttk.Combobox(self.frame_part, width=part_element_width, textvariable=self.output_options,
                                      exportselection=False, state='readonly')
        self.cb_output['values'] = self.output_options_tuple

        # sub-frame for dataset input box
        self.label_dataset = Label(self.frame_part, text='Dataset:', font=my_font, width=part_element_width,
                                       height=1, bg=self.backgroundcolor)
        self.label_dataset_range = Label(self.frame_part, text='(Range)', font=my_font, width=part_element_width,
                                       height=element_height, bg=self.backgroundcolor)
        self.entry_dataset = Entry.FloatEntry(self.frame_part, width=part_element_width)

        # sub-frame for showing specification max
        self.frame_max = Frame(self.frame_part, height=element_height, width=element_width, bg=self.backgroundcolor)
        self.label_spec_max = Label(self.frame_max, text='max:', font=my_font, width=int(element_width/3 - 1),
                                    height=element_height, bg=self.backgroundcolor)
        self.label_spec_max_value = Label(self.frame_max, text='', font=my_font, width=int(element_width/3 + 3),
                                          height=element_height, bg=self.backgroundcolor)
        self.label_spec_max_unit = Label(self.frame_max, text='', font=my_font, width=int(element_width/3 - 2),
                                         height=element_height, bg=self.backgroundcolor)

        # sub-frame for showing specification min
        self.frame_min = Frame(self.frame_part, height=element_height, width=element_width, bg=self.backgroundcolor)
        self.label_spec_min = Label(self.frame_min, text='min:', font=my_font, width=int(element_width/3 - 1),
                                    height=element_height, bg=self.backgroundcolor)
        self.label_spec_min_value = Label(self.frame_min, text='', font=my_font, width=int(element_width/3 + 3),
                                          height=element_height, bg=self.backgroundcolor)
        self.label_spec_min_unit = Label(self.frame_min, text='', font=my_font, width=int(element_width/3 - 2),
                                         height=element_height, bg=self.backgroundcolor)

        # environment frame, place all elements related to environment inputs in this frame
        self.frame_environment = Frame(height=element_height * 2, width=element_width * 6, bg=self.backgroundcolor,
                                       bd=2, relief=RIDGE)

        # dose rate selection combobox
        self.label_dose = Label(self.frame_environment, text='Dose Rate(rad/s):', font=my_font, width=element_width,
                                height=element_height,
                                 bg=self.backgroundcolor)
        self.dose_options = StringVar()
        self.dose_options_tuple = ["100","0.1","0.02"]
        self.cb_dose = ttk.Combobox(self.frame_environment, width=element_half_width, textvariable=self.dose_options,
                                    exportselection=False, state='readonly')
        self.cb_dose['values'] = self.dose_options_tuple

        # hydrogen content selection combobox
        self.label_hydrogen = Label(self.frame_environment, text='Hydrogen Content(%):', font=my_font,
                                    width=element_width + 1, height=element_height, bg=self.backgroundcolor)
        self.hydrogen_options = StringVar()
        self.hydrogen_options_tuple = ["0","0.1","1","1.3","100"]
        self.cb_hydrogen = ttk.Combobox(self.frame_environment, width=element_half_width,
                                        textvariable=self.hydrogen_options, exportselection=False, state='readonly')
        self.cb_hydrogen['values'] = self.hydrogen_options_tuple

        # input bias selection combobox
        self.label_bias = Label(self.frame_environment, text='Bias(V):', font=my_font, width=element_width + 1,
                                height=element_height, bg=self.backgroundcolor)
        self.bias_options = StringVar()
        self.bias_options_tuple = ["0"]
        self.cb_bias = ttk.Combobox(self.frame_environment, width=element_half_width, textvariable=self.bias_options,
                                    exportselection=False, state='readonly')
        self.cb_bias['values'] = self.bias_options_tuple

        # temperature input box
        self.label_temperature = Label(self.frame_environment, text='Temperature(C):', font=my_font,
                                       width=element_width, height=element_height, bg=self.backgroundcolor)
        self.entry_temperature = Entry.FloatEntry(self.frame_environment, width=element_half_width)

        # TID level range input boxes
        self.label_TID_level_lower_bound = Label(self.frame_environment, text='TID min(rad):', font=my_font,
                                                 width=element_width, height=element_height, bg=self.backgroundcolor)
        self.entry_TID_lower_bound = Entry.TIDEntry(self.frame_environment, width=element_half_width)

        self.label_TID_level_upper_bound = Label(self.frame_environment, text='TID max(rad):', font=my_font,
                                                 width=element_width, height=element_height, bg=self.backgroundcolor)
        self.entry_TID_upper_bound = Entry.TIDEntry(self.frame_environment, width=element_half_width)

        # frame for switch button
        self.frame_switch_button = Frame(self.window, height=element_height, width=element_width, bg=self.backgroundcolor)

        self.button_switch = Button(self.frame_switch_button, text='Switch', font=my_font, width=10, height=2,
                                    command=self.switch_hit, bg="CadetBlue2", activebackground ="CadetBlue1")
        self.switched_plot = False
        self.switch_tids = StringVar()
        self.cb_switch_tid = ttk.Combobox(self.frame_switch_button, width=10, textvariable=self.switch_tids,
                                          exportselection=False, state='readonly')
        self.empty = Label(self.frame_switch_button, text="", font=my_font, width=13, height=element_height,
                           bg=self.backgroundcolor)

        # input button, not in use in current version
        self.button_import = Button(self.window, text='Import', font=my_font, width=15, height=2,
                                    command=self.import_hit)

        # frame for execute button and change scale button
        self.frame_execute_or_change_scale = Frame(height=element_height, width=element_width * 2,
                                                   bg=self.backgroundcolor)
        self.button_execute = Button(self.frame_execute_or_change_scale, text='Execute', font=my_font, width=10,
                                     height=2, command=self.execute_hit, bg="PaleGreen2", activebackground ="PaleGreen1")
        self.button_change_scale = Button(self.frame_execute_or_change_scale, text='Change Scale', font=my_font,
                                          width=10, height=2, command=self.change_scale, bg="LemonChiffon2",
                                          activebackground ="lemon chiffon")

        # frame for save button and clear button
        self.frame_save_or_clear = Frame(height=element_height, width=element_width * 2, bg=self.backgroundcolor)
        self.button_save = Button(self.frame_save_or_clear, text='Save', font=my_font, width=10, height=2,
                                  command=self.save_hit, bg="SlateGray2", activebackground="SlateGray1")
        self.button_clear = Button(self.frame_save_or_clear, text='Clear', font=my_font, width=10, height=2,
                                   command=self.clear, bg="PeachPuff2", activebackground="peach puff")

        # canvas for showing the graph
        self.canvas_plot = Canvas(self.window, width=800, height=400, bg=self.backgroundcolor,
                                  highlightbackground=self.backgroundcolor)
        self.figure = mpl.figure.Figure(figsize=self.figsize, facecolor=self.backgroundcolor, edgecolor='w')

        self.result_text = StringVar()
        self.label_result_text = Label(self.window, textvariable=self.result_text, font=my_font,
                                       width=element_width * 2,
                                       height=5, bg=self.backgroundcolor, justify='center')
        self.cross_spec_text = StringVar()
        self.label_cross_spec_text = Label(self.window, textvariable=self.cross_spec_text, font=('Arial', 12,'bold'),
                                       width=element_width * 3,
                                       height=5, bg=self.backgroundcolor, justify='center')

        self.X_list = list()                    # store all the X value for displaying on the graph
        self.Y_list = list()                    # store all the Y value for displaying on the graph
        self.figure_input = list()              # store all the data for plotting the graph
        self.previous_part = ''                 # store the last plotted part
        self.previous_Y_label = ''              # store the last plotted Y label (specification)
        self.cross_message = list()             # store the cross specification messages
        self.switched_cross_message = list()    # store the cross specification messages for switched graphs
        self.AD590_base_temperature = 27        # default temperature
        self.multiplot = False                  # indicate if is multiploting
        self.image = PhotoImage()               # keep a reference to ploted photo. Otherwise, the ploted photo will disappear
        self.netlist_filepath = Main.relative_path(FILEPATHS.TEMP_DIR_PATH + 'myNetlist.cir')   # file path to the generated netlist
        self.output_filepath = ''               # file path to the result generated by Xyce
        self.color_gen = cycle('bgcmyk')        # color generator for plotting graphs

        return

    # read all netlist in Netlist folder and add/update the all parts into library
    def import_hit(self):
        # filename = filedialog.askopenfilename(initialdir=relative_path('Netlist'))
        # print(filename)
        for filename in os.listdir(Main.relative_path('Netlist')):
            try:
                # filename = filedialog.askopenfilename(initialdir=relative_path('Netlist'))
                # # print(filename)
                # if filename == () or filename == '':
                #     return
                if filename[-4:] != '.cir':
                    continue
                f = open('Netlist/' + filename, 'r')
                line = next(f)
                while line[0:5] != 'Title':
                    line = next(f, None)
                    if line is None:
                        print('Missing Title')
                        return
                title = line.split(':')[1].split('/')
                my_part = title[0].strip()
                my_spec = title[1].strip()
                my_voltage_source = list()
                my_circuit_core = list()
                my_input = list()
                my_output = list()
                my_subcircuit = list()
                my_extra_library = list()

                line = next(f)
                while line is not None:
                    if line.find('*Input Voltage Source') != -1:
                        line = next(f)
                        while line.find('*Circuit Core') == -1:
                            if line is None:
                                print('ERROR!!! Missing \'*Circuit Core\', abort import')
                                return
                            elif line.find('*****') == -1:
                                my_voltage_source.append(line.replace('\n', ''))
                            line = next(f)
                        continue
                    elif line.find('*Circuit Core') != -1:
                        line = next(f)
                        while line.find('*Input') == -1:
                            if line is None:
                                print('ERROR!!! Missing \'*Input\', abort import')
                                return
                            elif line.find('*****') == -1:
                                my_circuit_core.append(line.replace('\n', ''))
                            line = next(f)
                        continue
                    elif line.find('*Input') != -1:
                        line = next(f)
                        while line.find('*Output') == -1:
                            if line is None:
                                print('ERROR!!! Missing \'*Output\', abort import')
                                return
                            elif line.find('*****') == -1:
                                my_input.append(line.replace('\n', ''))
                            line = next(f)
                        continue
                    elif line.find('*Output') != -1:
                        line = next(f)
                        while line.find('*Subcircuit') == -1:
                            if line is None:
                                print('ERROR!!! Missing \'*Subcircuit\', abort import')
                                return
                            elif line.find('*****') == -1 and line.find('.print') == -1:
                                my_output.append(line.replace('\n', ''))
                            line = next(f)
                        continue
                    elif line.find('*Subcircuit') != -1:
                        line = next(f)
                        while line.find('*Library') == -1:
                            if line is None:
                                print('ERROR!!! Missing \'*Library\', abort import')
                                return
                            elif line.find('*****') == -1:
                                my_subcircuit.append(line.replace('\n', ''))
                            line = next(f)
                        continue
                    elif line.find('*Library') != -1:
                        line = next(f)
                        while line.find('*Extra Library') == -1:
                            if line is None:
                                print('ERROR!!! Missing \'*Extra Library\', abort import')
                                return
                            line = next(f)
                        continue
                    elif line.find('*Extra Library') != -1:
                        line = next(f)
                        while line.find('*end of the netlist') == -1:
                            if line is None:
                                print('ERROR!!! Missing \'*end of the netlist\', abort import')
                                return
                            elif line.find('*****') == -1 and line.replace(' ','') != '':
                                my_extra_library.append(line.replace('\n', ''))
                            line = next(f)
                        break
                    line = next(f, None)
                f.close()
                if len(my_voltage_source) == 0:
                    print('ERROR!!! Missing \'*Input Voltage Source\', abort import')
                    return
                # elif len(my_circuit_core) == 0:
                #     print('ERROR!!! Missing \'*Circuit Core\', abort import')
                #     return
                elif len(my_input) == 0:
                    print('ERROR!!! Missing \'*Input\', abort import')
                    return
                elif len(my_output) == 0:
                    print('ERROR!!! Missing \'*Output\', abort import')
                    return
                elif len(my_subcircuit) == 0:
                    print('ERROR!!! Missing \'*Subcircuit\', abort import')
                    return

                if my_part not in Library.PARTS:
                    Library.PARTS.append(my_part)
                # Library.PARTS = list(set(Library.PARTS))
                if Library.OUTPUT_NAME.get(my_part) is None:
                    Library.OUTPUT_NAME[my_part] = list()
                if my_spec not in Library.OUTPUT_NAME[my_part]:
                    Library.OUTPUT_NAME[my_part].append(my_spec)
                # Library.OUTPUT_NAME[my_part] = list(set(Library.OUTPUT_NAME[my_part]))


                Library.INPUT_VOLTAGE_SOURCE[my_part + my_spec] = my_voltage_source
                Library.CIRCUIT_CORE[my_part + my_spec] = my_circuit_core
                Library.INPUT[my_part + my_spec] = my_input
                m_output_dict = Library.OUTPUT.get(my_part)
                if m_output_dict is not None:
                    m_output_dict[my_spec] = my_output
                else:
                    temp = dict()
                    temp[my_spec] = my_output
                    Library.OUTPUT[my_part] = temp

                my_subcircuit_model = list()
                for line in my_subcircuit:
                    if line.find('PNP') == -1 and line.find('NPN') == -1:
                        my_subcircuit_model.append(line)
                m_dict = Library.SUBCIRCUIT.get(my_part)
                if m_dict is not None:
                    m_dict[Library.SIMULATION_SOURCE] = my_subcircuit
                    m_dict[Library.SIMULATION_MODEL] = my_subcircuit_model
                else:
                    temp = dict()
                    temp[Library.SIMULATION_SOURCE] = my_subcircuit
                    temp[Library.SIMULATION_MODEL] = my_subcircuit_model
                    Library.SUBCIRCUIT[my_part] = temp
                if len(my_extra_library) != 0:
                    Library.EXTRA_LIBRARY[my_part] = my_extra_library
                elif Library.EXTRA_LIBRARY.get(my_part) is None:
                    Library.EXTRA_LIBRARY[my_part] = []

                createNaLJson.save_name_to_json(Library.TITLE, Library.PARTS, Library.OUTPUT_NAME, Library.SIMULATION,
                                          Library.TID_LEVEL, Library.COL_NAME, path=FILEPATHS.NAME_FILE_PATH)
                createNaLJson.save_library_to_json(Library.INPUT_VOLTAGE_SOURCE, Library.CIRCUIT_CORE, Library.INPUT,
                                             Library.OUTPUT,
                                             Library.SUBCIRCUIT, Library.LIBRARY_TID_LEVEL_MODEL, Library.EXTRA_LIBRARY, path=FILEPATHS.LIBRARY_FILE_PATH)
            except:
                messagebox.showerror("Import Error", "Import Error for file " + filename)
        self.refresh()
        self.result_text.set("Import complete")
        return

    # reset the library
    def reset_hit(self):
        reset.do()
        self.refresh()
        return

    # update the specification library based on the Specification_template.txt file
    def refresh_spec_hit(self):
        s = createSaSJson.save_txt_to_specfication(FILEPATHS.SPEC_TXT_FILE_PATH)
        createSaSJson.save_specification_to_json(s, FILEPATHS.SPECIFICATION_FILE_PATH)
        self.refresh()
        return

    # switch to ILOAD vs OUTPUT graph
    def switch_hit(self):
        if len(self.figure_input) == 0:
            return
        self.switched_plot = not self.switched_plot
        self.figure.clf()
        if self.switched_plot:
            self.switched_cross_message = list()
            self.cb_switch_tid_put()
            output_folder = Main.relative_path(FILEPATHS.OUTPUT_DIR_PATH)
            str_TIDs = list()
            for file in os.listdir(output_folder):
                if file[-4:] == '.txt':
                    str_TID = file.split('_')[1]
                    str_TIDs.append(str_TID)
            num_TIDs = [self.get_num_TID(str_TID) for str_TID in str_TIDs]
            num_str_TID_dict = {self.get_num_TID(str_TID):str_TID for str_TID in str_TIDs}
            num_TIDs = sorted(num_TIDs)
            str_TIDs = [num_str_TID_dict.get(num_TID) for num_TID in num_TIDs]
            self.cb_switch_tid['values'] = str_TIDs
            self.cb_switch_tid.set(str_TIDs[0])
            self.plot_switched_figure_for_tid(str_TIDs[0])

        else:
            self.cb_switch_tid_remove()
            self.plotfigureTK(self.figure_input[0], self.figure_input[1], self.figure_input[2], self.figure_input[3],
                              self.figure_input[4], self.figure_input[5], self.figure_input[6], self.figure_input[7],
                              self.figure_input[8], self.figure_input[9], self.figure_input[10], self.figure_input[11],
                              self.figure_input[12], self.figure_input[13], self.figure_input[14],
                              self.figure_input[15],
                              self.figure_input[16])
            display_message = ''
            self.cross_message = self.cross_message[-1:]
            for cur_message in self.cross_message:
                display_message += cur_message + "\n"
            self.cross_spec_text.set(display_message)
        return

    # open datasheet for the selected part using system default pdf reader
    def part_help_hit(self):
        part = self.cb_parts.get()
        datasheet_path = Main.relative_path('Datasheet') + '/' + part + '.pdf'
        try:
            execute.open_file(datasheet_path)
        except:
            messagebox.showinfo("Failed", "No datasheet for this part")
        return

    # execute the simulation based on user input
    def execute_hit(self):
        # do input check first and then execute:
        if self.input_check():
            if self.switched_plot:
                self.clear()
            # remove every .txt file in Output folder
            execute.rm_all()
            self.temp_focus_out_helper()

            # get part name, TID level range, output option and specifications
            part = self.cb_parts.get()
            # simulation = self.cb_simulation.get()
            DR = self.cb_dose.get()
            H2 = self.cb_hydrogen.get()
            bias = self.cb_bias.get()
            temperature = self.entry_temperature.get()
            dataset = self.entry_dataset.get()
            simulation = Library.SIMULATION_SOURCE
            TID_level_lower = self.entry_TID_lower_bound.get()
            TID_level_upper = self.entry_TID_upper_bound.get()
            output_option = self.cb_output.get()
            num_TID_lower = self.get_num_TID(TID_level_lower)
            num_TID_upper = self.get_num_TID(TID_level_upper)
            if num_TID_lower > num_TID_upper:
                num_TID_lower = num_TID_lower + num_TID_upper
                num_TID_upper = num_TID_lower - num_TID_upper
                num_TID_lower = num_TID_lower - num_TID_upper

            spec_min = float(self.label_spec_min_value.cget('text')) if self.label_spec_min_value.cget('text') != '' else None
            spec_max = float(self.label_spec_max_value.cget('text')) if self.label_spec_max_value.cget('text') != '' else None
            nonlinearity = False
            if part == Library.PART_AD590 and output_option == Library.Nonlinearity:
                nonlinearity = True
                X1 = Library.SPECIFICATION.get(part).get("Dataset")[0]
                X2 = Library.SPECIFICATION.get(part).get("Dataset")[1]
            if dataset != "":
                plotted_X = float(dataset)
            else:
                plotted_X = Library.SPECIFICATION.get(part).get("Dataset")[0]

            self.X_list.clear()
            self.Y_list.clear()
            oneMore = True
            Tid_Levels_dict = {self.get_num_TID(tid): tid for tid in Library.TID_LEVEL}
            Tid_Levels = [(k, Tid_Levels_dict[k]) for k in sorted(Tid_Levels_dict.keys())]
            for tid_level in range(500, 300000, 500):
                Tid_Levels_dict[tid_level] = str(tid_level / 1000) + 'k'

            for i in range(len(Tid_Levels)):
                num_TID = Tid_Levels[i][0]
                str_TID = Tid_Levels[i][1]
                if (num_TID < num_TID_lower and i + 1 < len(Tid_Levels) and Tid_Levels[i + 1][0] > num_TID_lower) or \
                        (num_TID_lower <= num_TID and (num_TID < num_TID_upper or oneMore)):
                    self.output_filepath = Main.relative_path(FILEPATHS.OUTPUT_DIR_PATH + part + '_' + str_TID + '_' + DR + '_' + H2 + '_' + '_' + bias +
                    datetime.datetime.now().strftime("%Y-%m-%d-%H:%M") + '.txt')
                    result = netListGenerator.generate(part, simulation, DR, H2, bias, temperature, str_TID, output_option,
                                              self.output_filepath, self.netlist_filepath)
                    if result == False:
                        continue
                    if num_TID >= num_TID_upper:
                        oneMore = False
                    my_result = execute.execute_module3(self.netlist_filepath)

                    # print(my_result)
                    X_label, Y_label, X, Y = self.load_and_finalize_output(part, str_TID)
                    self.X_list.append(num_TID)
                    lengthX = len(X)
                    if nonlinearity:
                        for i in range(len(X)):
                            if X[i] == X1:
                                Y1 = Y[i]
                            if X[i] == X2:
                                Y2 = Y[i]
                        self.Y_list.append(Y2 - Y1)
                    else:
                        for i in range(len(X)):
                            if X[i] == plotted_X:
                                self.Y_list.append(Y[i])
                                break
            unit = Library.SPECIFICATION.get(part).get(output_option)[2]    # read unit from library

            # post-processing for input bias
            if output_option == Library.Positive_Input_Bias_Current or output_option == Library.Negative_Input_Bias_Current:
                pre_rad_y = 0
                if Library.TPRE_RAD in self.X_list:
                    pre_rad_y = self.Y_list[0]
                else:
                    str_TID = Library.TPRE_RAD
                    self.output_filepath = Main.relative_path(FILEPATHS.OUTPUT_DIR_PATH + part + '_' + Library.TPRE_RAD + '_test.txt')
                    result = netListGenerator.generate(part, simulation, DR, H2, bias, temperature, str_TID, output_option,
                                                       self.output_filepath, self.netlist_filepath)
                    my_result = execute.execute_module3(self.netlist_filepath)
                    X_label, Y_label, X, Y = self.load_and_finalize_output(part, str_TID)
                    for i in range(len(X)):
                        if X[i] == plotted_X:
                            pre_rad_y = Y[i]
                            break
                tmp_list = [y - pre_rad_y for y in self.Y_list]
                self.Y_list = tmp_list

            # post-processing for nonlinearity
            elif output_option == Library.Nonlinearity:
                divider = 1e-6
                tmp_list = [y / divider for y in self.Y_list]
                self.Y_list = tmp_list

            # post-processing for temperature
            elif output_option == Library.TEMPERATURE:
                divider = 1e-6
                tmp_list = [y / divider - 273.15 for y in self.Y_list]
                # print(tmp_list)
                self.Y_list = tmp_list

            # post-processing for temperature_error
            elif output_option == Library.TEMPERATURE_ERROR:
                pre_rad_y = 0
                divider = 1e-6
                if Library.TPRE_RAD in self.X_list:
                    pre_rad_y = self.Y_list[0]
                else:
                    str_TID = Library.TPRE_RAD
                    self.output_filepath = Main.relative_path(
                        FILEPATHS.OUTPUT_DIR_PATH + part + '_' + Library.TPRE_RAD + '_test.txt')
                    result = netListGenerator.generate(part, simulation, DR, H2, bias, temperature, str_TID, output_option,
                                                       self.output_filepath, self.netlist_filepath)
                    my_result = execute.execute_module3(self.netlist_filepath)
                    X_label, Y_label, X, Y = self.load_and_finalize_output(part, str_TID)
                    for i in range(len(X)):
                        if X[i] == plotted_X:
                            pre_rad_y = Y[i]
                            break

                tmp_list = [(y - pre_rad_y) / divider for y in self.Y_list]
                # print(tmp_list)
                self.Y_list = tmp_list

            # prepare data for plotting
            Y_label = output_option + ' (' + unit + ')'
            if len(self.X_list) == 0 or len(self.Y_list) == 0:
                message = "No result to show"
                self.result_text.set(message)
                return
            label_name = part + '_' + DR + '_' + H2 + '_' + bias + '_' + temperature + '_' + dataset
            self.figure_input.clear()
            self.figure_input.extend(['TID level (rad)', Y_label, self.X_list, self.Y_list, part, simulation, label_name,
                                      num_TID_lower, num_TID_upper, TID_level_lower, TID_level_upper, None, None,
                                      spec_min, spec_max, False, False])
            self.plotfigureTK(self.figure_input[0], self.figure_input[1], self.figure_input[2], self.figure_input[3],
                              self.figure_input[4], self.figure_input[5], self.figure_input[6], self.figure_input[7],
                              self.figure_input[8], self.figure_input[9], self.figure_input[10], self.figure_input[11],
                              self.figure_input[12], self.figure_input[13], self.figure_input[14], self.figure_input[15],
                              self.figure_input[16])
            cross_min, cross_max = self.get_cross_points(self.X_list, self.Y_list, spec_min, spec_max)
            cross_message = ""
            next_line = ""
            if len(cross_min) != 0:
                cross_message += "Cross min at " + ",".join(cross_min) + " rad (DR=" + DR + ", H2=" + H2 + ", Bias=" + bias + "). "
                next_line = "\n"
            if len(cross_max) != 0:
                cross_message += next_line
                cross_message += "Cross max at " + ",".join(cross_max) + " rad (DR=" + DR + ", H2=" + H2 + ", Bias=" + bias + "). "
            if cross_message == "":
                cross_message = "Cross specification at > " + TID_level_upper + " rad (DR=" + DR + ", H2=" + H2 + ", Bias=" + bias + "). "
            message = 'part: ' + part + ', TID level = ' + TID_level_lower + ' ~ ' + TID_level_upper + '\n'

            # message = my_result
            if self.multiplot:
                if len(self.cross_message) == 4:
                    self.cross_message.pop(0)
                self.cross_message.append(cross_message)
            else:
                self.cross_message.clear()
                self.cross_message.append(cross_message)
            display_message = ''
            for cur_message in self.cross_message:
                display_message += cur_message + "\n"
            self.cross_spec_text.set(display_message)
            self.result_text.set(message)
            self.switch_availability_check(part)

        # except Exception as error:
        #     print(error)
        #     self.result_text.set('Error! Do you have ' + str(error) + ' data in excel?')
        return

    # find all of the cross specification points
    def get_cross_points(self, X_list, Y_list, spec_min, spec_max, useDouble=False):
        # calculate the point that exceed specification limits
        cross_min = []
        cross_max = []
        if spec_min is not None:
            if max(Y_list) > spec_min and min(Y_list) < spec_min:
                for index in range(len(Y_list) - 1):
                    y1 = Y_list[index]
                    y2 = Y_list[index + 1]
                    if (y1 < spec_min and y2 >= spec_min) or (y1 > spec_min and y2 <= spec_min):
                        x1 = X_list[index]
                        x2 = X_list[index + 1]
                        cross = self.get_cross_point(x1, y1, x2, y2, spec_min)
                        # print(cross)
                        if useDouble:
                            cross_min.append(str(round(cross, 3)))
                        else:
                            cross_min.append(str(int(cross)))
        if spec_max is not None:
            if max(Y_list) > spec_max and min(Y_list) < spec_max:
                for index in range(len(Y_list) - 1):
                    y1 = Y_list[index]
                    y2 = Y_list[index + 1]
                    if (y1 < spec_max and y2 >= spec_max) or (y1 > spec_max and y2 <= spec_max):
                        x1 = X_list[index]
                        x2 = X_list[index + 1]
                        cross = self.get_cross_point(x1, y1, x2, y2, spec_max)
                        if useDouble:
                            cross_max.append(str(round(cross, 3)))
                        else:
                            cross_max.append(str(int(cross)))
                        # print(cross)
        return cross_min, cross_max

    # calculate the X value of the cross specification point
    def get_cross_point(self, x1, y1, x2, y2, spec_line):
        y1 -= spec_line
        y2 -= spec_line
        a = (y2 - y1) / (x2 - x1)
        b = y2 - a * (x2)
        result = - (b / a)
        return result

    # refresh the program to get all the up-to-date data from library
    def refresh(self):
        importlib.reload(Library)
        self.parts_options_tuple = (Library.PARTS)
        self.cb_parts['values'] = self.parts_options_tuple
        self.simulation_options_tuple = (Library.SIMULATION)
        self.cb_simulation['values'] = self.simulation_options_tuple
        self.clear_specs()
        self.entry_dataset.delete(0, 'end')
        self.entry_temperature.delete(0, 'end')
        self.entry_TID_lower_bound.delete(0, 'end')
        self.entry_TID_upper_bound.delete(0, 'end')
        self.getClearGraph()

        self.cb_parts.set('TL431')
        self.cb_simulation.set(Library.SIMULATION_SOURCE)
        self.output_options_tuple = (list(Library.OUTPUT_NAME.get('TL431')))
        self.cb_output['values'] = self.output_options_tuple
        self.cb_output.set('Vref')
        self.cb_dose.set('0.02')
        self.cb_hydrogen.set('1.3')
        self.cb_bias.set('0')
        self.entry_temperature.insert(0, "27")
        # self.label_dataset_range['text'] = "VCC:(0~25, step=1)"
        # self.entry_dataset.insert(0, "25")
        # self.label_spec_min_value['text'] = 2.44
        # self.label_spec_max_value['text'] = 2.55
        self.label_spec_max_unit['text'] = 'V'
        self.label_spec_min_unit['text'] = 'V'
        self.entry_TID_lower_bound.insert(0, "0")
        self.entry_TID_upper_bound.insert(0, "300k")
        return

    # check if the input is valid
    def input_check(self):
        if self.entry_TID_upper_bound.get() == '' or \
                self.entry_TID_upper_bound.get() == '' or \
                self.cb_parts.get() == '' or \
                self.cb_simulation.get() == '' or \
                self.cb_dose.get() == '' or \
                self.cb_hydrogen.get() == '' or \
                self.cb_output.get() == '':
            self.result_text.set('please check your input')
            messagebox.showerror("Input Missing", "please check your input")
            return False
        # data = [("0","0.02"), ("0","100"), ("1.3", "0.02"), ("1", "0.1"), ("1", "100"), ("100", "0.1"), ("100", "100")]
        my_t = "DR=" + self.cb_dose.get() + "_H2=" + self.cb_hydrogen.get() + "_B=" + self.cb_bias.get()
        data1 = xlrd.open_workbook(FILEPATHS.NPN_IB_DATABASE_FILE_PATH)
        data2 = xlrd.open_workbook(FILEPATHS.PNP_IB_DATABASE_FILE_PATH)
        exist_data = [sheet_name for sheet_name in data1.sheet_names() if sheet_name in data2.sheet_names()]
        if my_t not in exist_data:
            message = "please choose Dose Rate, Hydrogen Content and Bias from one of the following:\n"
            for data in exist_data:
                addon = data + ", "
                message += addon
            messagebox.showerror("No Such Data", message[:-2])
            return False
        self.result_text.set('in process, please wait...')
        return True

    # update the TID options, not in use in current version
    def TID_option_update(self):
        cur_sim = self.cb_simulation.get()
        self.TID_options_tuple = Library.TID_LIST[cur_sim]
        self.TID_options_lower.set('')
        self.TID_options_upper.set('')
        self.cb_TID_lower_bound['values'] = self.TID_options_tuple
        self.cb_TID_upper_bound['values'] = self.TID_options_tuple

    # change spec min and spec max when user edit the temperature
    def temp_focus_out(self, evt):
        self.temp_focus_out_helper()
        return

    def temp_focus_out_helper(self):
        temp = self.entry_temperature.get()
        if temp != '':
            self.AD590_base_temperature = float(temp)
            self.AD590_spec_change()
        return

    # change spec min and spec max based on the input
    def AD590_spec_change(self):
        if self.cb_parts.get() == Library.PART_AD590 and self.cb_output.get() == Library.TEMPERATURE:
            self.label_spec_min_value['text'] = self.AD590_base_temperature - 5
            self.label_spec_max_value['text'] = self.AD590_base_temperature + 5
        return

    # check if the selected part should have switch button
    def switch_availability_check(self, part):
        if part == Library.PART_LT1175 or part == Library.PART_LP2953 or part == Library.PART_LM3940:
            self.frame_switch_button.grid(row=10, column=1)
        else:
            self.frame_switch_button.grid_remove()
        return

    # update the output options when a part is selected
    def part_onselect(self, evt):
        try:
            part = self.cb_parts.get()
            self.output_options_tuple = (list(Library.OUTPUT_NAME.get(part)))
            self.cb_output['values'] = self.output_options_tuple
            self.output_options.set('')
            self.clear_specs()
            self.clear_dataset()
            self.cb_parts.selection_clear()
        except:
            pass
        return

    # update TID options when a simulation type is selected, not in use in current version
    def simulation_onselect(self, evt):
        # try:
        #     self.TID_option_update()
        # except:
        #     pass
        return

    # update dataset and spec min/max when a specification is selected
    def output_onselect(self, evt):
        part = self.cb_parts.get()
        output = self.cb_output.get()
        if Library.INPUT.get(part + output) is not None:
            input_lib = Library.INPUT.get(part + output)
        else:
            input_lib = Library.INPUT.get(part)
        # dataset_range = input_lib[0].split(' ')[1] + ":(" + input_lib[0].split(' ')[2] + "~" + input_lib[0].split(' ')[3] + ", step=" + input_lib[0].split(' ')[4] + ")"
        dataset_range = "VCC:(" + input_lib[0].split(' ')[2] + "~" + input_lib[0].split(' ')[3] + ", step=" + input_lib[0].split(' ')[4] + ")"
        self.label_dataset_range['text'] = dataset_range
        spec_lib = Library.SPECIFICATION.get(part)
        self.clear_specs()
        if spec_lib is not None:
            spec = spec_lib.get(output)
            if spec is not None:
                if spec[0] is not None:
                    if 0 < abs(spec[0]) < 1e-2 or abs(spec[0]) > 1e2:
                        self.label_spec_min_value['text'] = "{0:.2e}".format(spec[0])
                    else:
                        self.label_spec_min_value['text'] = spec[0]
                if spec[1] is not None:
                    if 0 < abs(spec[1]) < 1e-2 or abs(spec[1]) > 1e2:
                        self.label_spec_max_value['text'] = "{0:.2e}".format(spec[1])
                    else:
                        self.label_spec_max_value['text'] = spec[1]
                self.AD590_spec_change()
                self.label_spec_max_unit['text'] = spec[2]
                self.label_spec_min_unit['text'] = spec[2]
            dataset = spec_lib.get("Dataset")
            if dataset is not None:
                self.entry_dataset.delete(0, 'end')
                self.entry_dataset.insert(0, dataset[0])
        self.cb_output.selection_clear()
        return

    # plot the data if a tid level is selected
    # only in use under switched plot mode
    def switch_tid_onselect(self, evt):
        tid = self.cb_switch_tid.get()
        self.plot_switched_figure_for_tid(tid)

    # clear all the specification max and min values
    def clear_specs(self):
        self.label_spec_min_value['text'] = ''
        self.label_spec_max_value['text'] = ''
        self.label_spec_max_unit['text'] = ''
        self.label_spec_min_unit['text'] = ''
        return

    # clear the dataset values
    def clear_dataset(self):
        self.label_dataset_range['text'] = ''
        self.entry_dataset.delete('0', 'end')
        return

    # callback function when ENTER is hit
    def callback(self, event):
        self.execute_hit()
        return

    # get the numeric TID value for a given str TID
    def get_num_TID(self, str_TID):
        if str_TID == Library.TPRE_RAD:
            return 0
        num_TID = float(re.findall(r"\d+\.?\d*", str_TID)[0])
        if str_TID.find("k") != -1:
            num_TID = num_TID * 1000
        return num_TID

    # start the GUI interface
    def start(self):
        # row 0
        row = 0
        # self.label_topline.grid(row=row, columnspan=3)

        # row 1
        row += 1
        self.frame_part.grid(row=row, column=1, rowspan=8, pady=(10, 0))
        self.frame_environment.grid(row=row, column=2, rowspan=2, columnspan=5, padx=(0, 10), pady=(10, 0))
        # self.label_input_header.grid(row=row, rowspan=3)

        # frame_part layouts
        self.frame_part_help.grid(row=0, column=1)
        self.cb_parts.grid(row=1, column=1)
        self.label_output.grid(row=2, column=1, pady=(20, 0))
        self.cb_output.grid(row=3, column=1)
        self.label_dataset.grid(row=4, column=1, pady=(20, 0))
        self.label_dataset_range.grid(row=5, column=1)
        self.entry_dataset.grid(row=6, column=1)
        self.frame_max.grid(row=7, column=1)
        self.frame_min.grid(row=8, column=1)

        # frame part help layout
        self.label_parts.grid(row=0, column=1)
        self.button_part_help.grid(row=0, column=2)

        # frame_max layout
        self.label_spec_max.grid(row=0, column=1)
        self.label_spec_max_value.grid(row=0, column=2)
        self.label_spec_max_unit.grid(row=0, column=3)

        # frame_min layout
        self.label_spec_min.grid(row=0, column=1)
        self.label_spec_min_value.grid(row=0, column=2)
        self.label_spec_min_unit.grid(row=0, column=3)

        # self.label_simulation.grid(row=row, column=2)

        # frame_environment layouts
        self.label_dose.grid(row=0, column=1)
        self.label_hydrogen.grid(row=0, column=2)
        self.label_bias.grid(row=0, column=3)
        self.label_temperature.grid(row=0, column=4)
        self.label_TID_level_lower_bound.grid(row=0, column=5)
        self.label_TID_level_upper_bound.grid(row=0, column=6)
        self.cb_dose.grid(row=1, column=1, padx=(5, 0), pady=(0, 5))
        self.cb_hydrogen.grid(row=1, column=2)
        self.cb_bias.grid(row=1, column=3)
        self.entry_temperature.grid(row=1, column=4)
        self.entry_TID_lower_bound.grid(row=1, column=5)
        self.entry_TID_upper_bound.grid(row=1, column=6)


        # row 2
        row += 1
        # self.cb_simulation.grid(row=row, column=2)
        # self.cb_TID_lower_bound.grid(row=row, column=2)
        # self.cb_TID_upper_bound.grid(row=row, column=3)

        # row 3
        # row += 1

        # row 4
        # row += 1
        # self.button_import.grid(row=row, column=2, pady=10)

        # row 3
        row += 1

        # row 4
        row += 1
        self.canvas_plot.grid(row=row - 1, column=2, rowspan=9, columnspan=5)

        row += 1

        # row 5
        row += 1
        # self.label_spec_header.grid(row=row, column=0, rowspan=2, pady=(20, 0))

        # row 6
        row += 1

        # row 7
        row += 1

        # row 8
        row += 1

        # row 9
        row += 1
        # self.frame_switch_button.grid(row=row, column=1)
        self.button_switch.grid(row=0, column=1)
        self.empty.grid(row=0, column=2)
        # self.label_spec_min_value.grid(row=row, column=1)

        # row 10
        row += 1
        self.frame_execute_or_change_scale.grid(row=row, column=1)

        # frame_execute_or_change_scale layout
        self.button_execute.grid(row=0, column=1, pady=10)
        self.button_change_scale.grid(row=0, column=2)

        # row 11
        row += 1
        self.frame_save_or_clear.grid(row=row, column=1)

        # frame_save_or_clear layout
        self.button_save.grid(row=0, column=1)
        self.button_clear.grid(row=0, column=2)
        # self.button_save.grid(row=row, column=1)

        # row 12
        row += 1

        # row 13
        row += 1
        self.label_result_text.grid(row=row, column=1, columnspan=2)
        self.label_cross_spec_text.grid(row=row, column=3, columnspan=3)

        self.button_execute.focus_set()
        # bind onselect function with widget
        self.entry_temperature.bind('<FocusOut>', self.temp_focus_out)
        self.cb_parts.bind('<<ComboboxSelected>>', self.part_onselect)
        self.cb_simulation.bind('<<ComboboxSelected>>', self.simulation_onselect)
        self.cb_output.bind('<<ComboboxSelected>>', self.output_onselect)
        self.cb_switch_tid.bind('<<ComboboxSelected>>', self.switch_tid_onselect)
        self.window.bind('<Return>', self.callback)
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        testmode = True
        if testmode is True:
            self.cb_parts.set('TL431')
            self.cb_simulation.set(Library.SIMULATION_SOURCE)
            self.output_options_tuple = (list(Library.OUTPUT_NAME.get('TL431')))
            self.cb_output['values'] = self.output_options_tuple
            self.cb_output.set('Vref')
            self.cb_dose.set('0.02')
            self.cb_hydrogen.set('1.3')
            self.cb_bias.set('0')
            self.entry_temperature.insert(0, "27")
            self.label_dataset_range['text'] = "VCC:(0~25, step=1)"
            self.entry_dataset.insert(0, "25")
            self.label_spec_min_value['text'] = 2.44
            self.label_spec_max_value['text'] = 2.55
            self.label_spec_max_unit['text'] = 'V'
            self.label_spec_min_unit['text'] = 'V'
            self.entry_TID_lower_bound.insert(0, "0")
            self.entry_TID_upper_bound.insert(0, "300k")
        else:
            self.cb_simulation.set(Library.SIMULATION_SOURCE)
            self.button_import.grid_remove()

        # screenwidth = self.window.winfo_screenwidth()
        # screenheight = self.window.winfo_screenheight()
        # interfacewidth = self.window.winfo_screenmmwidth()
        # interfaceheight = self.window.winfo_reqheight()
        #
        # size = '%dx%d+%d+%d' % (interfacewidth, interfaceheight, (screenwidth - interfacewidth) / 2, (screenheight - interfaceheight) / 2)
        # self.window.geometry(size)
        self.getClearGraph()

        if Library.import_error:
            messagebox.showwarning("Library Error", "Error occurs in the library! Automatically reset the library to initial values.")
        self.window.mainloop()
        return

    # quit message box before closing the GUI
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.window.destroy()
            self.window.quit()
        return

    # read all data from output files generated by Xyce
    def load_and_finalize_output(self, part, TID_level, costom_output_filepath=False):

        X_label = ''
        Y_label = ''
        XnY = []
        X = []
        Y = []
        if costom_output_filepath:
            prefix = part + '_' + TID_level
            output_folder = Main.relative_path(FILEPATHS.OUTPUT_DIR_PATH)
            for file in os.listdir(output_folder):
                if file[0:len(prefix)] == prefix:
                    output_filepath = output_folder + '/' + file
                else:
                    continue
        else:
            output_filepath = self.output_filepath
        f = open(output_filepath, 'r')
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

    # put switch tid combobox
    # only in use under switched mode
    def cb_switch_tid_put(self):
        self.empty.grid_remove()
        self.cb_switch_tid.grid(row=0, column=2, padx=(8,0))
        return

    # remove switch tid combobox
    def cb_switch_tid_remove(self):
        self.cb_switch_tid.grid_remove()
        self.empty.grid(row=0, column=2)
        return

    # plot figure in a pop up window
    def plotfigure(self, X_label, Y_label, X, Y, part, simulation, TID_level, TID_level2=None, spec_min=None, spec_max=None):
        plt.figure(part + simulation + ' X=' + X_label + ' Y=' + Y_label, figsize=self.figsize)
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

    # plot figure in the main GUI
    def plotfigureTK(self, X_label, Y_label, X, Y, part, simulation, label_name, X_min, X_max, TID_level, TID_level2=None,
                     Y_min=None, Y_max=None, spec_min=None, spec_max=None, x_logscale=False, y_logscale=False):
        # preprocessing input
        font = {'size': 10}
        matplotlib.rc('font', **font)
        if X_min > X_max:
            tmp = X_min
            X_min = X_max
            X_max = tmp
        if Y_min is not None and Y_max is not None:
            if Y_min > Y_max:
                tmp = Y_min
                Y_min = Y_max
                Y_max = tmp
        if part != self.previous_part or Y_label != self.previous_Y_label:
            self.figure.clf()
            self.multiplot = False
        else:
            self.multiplot = True
        self.previous_part = part
        self.previous_Y_label = Y_label
        subplot = self.figure.add_subplot(111)
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
        # scientific formatter
        # formatter = ticker.ScalarFormatter()
        # formatter.set_scientific(True)
        # formatter.set_powerlimits((-1,1))
        # subplot.yaxis.set_major_formatter(formatter)
        if len(Y) != 0:
            y_min = min(Y)
            y_max = max(Y)
            # set the data range where we use scientific format on y axis
            if 0 < max(abs(y_max), abs(y_min)) < 1e-2 or max(abs(y_max), abs(y_min)) > 1e2:
                subplot.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.2e'))
            if spec_max is not None:
                subplot.axhline(y=spec_max, color='r', linestyle='--')
                y_max = max(y_max, spec_max)
            if spec_min is not None:
                subplot.axhline(y=spec_min, color='r', linestyle='--')
                y_min = min(y_min, spec_min)
            subplot.plot(X, Y, next(self.color_gen), label=label_name)
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
        subplot.legend(loc='best', fancybox=True, framealpha=0.2)

        figure_canvas_agg = FigureCanvasAgg(self.figure)
        figure_canvas_agg.draw()
        figure_x, figure_y, figure_w, figure_h = self.figure.bbox.bounds
        figure_w, figure_h = int(figure_w), int(figure_h)
        photo = PhotoImage(master=self.canvas_plot, width=figure_w, height=figure_h)
        self.canvas_plot.create_image(figure_w / 2, figure_h / 2, image=photo)
        self.image = photo  # make a reference to our plot. If not, the image will disappear because Python's garbage collection is like shit
        tkagg.blit(photo, figure_canvas_agg.get_renderer()._renderer, colormode=2)
        # self.canvas_plot = FigureCanvasTkAgg(figure, self.window)
        # self.canvas_plot.show()
        # self.canvas_plot.get_tk_widget().grid(row=4, column=2, rowspan=10, columnspan=4, padx=(20,0))
        return

    # plot the switched graph in GUI
    def plot_switched_figure_for_tid(self, str_TID):
        X_label, Y_label, X, Y = self.load_and_finalize_output(self.figure_input[4], str_TID, costom_output_filepath=True)
        X_label = 'ILOAD (A)'
        Y_label = self.figure_input[1]
        label_name = self.figure_input[6][0:self.figure_input[6].rfind('_') + 1] + str_TID
        spec_min = self.figure_input[13]
        spec_max = self.figure_input[14]
        cross_min, cross_max = self.get_cross_points(X, Y, spec_min, spec_max, useDouble=True)

        cross_message = ""
        next_line = ""
        ending = ". (TID=" + str_TID + ")"
        if len(cross_min) != 0:
            cross_message += "Cross min at " + X_label + " = " + ",".join(cross_min) + ending
            next_line = "\n"
        if len(cross_max) != 0:
            cross_message += next_line
            cross_message += "Cross max at " + X_label + " = " + ",".join(cross_max) + ending
        if cross_message == "":
            cross_message = "Cross specification at > " + str(max(X)) + ending

        if len(self.switched_cross_message) == 4:
            self.switched_cross_message.pop(0)
        self.switched_cross_message.append(cross_message)
        display_message = ''
        for cur_message in self.switched_cross_message:
            display_message += cur_message + "\n"

        self.cross_spec_text.set(display_message)
        self.plot_switched_figureTK(X_label, Y_label, X, Y, label_name, spec_min=spec_min, spec_max=spec_max)

    # plot the graph using tk
    def plot_switched_figureTK(self, X_label, Y_label, X, Y, label_name, spec_min=None, spec_max=None, x_logscale=False, y_logscale=False):
        # preprocessing input
        font = {'size': 10}
        matplotlib.rc('font', **font)
        subplot = self.figure.add_subplot(111)
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
        if len(Y) != 0:
            y_min = min(Y)
            y_max = max(Y)
            # set the data range where we use scientific format on y axis
            if 0 < max(abs(y_max), abs(y_min)) < 1e-2 or max(abs(y_max), abs(y_min)) > 1e2:
                subplot.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.2e'))
            if spec_max is not None:
                subplot.axhline(y=spec_max, color='r', linestyle='--')
                y_max = max(y_max, spec_max)
            if spec_min is not None:
                subplot.axhline(y=spec_min, color='r', linestyle='--')
                y_min = min(y_min, spec_min)
            subplot.plot(X, Y, next(self.color_gen), label=label_name)
            # subplot.plot(X, Y, 'r*')
        subplot.set_xlabel(X_label)
        subplot.set_ylabel(Y_label)
        subplot.legend(loc='best', fancybox=True, framealpha=0.2)

        figure_canvas_agg = FigureCanvasAgg(self.figure)
        figure_canvas_agg.draw()
        figure_x, figure_y, figure_w, figure_h = self.figure.bbox.bounds
        figure_w, figure_h = int(figure_w), int(figure_h)
        photo = PhotoImage(master=self.canvas_plot, width=figure_w, height=figure_h)
        self.canvas_plot.create_image(figure_w / 2, figure_h / 2, image=photo)
        self.image = photo  # make a reference to our plot. If not, the image will disappear because Python's garbage collection is like shit
        tkagg.blit(photo, figure_canvas_agg.get_renderer()._renderer, colormode=2)
        return

    # change the scale of the graph
    def plot_scale(self, X_max, X_min, Y_max, Y_min, x_logscale, y_logscale):
        if X_min is not None and X_max is not None:
            if X_min > X_max:
                tmp = X_min
                X_min = X_max
                X_max = tmp
        if Y_min is not None and Y_max is not None:
            if Y_min > Y_max:
                tmp = Y_min
                Y_min = Y_max
                Y_max = tmp
        subplot = self.figure.add_subplot(111)
        if x_logscale is True:
            subplot.set_xscale('symlog')
        else:
            subplot.set_xscale('linear')
        if y_logscale is True:
            subplot.set_yscale('log', nonposy='clip')
        else:
            subplot.set_yscale('linear')

        if Y_min is not None and Y_max is not None:
            subplot.set_ylim([float(Y_min), float(Y_max)])
        elif Y_min is not None:
            subplot.set_ylim(ymin=float(Y_min))
        elif Y_max is not None:
            subplot.set_ylim(ymax=float(Y_max))

        if X_min is not None and X_max is not None and X_max != X_min:
            subplot.set_xlim([float(X_min), float(X_max)])
        elif X_min is not None:
            subplot.set_xlim(xmin=float(X_min))
        elif X_max is not None:
            subplot.set_xlim(xmax=float(X_max))

        figure_canvas_agg = FigureCanvasAgg(self.figure)
        figure_canvas_agg.draw()
        figure_x, figure_y, figure_w, figure_h = self.figure.bbox.bounds
        figure_w, figure_h = int(figure_w), int(figure_h)
        photo = PhotoImage(master=self.canvas_plot, width=figure_w, height=figure_h)
        self.canvas_plot.create_image(figure_w / 2, figure_h / 2, image=photo)
        self.image = photo  # make a reference to our plot. If not, the image will disappear because Python's garbage collection is like shit
        tkagg.blit(photo, figure_canvas_agg.get_renderer()._renderer, colormode=2)
        return

    # change the scale of the graph
    def change_scale(self):
        if len(self.figure_input) != 0:
            changeScaleDialog = ChangeScaleWindow.ChangeScaleWindow()
            self.window.wait_window(changeScaleDialog)
            try:
                scaleinfo = changeScaleDialog.scaleinfo
                if scaleinfo is None:
                    return
            except:
                return
            x_upper, x_lower, x_log, y_upper, y_lower, y_log = scaleinfo
            x_upper = self.get_num_TID(x_upper) if x_upper != '' else None
            x_lower = self.get_num_TID(x_lower) if x_lower != '' else None
            y_upper = y_upper if y_upper != '' else None
            y_lower = y_lower if y_lower != '' else None

            if self.switched_plot:
                self.plot_scale(x_upper, x_lower, y_upper, y_lower, x_log, y_log)
            else:
                # x upper bound
                if x_upper is not None:
                    self.figure_input[8] = x_upper
                # x lower bound
                if x_lower is not None:
                    self.figure_input[7] = x_lower
                # x log scale
                if min(self.figure_input[3]) <= 0 and y_log is True:
                    self.result_text.set("can not use log scale on y axis \n non-positive value detected")
                else:
                    self.figure_input[16] = y_log
                # y upper bound
                self.figure_input[12] = y_upper
                # y lower bound
                self.figure_input[11] = y_lower
                # y log scale
                self.figure_input[15] = x_log

                self.plot_scale(self.figure_input[8], self.figure_input[7], self.figure_input[12], self.figure_input[11], self.figure_input[15], self.figure_input[16])
        return

    # save the output in a xlsx file
    def save_hit(self):
        if len(self.figure_input) == 0:
            messagebox.showinfo("Failed", "Please run a simulation first before save data")
            return
        if self.multiplot is True:
            messagebox.showinfo("Failed", "Can not save data when multiplot")
            return
        path = Main.relative_path(FILEPATHS.OUTPUT_DIR_PATH)
        files = os.listdir(path)
        part_name = ''
        DR = ''
        H2 = ''
        time = ''

        TIDs = []
        try:
            for file in files:
                if file[-4:] == ".txt":
                    filename_aray = file[0:-4].split('_')
                    part_name = filename_aray[0]
                    TIDs.append(filename_aray[1])
                    DR = filename_aray[2]
                    H2 = filename_aray[3]
                    time = filename_aray[4]
        except:
            return
        result_path = Main.relative_path(FILEPATHS.OUTPUT_DIR_PATH + part_name + '_' + DR + '_' + H2 + '_' + time + '.xlsx')
        assign_col = 0
        col_dict = {}
        for TID_option in Library.TID_LEVEL:
            if TIDs.count(TID_option) != 0:
                col_dict[TID_option] = assign_col
                assign_col += 3

        workbook = xlsxwriter.Workbook(result_path)
        worksheet = workbook.add_worksheet(part_name)
        for file in files:
            if file[-4:] != ".txt":
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
                my_line = list(filter(self.not_empty, my_line))
                if my_line[0] == 'End':
                    break
                if X_label == '' and Y_label == '':
                    X_label = my_line[0]
                    Y_label = my_line[1]
                else:
                    X.append(float(my_line[0]))
                    Y.append(float(my_line[1]))
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
        message = 'File saved at ./' + FILEPATHS.OUTPUT_DIR_PATH + part_name +'.xlsx'
        self.result_text.set(message)
        return

    # check if the given str is not empty
    def not_empty(self, s):
        return s and s.strip() != ''

    # clear all data and user input
    def clear(self):
        if (self.switched_plot):
            self.switch_hit()
        self.figure.clf()
        self.getClearGraph()
        self.previous_part = ''
        self.previous_Y_label = ''
        self.result_text.set('')
        self.cross_spec_text.set('')
        figure_canvas_agg = FigureCanvasAgg(self.figure)
        figure_canvas_agg.draw()
        figure_x, figure_y, figure_w, figure_h = self.figure.bbox.bounds
        figure_w, figure_h = int(figure_w), int(figure_h)
        photo = PhotoImage(master=self.canvas_plot, width=figure_w, height=figure_h)
        self.canvas_plot.create_image(figure_w / 2, figure_h / 2, image=photo)
        self.image = photo  # make a reference to our plot. If not, the image will disappear because Python's garbage collection is like shit
        tkagg.blit(photo, figure_canvas_agg.get_renderer()._renderer, colormode=2)

    # clear all the content on the graph
    def getClearGraph(self):
        self.figure_input.clear()
        self.plotfigureTK('TID level (rad)', "", [], [], "", "", "", 0, 300000, "0", "300k", None, None, None, None, False, False)
        self.result_text.set('')
        self.cross_spec_text.set('')
        self.cross_message.clear()
        self.switched_cross_message.clear()

# initialize all necessary classes
execute = execute.Execute()
netListGenerator = NetListGenerator.NetListGenerator()
execute.mkdirs()
