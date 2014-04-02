"""
This code is based on the very helpful tutorial at
http://sebsauvage.net/python/gui/
"""
# Standard library imports
import time
import math
import sys
 
# Tkinter imports
from Tkinter import *
import tkFileDialog
import ttk
from PIL import ImageTk, Image

# Matplotlib imports
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import prettyplotlib as ppl
from prettyplotlib import brewer2mpl

# Seating Chart Creator imports
import main as backend
import config
        

class ResultsFrame(Frame):
    def __init__(self, parent, plot_frame, width=350, height=200, bg="pink"):
        Frame.__init__(self, parent)#, width=width, height=height, bg=bg)
        self.parent = parent
        self.plot_frame = plot_frame
        self.initialize()

    def initialize(self):
        self.frame_header = Label(self, text="Save your results:", fg="black", \
                                  font=("Optima Italic", 24))
        self.frame_header.grid(row=0, column=0, columnspan=2, sticky=(NW), pady=(20,10), padx=(10,10))

        self.cost_label = Label(self, text="Cost of your best solution: ")
        self.cost_label.grid(row=1, column=0, padx=(10, 10))

        self.cost_label2 = Label(self, text="XXX")
        self.cost_label2.grid(row=1, column=1)

        self.savebtn = Button(self, text='Save Seating Chart', command=lambda: self.file_save())
        self.savebtn.grid(row=2, column=0, pady=10)

    def file_save(self):
        # default extension is optional, here will add .txt if missin
        fout = tkFileDialog.asksaveasfile(mode='w', defaultextension=".csv")
        text2save = "hellooooooo"
        fout.write(text2save)
        fout.close()
        

class InputFrame(Frame):
    def __init__(self, parent, plot_frame, width=350, height=200, bg="white"):
        Frame.__init__(self, parent)
        self.parent = parent
        self.plot_frame = plot_frame
        self.initialize()

    def initialize(self):
        self.frame_header = Label(self, text="Load your files:", fg="black", \
                                  font=("Optima Italic", 24))
        self.frame_header.grid(row=0, column=0, columnspan=2, sticky=(NW), pady=(20,10), padx=(10,10))

        self.p_filename = StringVar()
        self.t_filename = StringVar()

        # must use lamba - otherwise 'command' executes when the code is loaded,
        # not when the button is pressed
        self.p_label = ttk.Label(self, textvariable=self.p_filename, width=10)
        self.p_label.grid(row=1,column=0, sticky=(E))
        self.p_button = ttk.Button(self, text='Choose People File',\
                                   command=lambda: self.get_filename(self.p_filename))
        self.p_button.grid(row=1, column=1, padx=5, pady=10)

        self.t_label = ttk.Label(self, textvariable=self.t_filename, width=10)
        self.t_label.grid(row=2, column=0, sticky=(E))
        self.t_button = ttk.Button(self, text='Choose Tables File',\
                                   command=lambda: self.get_filename(self.t_filename))
        self.t_button.grid(row=2, column=1, padx=5, pady=10)

        self.submit_button = ttk.Button(self, text='Generate Seating Chart', \
                                        command=lambda: add_to_plot(self.plot_frame))
        self.submit_button.grid(row=4, column=0, columnspan=2, pady=10)

        self.quit_button = ttk.Button(self, text='Quit',\
                                      command=sys.exit)
        self.quit_button.grid(row=5, column=0, columnspan=2, pady=50)

    def get_filename(self, filename_var):
        options = dict(defaultextension='.csv',\
                   filetypes=[('CSV files','*.csv'), \
                              ('Text files','*.txt')])
        filename = tkFileDialog.askopenfilename(**options)
        filename_var.set(filename)        
        self.update_idletasks()
        if filename:
            print "selected: " + str(filename_var.get())
        else:
            print "file not selected"

def add_to_plot(plot_figure, x=[], y=[]):
    gen = backend.main("people.csv", "tables.csv")
    for (bcost, T) in gen:
        iteration = math.log(T)/math.log(config.alpha)
        x.append(iteration)
        y.append(bcost)
        ppl.scatter(plot_figure.plot, x, y)
        #plot_figure.plot.scatter(x, y)
        plot_figure.canvas.draw()
        time.sleep(0.05)

class PlotFrame(Frame):
    def __init__(self, parent, width=500, height=200, bg="white"):
        Frame.__init__(self, parent)#, width=width, height=height, bg=bg)
        self.initialize()

    def initialize(self):
        self.fig = plt.figure()

        spines_to_remove = ['top', 'right']
        self.fig.set_facecolor('white')
        self.fig.set_size_inches(6,5)
        self.plot = self.fig.add_subplot(1, 1, 1)
        
        self.plot.axis([0, 100, 0, 3000])
        self.plot.set_xlabel("Iteration")
        self.plot.set_ylabel("Cost")
        self.fig.tight_layout()

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.show()
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky=(N))


def main():
    root = Tk()
    centered_window = Frame(root)
    centered_window.pack()

    logo_frame = Frame(centered_window)
    logo_label = Label(logo_frame)
    logo = PhotoImage(file='logo-small.gif')
    logo_label['image'] = logo
    logo_label.grid(row=0, column=0, padx=20, pady=10, sticky=(W))

    title = Label(logo_frame, text="Seating Chart Creator", \
                  font=("Optima", 48))
    title.grid(row=0, column=1, sticky=(W))
    logo_frame.grid(row=0, column=0, columnspan=3, sticky=(W))


    instructions_text = \
    """ 
    Seating Chart Creator makes an optimal seating chart for a given set of people, tables, and days. It generates a random chart, then searches for a better one by switching people around.
    Each time, the 'cost' of the chart is measured and plotted below. The cost will decrease gradually as the program runs; an optimal chart has a cost of 0.\n
    <<CLICK HERE>> to see the list of rules SCC follows.
    <<CLICK HERE>> for an example People input file.
    <<CLICK HERE>> for an example Tables input file."""
    
    instructions_frame = Frame(centered_window)
    instructions_label = Label(instructions_frame, text=instructions_text, font=("Optima",14), anchor=W, justify=LEFT)
    instructions_label.grid(row=0, column=0, sticky=(W))
    instructions_frame.grid(row=1, column=0, columnspan=3, sticky=(W))


    plot_frame = PlotFrame(centered_window)#, width=600, height=200)
    plot_frame.grid(row=2, column=1, sticky=(N))

    input_frame = InputFrame(centered_window, plot_frame)#, width=300, height=200)
    input_frame.grid(row=2, column=0, padx=20, pady=20, sticky=(N))

    results_frame = ResultsFrame(centered_window, plot_frame)#, width=300, height=200)#, bg="pink")
    results_frame.grid(row=2, column=2, padx=20, pady=20, sticky=(N))

    root.mainloop()  


if __name__ == '__main__':
    main()  
