from tkinter import *
from GUI import Entry

class ChangeScaleWindow(Toplevel):
    def __init__(self):
        super().__init__()
        self.title('change scale')
        self.attributes('-topmost', 'true')
        element_width = 16
        my_font = ('Arial', 15)
        self.label_x_upper = Label(self, text='x upper bound(rad)', font=my_font, width=element_width)
        self.entry_x_upper = Entry.TIDEntry(self, width=element_width)
        self.label_x_lower = Label(self, text='x lower bound(rad)', font=my_font, width=element_width)
        self.entry_x_lower = Entry.TIDEntry(self, width=element_width)
        self.xlog = IntVar()
        self.checkbutton_x = Checkbutton(self, text="log scale x", font=my_font, variable=self.xlog)

        self.label_y_upper = Label(self, text='y upper bound', font=my_font, width=element_width)
        self.entry_y_upper = Entry.FloatEntry(self, width=element_width)
        self.label_y_lower = Label(self, text='y lower bound', font=my_font, width=element_width)
        self.entry_y_lower = Entry.FloatEntry(self, width=element_width)
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

