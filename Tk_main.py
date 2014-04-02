"""
This code is based on the very helpful tutorial at
http://sebsauvage.net/python/gui/
"""
# Standard library imports
import time
import math
import sys

# Threading imports
import threading
import Queue
 
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
    def __init__(self, parent, plot_frame):
        Frame.__init__(self, parent)#, bg="pink")
        self.parent = parent
        self.plot_frame = plot_frame
        self.initialize()

    def initialize(self):
        self.frame_header = Label(self, text="Save your results:", fg="black", \
                                  font=("Optima Italic", 24))
        self.frame_header.grid(row=0, column=0, columnspan=2, sticky=(NW), pady=(20,10), padx=(10,10))

        self.cost_label = Label(self, text="Final Cost: ")
        self.cost_label.grid(row=1, column=0, padx=(10, 10))

        self.cost_label2 = Label(self, text="<<XXX>>")
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
    def __init__(self, parent, plot_frame):
        Frame.__init__(self, parent)#, bg="blue")
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
                                        command=lambda: self.generate_results())
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

    # from http://stackoverflow.com/questions/16745507/tkinter-how-to-use-threads-to-preventing-main-event-loop-from-freezing
    def generate_results(self):
        self.submit_button.config(state="disabled")
        self.x = []
        self.y = []
        self.queue = Queue.Queue()
        ThreadedBackendCall(self.queue).start()
        self.parent.after(2500, self.process_queue)

    def process_queue(self):
        try:
            msg = self.queue.get(0)
            iteration = msg[0]
            bcost = msg[1]
            self.x.append(iteration)
            self.y.append(bcost)
            ppl.scatter(self.plot_frame.plot, self.x, self.y)
            self.plot_frame.canvas.draw()
            self.parent.after(2500, self.process_queue)
        except Queue.Empty:
            self.parent.after(2500, self.process_queue)


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


class InstructionsFrame(Frame):
    def __init__(self, parent, width=500, height=200, bg="white"):
        Frame.__init__(self, parent)#, width=width, height=height, bg=bg)
        self.initialize()

    def initialize(self):
        self.instructions_text = \
    """ 
    Seating Chart Creator makes an optimal seating chart for a given set of people, tables, and days. It generates a random chart, then searches for a better one by switching people around.\n
    Each time, the 'cost' of the chart is measured and plotted below. The cost will decrease gradually as the program runs; an optimal chart has a cost of 0.\n
    <<CLICK HERE>> to see the list of rules SCC follows.
    <<CLICK HERE>> for an example People input file.
    <<CLICK HERE>> for an example Tables input file.\n"""
    
        self.instructions_label = Label(self, text=self.instructions_text, font=("Optima",14), anchor=W, justify=LEFT)
        self.instructions_label.grid(row=0, column=0, sticky=(W))


class HeaderFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.initialize()

    def initialize(self):
        self.logo = PhotoImage(file='logo-small.gif')
        self.logo_label = Label(self)
        self.logo_label['image'] = self.logo
        self.logo_label.grid(row=0, column=0, padx=20, pady=(10,0), sticky=(W))

        self.title = Label(self, text="Seating Chart Creator", \
                      font=("Optima", 48))
        self.title.grid(row=0, column=1, sticky=(W))

class ThreadedBackendCall(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
    def run(self):
        gen = backend.main("people.csv", "tables.csv")
        for (bcost, T) in gen:
            iteration = math.log(T)/math.log(config.alpha)
            self.queue.put((iteration, bcost))
            time.sleep(0.05)
        self.queue.put("Task finished")

def main():
    root = Tk()
    centered_window = Frame(root)
    centered_window.pack()

    header_frame = HeaderFrame(centered_window)
    header_frame.grid(row=0, column=0, columnspan=3, sticky=(W))

    instructions_frame = InstructionsFrame(centered_window)
    instructions_frame.grid(row=1, column=0, columnspan=3, sticky=(W), padx=(0,20))

    plot_frame = PlotFrame(centered_window)
    plot_frame.grid(row=2, column=1, sticky=(N))

    input_frame = InputFrame(centered_window, plot_frame)
    input_frame.grid(row=2, column=0, padx=10, pady=20, sticky=(N))

    results_frame = ResultsFrame(centered_window, plot_frame)
    results_frame.grid(row=2, column=2, padx=10, pady=20, sticky=(N))


    """
    myTextWidget= Text(input_frame)

    myFile=file("test.py")
    myText= myFile.read()
    myFile.close()

    myTextWidget.insert(0.0,myText)
    myTextWidget.grid(row=5,column=1)
    """
    root.mainloop()  


if __name__ == '__main__':
    main()  
