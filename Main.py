import matplotlib.pyplot as plt
import os
import tkinter
from GUI import execute, NetListGenerator, Library


class Interface(object):
    def __init__(self):
        self.window = tkinter.Tk()
        self.window.title('Platform')
        self.window.geometry('800x400')

        self.label_topline = tkinter.Label(self.window, text=Library.TITLE, font=('Arial', 12), width=10, height=2)

        self.label_parts = tkinter.Label(self.window, text='parts:', font=('Arial', 0), width=21, height=2)
        self.parts_options = tkinter.StringVar()
        self.parts_options_tuple = (Library.PARTS)
        self.parts_options.set(self.parts_options_tuple)
        self.lb_parts = tkinter.Listbox(self.window, listvariable=self.parts_options, height=6, exportselection=False)

        self.label_simulation = tkinter.Label(self.window, text='simulation:', font=('Arial', 0), width=21, height=2)
        self.simulation_options = tkinter.StringVar()
        self.simulation_options_tuple = (Library.SIMULATION)
        self.simulation_options.set(self.simulation_options_tuple)
        self.lb_simulation = tkinter.Listbox(self.window, listvariable=self.simulation_options,
                                             height=6, exportselection=False)

        self.label_TID_level = tkinter.Label(self.window, text='TID level:', font=('Arial', 0), width=21, height=2)
        self.TID_options = tkinter.StringVar()
        self.TID_options_tuple = ()
        self.TID_options.set(self.TID_options_tuple)
        self.lb_TID = tkinter.Listbox(self.window, listvariable=self.TID_options,
                                      height=len(self.TID_options_tuple), exportselection=False)

        self.button = tkinter.Button(self.window, text='Execute', width=15, height=2, command=self.execute_hit)

        self.result_text = tkinter.StringVar()
        self.label_result_text = tkinter.Label(self.window, textvariable=self.result_text, font=('Arial', 12), width=30, height=5)

        self.netlist_filepath = relative_path('Netlist/test.cir')
        self.output_filepath = ''
        return

    def execute_hit(self):
        if self.input_check():
            TID_level = self.lb_TID.get(self.lb_TID.curselection())
            part = self.lb_parts.get(self.lb_parts.curselection())
            self.output_filepath = relative_path('Output/' + TID_level + '_test.txt')

            netListGenerator.generate(part, TID_level, self.output_filepath, self.netlist_filepath)
            my_result = execute.execute_module3(self.netlist_filepath)
            message = 'part: ' + part + ', TID level = ' + TID_level + '\n' + 'result file path = ' + self.output_filepath
            self.result_text.set(message)

            X, Y = self.load_finalized_output(part, TID_level)
            self.plotfigure(X, Y, TID_level)
        return

    def input_check(self):
        if self.lb_TID.curselection() == () or self.lb_parts.curselection() == () or self.lb_simulation.curselection() == ():
            self.result_text.set('please check your input')
            return False
        self.result_text.set('in process, please wait...')
        return True

    def simulation_onselect(self, evt):
        try:
            index = int(self.lb_simulation.curselection()[0])
            value = self.lb_simulation.get(index)
            if value == Library.SIMULATION[0]:
                self.TID_options_tuple = (list(Library.TID_LEVEL_MODEL))
            elif value == Library.SIMULATION[1]:
                self.TID_options_tuple = (list(Library.TID_LEVEL_SOURCE))
            self.TID_options.set(self.TID_options_tuple)
        except:
            pass
        return

    def start(self):
        #     self.label_topline.pack()
        #     self.label_TIDlevel.pack()
        #     self.lb.pack()
        #     self.button.pack()
        #     self.label_result_text.pack()
        # self.label_topline.grid(row=0,sticky='E')
        self.lb_simulation.bind('<<ListboxSelect>>', self.simulation_onselect)
        self.label_parts.grid(row=0)
        self.label_simulation.grid(row=0, column=1)
        self.label_TID_level.grid(row=0, column=2)

        self.lb_parts.grid(row=1)
        self.lb_simulation.grid(row=1, column=1)
        self.lb_TID.grid(row=1, column=2)

        self.button.grid(row=2,sticky='E')

        self.label_result_text.grid(row=3,sticky='W')
        self.window.mainloop()
        return

    def load_finalized_output(self, device, TID_level):
        f = open(self.output_filepath, 'r')
        lines = f.readlines()
        f.close()

        n = open(self.output_filepath, 'w')
        n.write('device: ' + device + ', TID level = ' + TID_level + '\n')
        n.writelines(lines)

        XnY = []
        X = []
        Y = []
        cnt = 0
        for line in lines:
            line = line.strip('\n')
            my_line = line.split(' ')
            for word in my_line:
                if word != '':
                    try:
                        XnY.append(float(word))
                    except:
                        cnt += 1
        # print(lines)
        for i in range(len(XnY)):
            if i % 2 == 0:
                X.append(XnY[i])
            else:
                Y.append(XnY[i])
        return X, Y

    def plotfigure(self, X, Y, TID_level):
        plt.figure(1, figsize=(8,6))
        # plt.plot(X, Y, 'b*')
        if TID_level == self.TID_options_tuple[0]:
            plt.plot(X, Y, 'r', label="X and Y, TID level=" + TID_level)
        elif TID_level == self.TID_options_tuple[1]:
            plt.plot(X, Y, 'g', label="X and Y, TID level=" + TID_level)
        elif TID_level == self.TID_options_tuple[2]:
            plt.plot(X, Y, 'y', label="X and Y, TID level=" + TID_level)
            plt.plot(X, Y, 'y', label="X and Y, TID level=" + TID_level)
        plt.xlabel("V(1)")
        plt.ylabel("I(ROUT)")
        plt.legend(loc='lower right')

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




