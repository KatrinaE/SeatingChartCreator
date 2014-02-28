"""
This code is based on the very helpful tutorial at
http://sebsauvage.net/python/gui/
"""
from Tkinter import Tk, Frame, Label, BOTH, Entry, StringVar
from Tkinter import *
import tkFileDialog
import ttk
import sys

import main2 as backend
from Temp_animation3 import thingy

class BaseWindow(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initialize()


    def initialize(self):
        self.centerWindow()
        self.grid_columnconfigure(0,weight=1)

        self.title = Label(self.parent, text="Welcome to Seating Chart Creator", fg="black",bg="lightblue")
        self.title.grid(row=0, column=0, columnspan=2)

        self.p_filename = StringVar()
        self.t_filename = StringVar()

        self.p_label = ttk.Label(self.parent, textvariable=self.p_filename, width=30)
        self.p_label.grid(row=1,column=0, sticky=(E))
        self.p_button = ttk.Button(self.parent, text='Choose People File',\
                                 command=self.get_ppl_filename)
        self.p_button.grid(row=1, column=1)

        self.t_label = ttk.Label(self.parent, textvariable=self.t_filename, width=30)
        self.t_label.grid(row=2, column=0)
        self.t_button = ttk.Button(self.parent, text='Choose Tables File',\
                                command=self.get_tables_filename)
        self.t_button.grid(row=2, column=1)

        # can we make this callback instantiate a new ProgressWindow widget
        # rather than calling backend.main directly?
        self.submit_button = ttk.Button(self.parent, text='Generate Seating Chart', command=lambda: thingy(self.p_filename.get(), self.t_filename.get()))

#command=lambda: backend.main(self.p_filename.get(), self.t_filename.get()))
        self.submit_button.grid(row=4, column=0)
        

        self.quit_button = ttk.Button(self.parent, text='Quit',\
                                      command=sys.exit)
        self.quit_button.grid(row=4, column=1, columnspan=2)
        mainloop()

    def get_ppl_filename(self):
        options = dict(defaultextension='.csv',\
                   filetypes=[('CSV files','*.csv'), \
                              ('Text files','*.txt')])
        filename = tkFileDialog.askopenfilename(**options)
        self.p_filename.set(filename)        
        self.update_idletasks()
        if filename:
            print "selected:", filename
        else:
            print "file not selected"


    def get_tables_filename(self):
        options = dict(defaultextension='.csv',\
                   filetypes=[('CSV files','*.csv'), \
                              ('Text files','*.txt')])
        filename = tkFileDialog.askopenfilename(**options)
        self.t_filename.set(filename)        
        self.update_idletasks()
        if filename:
            print "selected:", filename
        else:
            print "file not selected"

    def centerWindow(self):
        w = 500
        h = 400
        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()
        x = (sw - w)/2
        y = (sh - h)/2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))


class ProgressWindow(Frame):
    def __init__(self, parent, peoples_csv, tables_csv):
        Frame.__init__(self, parent)
        self.parent = parent

        f = plt.figure()
        plt.axis([0, 1, 0, 30000])
        plt.ion()
        plt.show()
        
        x = []
        y = []

        gen = main('people.csv', 'tables.csv')
        for (bcost, T) in gen:
            x.append(T)
            y.append(bcost)
            plt.scatter(x, y)
            plt.draw()
            time.sleep(0.05)


        

def main():
    root = Tk()
    app = BaseWindow(root)
    root.mainloop()  


if __name__ == '__main__':
    main()  

