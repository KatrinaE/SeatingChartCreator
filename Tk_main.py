"""
This code is based on the very helpful tutorial at
http://sebsauvage.net/python/gui/
"""
from Tkinter import Tk, Frame, Label, BOTH, Entry, StringVar
from Tkinter import *
import tkFileDialog
import ttk
import sys

import main as backend
from Tk_plot import callback


from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
#import Tkinter as Tk
import ttk
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import interactive
from matplotlib.pylab import subplots, close
import time
import math

import config

class ProgressWindow(Frame):
    def __init__(self, parent, peoples_csv, tables_csv):
        Frame.__init__(self, parent, width=600, height=600, bg='red')
        self.parent = parent

        f = plt.figure()
        plt.axis([0, 1, 0, 30000])
        plt.ion()
        plt.show()
        
        x = []
        y = []
        """
        gen = main(people_csv, tables_csv)
        for (bcost, T) in gen:
            x.append(T)
            y.append(bcost)
            plt.scatter(x, y)
            plt.draw()
            time.sleep(0.05)
        """
        
class InputFrame(Frame):
    def __init__(self, parent, plot_frame, width=350, height=600, bg="white"):
        Frame.__init__(self, parent, width=width, height=height, bg=bg)
        self.parent = parent
        self.plot_frame = plot_frame
        self.initialize()

    def initialize(self):
        self.title = Label(self, text="Input your data", fg="black", \
                           font=("Helvetica", 24))
        self.title.grid(row=0, column=0, columnspan=2, sticky=(W), pady=(0,10))

        self.p_filename = StringVar()
        self.t_filename = StringVar()
        self.p_label = ttk.Label(self, textvariable=self.p_filename, width=20)
        self.p_label.grid(row=1,column=0, sticky=(E)) 
        self.p_button = ttk.Button(self, text='Choose People File',\
                                   command=self.get_ppl_filename)
        self.p_button.grid(row=1, column=1, padx=5, pady=10)

        self.t_label = ttk.Label(self, textvariable=self.t_filename, width=20)
        self.t_label.grid(row=2, column=0, sticky=(E))
        self.t_button = ttk.Button(self, text='Choose Tables File',\
                                   command=self.get_tables_filename)
        self.t_button.grid(row=2, column=1, padx=5, pady=10)

        # must use lamba or else the command executes when the code is loaded,
        # not when the button is pressed
        self.submit_button = ttk.Button(self, text='Generate Seating Chart', command=lambda: add_to_plot(self.plot_frame))#lambda: callback(self.p_filename.get(), self.t_filename.get()))
        self.submit_button.grid(row=4, column=0, columnspan=2, pady=10)

        self.quit_button = ttk.Button(self, text='Quit',\
                                      command=sys.exit)
        self.quit_button.grid(row=5, column=0, columnspan=2, pady=50)


    def foo(self):
        x = ProgressWindow(self.parent, 'people.csv', 'tables.csv')
        x.grid(row=1, column=1)

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

def add_to_plot(plot_figure, x=[], y=[]):
    gen = backend.main("people.csv", "tables.csv")
    """
    for i in range(1, 100):
        x.append(i)
        y.append(i*10)
        plot_figure.plot.scatter(x, y)
        plot_figure.canvas.draw()
        time.sleep(0.05)
    """
    for (bcost, T) in gen:
        iteration = math.log(T)/math.log(config.alpha)
        x.append(iteration)
        y.append(bcost)
        plot_figure.plot.scatter(x, y)
        plot_figure.canvas.draw()
        print "just plotted (" + str(T) + ", " + str(bcost) + ")"
        time.sleep(0.05)

# for some reason this doesn't work - I get the error
# AttributeError: PlotFrame instance has no attribute 'tk'
# which is weird, because Frame does.

class PlotFrame(Frame):
    def __init__(self, parent, width=500, height=600, bg="purple"):
        Frame.__init__(self, parent, width=width, height=height, bg=bg)
        self.initialize()

    def initialize(self):
        self.fig = plt.figure()#figsize=(6,5), dpi=100)
        x = []
        y = []
        self.plot = self.fig.add_subplot(1, 1, 1)
        self.plot.axis([0, 100, 0, 3000])
        self.plot.set_xlabel("Iteration")
        self.plot.set_ylabel("Cost")

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.show()
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky=(N))

def main():
    root = Tk()
    centered_window = Frame(root)
    centered_window.pack()

    logo = Frame(centered_window, width=350, height=200, bg="purple")
    logo.grid(row=0, column=0)

    title = Label(centered_window, text="Seating Chart Creator", \
                  font=("Helvetica", 48), bg="white")
    title.grid(row=0, column=1)

    plot_frame = PlotFrame(centered_window, width=600, height=600, bg="orange")
    plot_frame.grid(row=1, column=1, sticky=(N))

    input_frame = InputFrame(centered_window, plot_frame, width=300, height=600)
    input_frame.grid(row=1, column=0, sticky=(N))

    results_frame = Frame(centered_window, width=300, height=600, bg="pink")
    results_frame.grid(row=1, column=2)

    root.mainloop()  


if __name__ == '__main__':
    main()  
