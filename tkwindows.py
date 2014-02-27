"""
This code is based on the very helpful tutorial at
http://sebsauvage.net/python/gui/
"""
from Tkinter import Tk, Frame, Label, BOTH, Entry, StringVar
from Tkinter import *
import tkFileDialog
import ttk
import sys


class BaseWindow(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initialize()


    def initialize(self):
        label = Label(self.parent, text="Welcome to Seating \
        Chart Creator", fg="black",bg="lightblue")

        label.grid(row=0, column=0, columnspan=2)

        self.p_filename = StringVar()
        self.p_filename.set("Please choose a file")
        self.label1 = ttk.Label(self.parent, textvariable=self.p_filename.get())
        #self.label1.insert(0, self.p_filename.get())
        self.label1.grid(row=1,column=0, sticky=(E))

        self.button = ttk.Button(self.parent, text='Choose People File',\
                                 command=self.get_ppl_filename)
        self.button.bind(self.quit)
        self.button.grid(row=1, column=1)


        v = StringVar()
        e = Entry(self, textvariable=v)
        e.grid(row=6,column=1)
        v.set("a default value")
        s = v.get()
        self.entry1 = ttk.Entry(self.parent)
        self.entry1.grid(row=2, column=0)

        self.button = ttk.Button(self.parent, text='Choose Tables File',\
                                command=self.get_ppl_filename)
        self.button.bind(self.quit)
        self.button.grid(row=2, column=1)



        self.centerWindow()
        self.grid_columnconfigure(0,weight=1)


        self.button = ttk.Button(self.parent, text='Quit',\
                                command=self.OnButtonClick)
        self.button.bind(self.quit)
        self.button.grid(row=4, column=1, columnspan=2)




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

    def OnButtonClick(self):
        print "You clicked the button !"
        sys.exit()

    def OnPressEnter(self,event):
        print "You pressed enter !"

    def centerWindow(self):
        w = 500
        h = 400
        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()
        x = (sw - w)/2
        y = (sh - h)/2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def quit(self):
        sys.exit()

class ProgressWindow(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        

def main():
    root = Tk()
    app = BaseWindow(root)
    import pdb; pdb.set_trace()
    root.mainloop()  


if __name__ == '__main__':
    main()  

