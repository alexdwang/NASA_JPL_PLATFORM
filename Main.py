import matplotlib.pyplot as plt
import os
import tkinter
from GUI import execute, NetListGenerator, Library


class Interface(object):
    def __init__(self):
        self.window = tkinter.Tk()
        self.window.title('Platform')
        self.window.geometry('1000x500')

        self.label_topline = tkinter.Label(self.window, text=Library.TITLE, font=('Arial', 20), width=30, height=2)

        self.label_parts = tkinter.Label(self.window, text='parts:', font=('Arial', 0), width=16, height=2)
        self.parts_options = tkinter.StringVar()
        self.parts_options_tuple = (Library.PARTS)
        self.parts_options.set(self.parts_options_tuple)
        self.lb_parts = tkinter.Listbox(self.window, listvariable=self.parts_options, height=6, exportselection=False)

        self.label_simulation = tkinter.Label(self.window, text='simulation:', font=('Arial', 0), width=16, height=2)
        self.simulation_options = tkinter.StringVar()
        self.simulation_options_tuple = (Library.SIMULATION)
        self.simulation_options.set(self.simulation_options_tuple)
        self.lb_simulation = tkinter.Listbox(self.window, listvariable=self.simulation_options,
                                             height=6, exportselection=False)

        self.label_TID_level = tkinter.Label(self.window, text='TID level:', font=('Arial', 0), width=16, height=2)
        self.TID_options = tkinter.StringVar()
        self.TID_options_tuple = ()
        self.TID_options.set(self.TID_options_tuple)
        self.lb_TID = tkinter.Listbox(self.window, listvariable=self.TID_options,
                                      height=len(self.TID_options_tuple), exportselection=False)

        self.label_output = tkinter.Label(self.window, text='Output:', font=('Arial', 0), width=16, height=2)
        self.output_options = tkinter.StringVar()
        self.output_options_tuple = (Library.LT1175_OUTPUT_OPTION)
        self.output_options.set(self.output_options_tuple)
        self.lb_output = tkinter.Listbox(self.window, listvariable=self.output_options,
                                      height=len(self.output_options_tuple), exportselection=False)

        self.button = tkinter.Button(self.window, text='Execute', width=15, height=2, command=self.execute_hit)

        self.result_text = tkinter.StringVar()
        self.label_result_text = tkinter.Label(self.window, textvariable=self.result_text, font=('Arial', 12), width=80, height=5)

        self.netlist_filepath = relative_path('Netlist/test.cir')
        self.output_filepath = ''
        return

    def execute_hit(self):
        try:
            if self.input_check():
                part = self.lb_parts.get(self.lb_parts.curselection())
                simulation = self.lb_simulation.get(self.lb_simulation.curselection())
                TID_level = self.lb_TID.get(self.lb_TID.curselection())
                if (part == Library.PART_LT1175):
                    output_option = self.lb_output.get(self.lb_output.curselection())
                else:
                    output_option = Library.AD590_OUTPUT_OPTION[0]

                self.output_filepath = relative_path('Output/' + part + '_' + TID_level + '_test.txt')

                netListGenerator.generate(part, simulation, TID_level, output_option, self.output_filepath, self.netlist_filepath)
                my_result = execute.execute_module3(self.netlist_filepath)
                message = 'part: ' + part + ', TID level = ' + TID_level + '\n' + 'result file path = ' + self.output_filepath
                # message = my_result
                self.result_text.set(message)

                X_label, Y_label, X, Y = self.load_and_finalize_output(part, TID_level)
                self.plotfigure(X_label, Y_label, X, Y, part, TID_level)
        except Exception as error:
            print(error)
            self.result_text.set('Error! Do you have ' + str(error) + ' data in excel?')
        return

    def input_check(self):
        if self.lb_TID.curselection() == () or self.lb_parts.curselection() == () or self.lb_simulation.curselection() == () or \
                (self.lb_parts.get(self.lb_parts.curselection()) == Library.PART_LT1175 and self.lb_output.curselection() == ()):
            self.result_text.set('please check your input')
            return False
        self.result_text.set('in process, please wait...')
        return True

    def TID_option_update(self):
        cur_part = self.lb_parts.get(self.lb_parts.curselection())
        cur_sim = self.lb_simulation.get(self.lb_simulation.curselection())
        self.TID_options_tuple = Library.TID_LIST[cur_part][cur_sim]
        self.TID_options.set(self.TID_options_tuple)


    def part_onselect(self, evt):
        try:
            index = int(self.lb_parts.curselection()[0])
            value = self.lb_parts.get(index)
            if value == Library.PART_LT1175:
                self.label_output.grid()
                self.lb_output.grid()
            elif value == Library.PART_AD590:
                self.label_output.grid_remove()
                self.lb_output.grid_remove()
            self.TID_option_update()
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
        self.label_topline.grid(row=0, columnspan=3)

        self.lb_parts.bind('<<ListboxSelect>>', self.part_onselect)
        self.lb_simulation.bind('<<ListboxSelect>>', self.simulation_onselect)
        self.label_parts.grid(row=1)
        self.label_simulation.grid(row=1, column=1)
        self.label_TID_level.grid(row=1, column=2)
        self.label_output.grid(row=1, column=3)

        self.lb_parts.grid(row=2)
        self.lb_simulation.grid(row=2, column=1)
        self.lb_TID.grid(row=2, column=2)
        self.lb_output.grid(row=2, column=3)

        self.button.grid(row=3, sticky='E', columnspan=3, pady=10)

        self.label_result_text.grid(row=4, column=0, columnspan=3)

        self.label_output.grid_remove()
        self.lb_output.grid_remove()
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

    def plotfigure(self, X_label, Y_label, X, Y, part, TID_level):
        color = {Library.TPRE_RAD: 'r-',
                 Library.T2_5KRAD: 'y-',
                 Library.T5KRAD: 'c-',
                 Library.T10KRAD: 'c-',
                 Library.T20KRAD: 'y-',
                 Library.T30KRAD: 'g-',
                 Library.T50KRAD: 'c-',
                 Library.T100KRAD: 'g-',
                 Library.T200KRAD: 'm-',
                 Library.T300KRAD: 'k-'}
        figure_num = {Library.PART_LT1175: 1,
                      Library.PART_AD590: 2}
        location = {Library.PART_LT1175: 'upper left',
                      Library.PART_AD590: 'lower right'}
        plt.figure(figure_num[part], figsize=(8,8))
        plt.plot(X, Y, color[TID_level], label="Part=" + part + "TID level=" + TID_level)
        plt.xlabel(X_label)
        plt.ylabel(Y_label)
        # plt.plot(X, Y, 'b*')
        plt.legend(loc=location[part])
        plt.show()
        return


def relative_path(path):
    dirname = os.path.dirname(os.path.realpath('__file__'))
    path = os.path.join(dirname, path)
    return os.path.normpath(path)


if __name__ == "__main__":
    interface = Interface()
    execute = execute.Execute()
    netListGenerator = NetListGenerator.NetListGenerator()
    interface.start()




