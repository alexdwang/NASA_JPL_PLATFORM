import tkinter
from GUI import execute

class Interface(object):
    def __init__(self):
        self.window = tkinter.Tk()
        self.window.title('Platform')
        self.window.geometry('1000x700')
        self.result_text = tkinter.StringVar()
        pass
    def execute_hit(self):
        my_result = execute.execute_module3()
        self.result_text.set(my_result)
        pass

    def start(self):

        label_topline = tkinter.Label(self.window, text='NASA JPL', font=('Arial', 12), width=10, height=2)
        button = tkinter.Button(self.window, text='Execute', width=15, height=2, command=self.execute_hit)
        label_result_text = tkinter.Label(self.window, textvariable=self.result_text, font=('Arial', 12), width=900, height=600)

        label_topline.pack()
        button.pack()
        label_result_text.pack()

        self.window.mainloop()

        pass

if __name__ == "__main__" :
    interface = Interface()
    execute = execute.Execute()
    interface.start()