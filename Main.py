import matplotlib.pyplot as plt
import os
import tkinter
from GUI import execute, NetListGenerator


class Interface(object):
    def __init__(self):
        self.window = tkinter.Tk()
        self.window.title('Platform')
        self.window.geometry('600x400')
        self.result_text = tkinter.StringVar()
        self.label_topline = tkinter.Label(self.window, text='NASA JPL', font=('Arial', 12), width=10, height=2)
        self.label_radiation = tkinter.Label(self.window, text='Radiation:                       ', font=('Arial', 0), width=21, height=2)
        self.options = tkinter.StringVar()
        self.options_tuple = ('pre_rad', '20k', '50k')
        self.options.set(self.options_tuple)
        self.lb = tkinter.Listbox(self.window, listvariable=self.options, height=3)
        self.button = tkinter.Button(self.window, text='Execute', width=15, height=2, command=self.execute_hit)
        self.label_result_text = tkinter.Label(self.window, textvariable=self.result_text, font=('Arial', 12), width=900, height=600)

        self.netlist_filepath = relative_path('Netlist/test.cir')
        self.output_filepath = ''
        return

    def execute_hit(self):
        if self.input_check():
            radiation = self.lb.get(self.lb.curselection())
            device = 'AD590'
            self.output_filepath = relative_path('Output/' + radiation + '_test.txt')

            netListGenerator.generate(radiation, self.output_filepath, self.netlist_filepath)
            my_result = execute.execute_module3(self.netlist_filepath)
            message = 'device: ' + device + ', radiation = ' + radiation + '\n' + 'result file path = ' + self.output_filepath
            self.result_text.set(message)

            X, Y = self.load_finalized_output(device, radiation)
            self.plotfigure(X, Y, radiation)
        return

    def input_check(self):
        if self.lb.curselection() == ():
            self.result_text.set('please check your radiation input')
            return False
        return True

    def start(self):
        self.label_topline.pack()
        self.label_radiation.pack()
        self.lb.pack()
        self.button.pack()
        self.label_result_text.pack()
        self.window.mainloop()
        return

    def load_finalized_output(self, device, radiation):
        f = open(self.output_filepath, 'r')
        lines = f.readlines()
        f.close()

        n = open(self.output_filepath, 'w')
        n.write('device: ' + device + ', radiation = ' + radiation + '\n')
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

    def plotfigure(self, X, Y, radiation):
        plt.figure(1, figsize=(8,6))
        # plt.plot(X, Y, 'b*')
        if radiation == self.options_tuple[0]:
            plt.plot(X, Y, 'r',label="X and Y, radiation=" + radiation)
        elif radiation == self.options_tuple[1]:
            plt.plot(X, Y, 'g', label="X and Y, radiation=" + radiation)
        elif radiation == self.options_tuple[2]:
            plt.plot(X, Y, 'y', label="X and Y, radiation=" + radiation)
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




