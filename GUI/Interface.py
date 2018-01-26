import tkinter
from GUI import execute, NetListGenerator


class Interface(object):
    def __init__(self):
        self.window = tkinter.Tk()
        self.window.title('Platform')
        self.window.geometry('1000x700')
        self.result_text = tkinter.StringVar()
        self.label_topline = tkinter.Label(self.window, text='NASA JPL', font=('Arial', 12), width=10, height=2)
        self.button = tkinter.Button(self.window, text='Execute', width=15, height=2, command=self.execute_hit)
        self.label_result_text = tkinter.Label(self.window, textvariable=self.result_text, font=('Arial', 12), width=900, height=600)
        self.options = tkinter.StringVar()
        self.options.set(('pre_rad', '20k', '50k'))
        self.lb = tkinter.Listbox(self.window, listvariable=self.options)

        pass

    def execute_hit(self):
        if self.input_check():
            value = self.lb.get(self.lb.curselection())
            netListGenerator.generate(value)
            my_result = execute.execute_module3()
            self.result_text.set(my_result)
        pass

    def input_check(self):
        if self.lb.curselection() == ():
            return False
        return True

    def start(self):
        self.label_topline.pack()
        self.lb.pack()
        self.button.pack()
        self.label_result_text.pack()
        self.window.mainloop()

        pass


if __name__ == "__main__":
    interface = Interface()
    execute = execute.Execute()
    netListGenerator = NetListGenerator.NetListGenerator()
    interface.start()