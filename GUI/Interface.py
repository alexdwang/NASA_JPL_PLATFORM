import tkinter
from GUI import execute

class Interface(object):
    def __init__(self):
        self.window = tkinter.Tk()
        self.window.title('Platform')
        self.window.geometry('1000x700')
        self.result_text = tkinter.StringVar()

        # self.entry = tkinter.Entry(self.window, show=None, )
        # self.text = tkinter.Text(self.window)

        # self.var1=tkinter.StringVar()
        # self.var2=tkinter.StringVar()
        # self.var2.set((11,22,33,44))
        # self.l = tkinter.Label(self.window, bg='yellow', width=4, textvariable=self.var1)
        # self.lb = tkinter.Listbox(self.window, listvariable=self.var2)

        self.var = tkinter.StringVar()
        self.l = tkinter.Label(self.window, bg='yellow', width=34, text='empty')
        pass

    def execute_hit(self):
        my_result = execute.execute_module3()
        self.result_text.set(my_result)
        pass

    # def insert_point(self):
    #     var = self.entry.get()
    #     self.text.insert('insert',var)
    #     pass
    #
    # def insert_end(self):
    #     var = self.entry.get()
    #     self.text.insert('end',var)
    #     pass

    # def print_selection(self):
    #     value = self.lb.get(self.lb.curselection())
    #     self.var1.set(value)
    #     pass

    # def print_selection(self):
    #     self.l.config(text='you have selected ' + self.var.get())
    #     pass

    def start(self):

        label_topline = tkinter.Label(self.window, text='NASA JPL', font=('Arial', 12), width=10, height=2)
        button = tkinter.Button(self.window, text='Execute', width=15, height=2, command=self.execute_hit)
        label_result_text = tkinter.Label(self.window, textvariable=self.result_text, font=('Arial', 12), width=900, height=600)

        # lecture 2 entry / text:
        # b1 = tkinter.Button(self.window, text='insert point', width=15, height=2, command=self.insert_point)
        # b2 = tkinter.Button(self.window, text='insert end', width=15, height=2, command=self.insert_end)
        #
        # self.entry.pack()
        # b1.pack()
        # b2.pack()
        # self.text.pack()

        # lecture 3 listbox:
        # b1 = tkinter.Button(self.window, text='print selection', width=15, height=2, command=self.print_selection)
        # list_items = [1,2,3,4]
        # for item in list_items:
        #     self.lb.insert('end', item)
        # self.lb.insert(1,'first')
        # self.lb.delete(5)
        #
        # self.l.pack()
        # b1.pack()
        # self.lb.pack()

        # lecture 4 radiobutton:
        # r1 = tkinter.Radiobutton(self.window, text='Option A', variable=self.var, value='A', command=self.print_selection, )
        # r2 = tkinter.Radiobutton(self.window, text='Option B', variable=self.var, value='B', command=self.print_selection)
        # r3 = tkinter.Radiobutton(self.window, text='Option C', variable=self.var, value='C', command=self.print_selection)
        # r1.pack()
        # r2.pack()
        # r3.pack()
        # self.l.pack()

        label_topline.pack()
        button.pack()
        label_result_text.pack()

        self.window.mainloop()

        pass

if __name__ == "__main__" :
    interface = Interface()
    execute = execute.Execute()
    interface.start()