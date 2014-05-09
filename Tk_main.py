"""
This code is based on the very helpful tutorial at
http://sebsauvage.net/python/gui/
"""
# Standard library imports
import time
import math
import sys
import threading
import Queue
 
# Tkinter imports
from Tkinter import *
import tkMessageBox
import tkFileDialog
import ttk

# Matplotlib imports
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

# Seating Chart Creator imports
import main as backend
import config
from seating_io import write_tables_to_csv, write_people_to_csv, InputData

class ResultsFrame(Frame):
    def __init__(self, parent, plot_frame):
        Frame.__init__(self, parent, background="white")
        self.parent = parent
        self.plot_frame = plot_frame
        self.initialize()

    def initialize(self):
        self.frame_header = Label(self, text="Solution Metrics:", foreground="gray", \
                                  font=("Optima Italic", 24))
        self.frame_header.grid(row=0, column=0, columnspan=2, sticky=(NW), \
                               pady=(20,10))

        self.pairs2_label = Label(self, text="Number of pairs sitting \n" + \
                                    "together twice: ", \
                                    justify=LEFT, foreground="gray")
        self.pairs2_label.grid(row=2, column=0, sticky=(W), pady=10)
        self.pairs2_var = StringVar()
        self.pairs2_var.set('__')
        self.pairs2 = Label(self, textvariable=self.pairs2_var, width=10, \
                             foreground="gray", font=("Optima bold", 24))
        self.pairs2.grid(row=2, column=1, sticky=(E))


        self.pairs3_label = Label(self, text="Number of pairs sitting \n" + \
                                    "together three times: ", \
                                    justify=LEFT, foreground="gray")
        self.pairs3_label.grid(row=3, column=0, sticky=(W), pady=10)
        self.pairs3_var = StringVar()
        self.pairs3_var.set('__')
        self.pairs3 = Label(self, textvariable=self.pairs3_var, width=10, \
                             foreground="gray", font=("Optima bold", 24))
        self.pairs3.grid(row=3, column=1, sticky=(E))

        self.trios2_label = Label(self, text="Number of trios sitting \n" + \
                                    "together twice: ", \
                                    justify=LEFT, foreground="gray")
        #self.trios2_label.grid(row=4, column=0, sticky=(W), pady=10)
        self.trios2_var = StringVar()
        self.trios2_var.set('__')
        self.trios2 = Label(self, textvariable=self.trios2_var, width=10, \
                             foreground="gray", font=("Optima bold", 24))
        #self.trios2.grid(row=4, column=1, sticky=(E))



        self.trios3_label = Label(self, text="Number of trios sitting \n" + \
                                    "together three times: ", \
                                    justify=LEFT, foreground="gray")
        #self.trios3_label.grid(row=5, column=0, sticky=(W), pady=10)
        self.trios3_var = StringVar()
        self.trios3_var.set('__')
        self.trios3 = Label(self, textvariable=self.trios3_var, width=10, \
                             foreground="gray", font=("Optima bold", 24))
        #self.trios3.grid(row=5, column=1, sticky=(E))

        self.same_spot2_label = Label(self, text="Number of people sitting \n" + \
                                     "in the same spot twice: ", \
                                     justify=LEFT, foreground="gray")
        self.same_spot2_label.grid(row=6, column=0, sticky=(W), pady=10)
        self.same_spot2_var = StringVar()
        self.same_spot2_var.set('__')
        self.same_spot2 = Label(self, textvariable=self.same_spot2_var, width=10, \
                             foreground="gray", font=("Optima bold", 24))
        self.same_spot2.grid(row=6, column=1, sticky=(E))


        self.same_spot3_label = Label(self, text="Number of people sitting \n" + \
                                     "in the same spot three times: ", \
                                     justify=LEFT, foreground="gray")
        self.same_spot3_label.grid(row=7, column=0, sticky=(W), pady=10)
        self.same_spot3_var = StringVar()
        self.same_spot3_var.set('__')
        self.same_spot3 = Label(self, textvariable=self.same_spot3_var, width=10, \
                             foreground="gray", font=("Optima bold", 24))
        self.same_spot3.grid(row=7, column=1, sticky=(E))


class InputFrame(Frame):
    def __init__(self, parent, progress_frame, results_frame):
        Frame.__init__(self, parent, bg="white")
        self.parent = parent
        self.progress_frame = progress_frame
        self.plot_frame = progress_frame.plot_frame
        self.backend_call = None
        self.results_frame = results_frame
        self.holding_lock = False
        self.initialize()


    def activate_submit_button(self, name, index, mode):
        p = self.p_filename.get()
        t = self.t_filename.get()
        if (p != '') and (t != ''):
            self.submit_button.config(state='normal')
        else:
            self.submit_button.config(state='disabled')

    def initialize(self):
        self.frame_header = Label(self, text="Load your files:", foreground="black", \
                                  font=("Optima Italic", 24))
        self.frame_header.grid(row=0, column=0, columnspan=2, sticky=(NW), pady=(20,10), padx=(0,0))

        self.p_filename = StringVar()
        self.t_filename = StringVar()
        self.p_filename.trace('w', self.activate_submit_button)
        self.t_filename.trace('w', self.activate_submit_button)

        # must use lamba - otherwise 'command' executes when the code is loaded,
        # not when the button is pressed
        self.p_entry = ttk.Entry(self, textvariable=self.p_filename, width=20)
        self.p_entry.grid(row=1,column=0, sticky=(W))
        self.p_button = ttk.Button(self, text='Choose People File',\
                                   command=lambda: self.get_filename(self.p_filename))
        self.p_button.grid(row=1, column=1, padx=5, pady=10, sticky=(E))

        self.t_entry = ttk.Entry(self, textvariable=self.t_filename, width=20)
        self.t_entry.grid(row=2, column=0, sticky=(W))
        self.t_button = ttk.Button(self, text='Choose Tables File',\
                                   command=lambda: self.get_filename(self.t_filename))
        self.t_button.grid(row=2, column=1, padx=5, pady=10, sticky=(E))

        self.submit_button = ttk.Button(self, text='Generate Seating Chart', \
                                        command=lambda: self.generate_results(), 
                                        state='disabled')
        self.submit_button.grid(row=4, column=0, columnspan=2, pady=10)

        self.save_header = Label(self, text="Save your results:", fg="Gray", \
                                  font=("Optima Italic", 24))
        self.save_header.grid(row=6, column=0, columnspan=2, sticky=(NW), \
                               pady=(20,10), padx=(10,10))

        self.save_filename = StringVar()

        self.save_people_var = StringVar()
        self.save_people_var.set('Save by Person Name')
        self.save_people_button = Button(self, textvariable=self.save_people_var, state='disabled',\
                                  command=lambda: self.save_file('people'))
        self.save_people_button.grid(row=7, column=0, pady=10)


        self.save_tables_var = StringVar()
        self.save_tables_var.set('Save by Table Number')
        self.save_tables_button = Button(self, textvariable=self.save_tables_var, state='disabled',\
                                  command=lambda: self.save_file('tables'))
        self.save_tables_button.grid(row=7, column=1, pady=10)


    def pause_or_resume(self):
        if not self.holding_lock: 
            # pause
            self.switch_to_output_mode()
            self.backend_call.lock.acquire()
            self.holding_lock = True
        else:
            # resume
            self.switch_to_calculations_mode()
            self.backend_call.lock.release()        
            self.holding_lock = False

    def reset(self):
        if self.holding_lock:
            self.backend_call.lock.release()
            self.holding_lock = False
        self.backend_call.stop()
        self.queue.put('Reset')
        self.backend_call.join()
        self.switch_to_input_mode()

    def save_file(self, formatting):
        options = dict(defaultextension='.csv',\
                       filetypes=[('CSV files','*.csv'), \
                                  ('Text files','*.txt')])
        filename = tkFileDialog.asksaveasfilename(**options)
        self.save_filename.set(filename)
        self.update_idletasks()
        if formatting == 'people':
            write_people_to_csv(self.solution, self.save_filename.get())
        else:
            write_tables_to_csv(self.solution, self.save_filename.get())

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


    def switch_to_input_mode(self):
        self.submit_button.config(state='active')
        self.frame_header.config(foreground="black")
        self.p_entry.config(foreground="black", state="active")
        self.t_entry.config(foreground="black", state="active")
        self.p_button.config(state='active')
        self.t_button.config(state='active')

        self.save_header.config(foreground="gray")
        self.save_people_button.config(state="disabled")
        self.save_tables_button.config(state="disabled")

        self.progress_frame.pause_button.config(state="disabled")
        self.progress_frame.pause_var.set("Pause")
        self.progress_frame.reset_button.config(state="disabled")

        self.progress_frame.plot_frame.title.config(foreground="gray")
        self.progress_frame.plot_frame.shield.grid(row=1, column=0)
        self.progress_frame.num_tries_title.config(foreground="gray")
        self.progress_frame.num_tries.config(foreground="white")
        self.progress_frame.num_tries_var.set('__')

        self.results_frame.frame_header.config(foreground="gray")
        self.results_frame.pairs2_label.config(foreground="gray")
        self.results_frame.pairs3_label.config(foreground="gray")
        self.results_frame.trios2_label.config(foreground="gray")
        self.results_frame.trios3_label.config(foreground="gray")
        self.results_frame.same_spot2_label.config(foreground="gray")
        self.results_frame.same_spot3_label.config(foreground="gray")

        self.results_frame.pairs2.config(foreground="white")
        self.results_frame.pairs3.config(foreground="white")
        self.results_frame.trios2.config(foreground="white")
        self.results_frame.trios3.config(foreground="white")
        self.results_frame.same_spot2.config(foreground="white")
        self.results_frame.same_spot3.config(foreground="white")

        self.results_frame.pairs2_var.set('__')
        self.results_frame.pairs3_var.set('__')
        self.results_frame.trios2_var.set('__')
        self.results_frame.trios3_var.set('__')
        self.results_frame.same_spot2_var.set('__')
        self.results_frame.same_spot3_var.set('__')

        self.plot_frame.rects = self.plot_frame.plot.barh((0), (43000), height=1, left=0, linewidth=0, color='white')
        self.plot_frame.canvas.draw()
 
    def switch_to_output_mode(self):
        self.submit_button.config(state='disabled')
        self.frame_header.config(foreground="gray")
        self.p_entry.config(foreground="black", state="disabled")
        self.t_entry.config(foreground="black", state="disabled")
        self.p_button.config(state='disabled')
        self.t_button.config(state='disabled')

        self.save_header.config(foreground="black")
        self.save_people_button.config(state="active")
        self.save_tables_button.config(state="active")

        self.progress_frame.pause_var.set("Resume")
        self.progress_frame.pause_button.config(state="active")
        self.progress_frame.reset_button.config(state="active")

        self.progress_frame.plot_frame.title.config(foreground="gray")
        self.progress_frame.plot_frame.shield.grid(row=1, column=0)
        self.progress_frame.num_tries_title.config(foreground="gray")
        self.progress_frame.num_tries.config(foreground="gray")

        self.results_frame.frame_header.config(foreground="gray")
        self.results_frame.pairs2_label.config(foreground="gray")
        self.results_frame.pairs3_label.config(foreground="gray")
        self.results_frame.trios2_label.config(foreground="gray")
        self.results_frame.trios3_label.config(foreground="gray")
        self.results_frame.same_spot2_label.config(foreground="gray")
        self.results_frame.same_spot3_label.config(foreground="gray")

        self.results_frame.pairs2.config(foreground="gray")
        self.results_frame.pairs3.config(foreground="gray")
        self.results_frame.trios2.config(foreground="gray")
        self.results_frame.trios3.config(foreground="gray")
        self.results_frame.same_spot2.config(foreground="gray")
        self.results_frame.same_spot3.config(foreground="gray")

    def switch_to_calculations_mode(self):
        self.submit_button.config(state='disabled')
        self.frame_header.config(foreground="gray")
        self.p_entry.config(foreground="gray", state="disabled")
        self.t_entry.config(foreground="gray", state="disabled")
        self.p_button.config(state='disabled')
        self.t_button.config(state='disabled')

        self.save_header.config(foreground="gray")
        self.save_people_button.config(state="disabled")
        self.save_tables_button.config(state="disabled")


        self.progress_frame.plot_frame.title.config(foreground="black")
        self.progress_frame.plot_frame.shield.grid_forget()
        self.progress_frame.num_tries_title.config(foreground="black")
        self.progress_frame.num_tries.config(foreground="violet red")

        self.progress_frame.pause_button.config(state="active")
        self.progress_frame.pause_var.set("Pause")
        self.progress_frame.reset_button.config(state="active")


        self.results_frame.frame_header.config(foreground="black")
        self.results_frame.pairs2_label.config(foreground="black")
        self.results_frame.pairs3_label.config(foreground="black")
        self.results_frame.trios2_label.config(foreground="black")
        self.results_frame.trios3_label.config(foreground="black")
        self.results_frame.same_spot2_label.config(foreground="black")
        self.results_frame.same_spot3_label.config(foreground="black")


        self.results_frame.pairs2.config(foreground="violet red")
        self.results_frame.pairs3.config(foreground="violet red")
        self.results_frame.trios2.config(foreground="violet red")
        self.results_frame.trios3.config(foreground="violet red")
        self.results_frame.same_spot2.config(foreground="violet red")
        self.results_frame.same_spot3.config(foreground="violet red")

    # from http://stackoverflow.com/questions/16745507/tkinter-how-to-use-threads-to-preventing-main-event-loop-from-freezing
    def generate_results(self):
        self.switch_to_calculations_mode()
        self.queue = Queue.Queue()
        try:
            self.backend_call = ThreadedBackendCall(self.queue, self.p_filename, 
                                                    self.t_filename)
        except TypeError:
            # bad input files
            self.switch_to_input_mode()
            tkMessageBox.showerror(
                "Invalid Input File(s)",
                "Could not read input data"
            )
            raise
            return
        self.backend_call.start()
        self.parent.after(10, self.process_queue)

    def process_queue(self):
        try:
            msg = self.queue.get(0)
            if msg == "Reset":
                self.switch_to_input_mode()
            elif msg == "Task finished":
                print msg
                self.switch_to_output_mode()
            else:
                self.solution = msg[0]
                iteration = msg[1]
                cost = msg[2]
                quality = 43000-cost # low cost = high quality
                self.progress_frame.num_tries_var.set(int(iteration))
                self.plot_frame.rects = self.plot_frame.plot.barh((0), (quality), height=1, left=0, linewidth=0, color=self.plot_frame.color)
                self.plot_frame.canvas.draw()

                self.plot_frame.rects = self.plot_frame.plot.barh\
                                        ((0), (quality), height=1, left=0, \
                                         linewidth=0, color=self.plot_frame.color)
                self.plot_frame.canvas.draw()
                self.progress_frame.num_tries_var.set(int(iteration))
                self.results_frame.pairs2_var.set(self.solution.overlaps2_freqs[2])
                self.results_frame.pairs3_var.set(self.solution.overlaps2_freqs[3])
                self.results_frame.trios2_var.set(self.solution.overlaps3_freqs[2])
                self.results_frame.trios3_var.set(self.solution.overlaps3_freqs[3])
                self.results_frame.same_spot2_var.set(self.solution.same_spot_freqs[2])
                self.results_frame.same_spot3_var.set(self.solution.same_spot_freqs[3])

                self.parent.after(10, self.process_queue)
        except Queue.Empty:
            self.parent.after(10, self.process_queue)


class PlotFrame(Frame):
    def __init__(self, parent, title_text, axes_scale, color, y_left, y_right, width=500, height=200, background="white"):
        Frame.__init__(self, parent, width=1000, height=5000, background="white")
        self.title_text = title_text
        self.axes_scale = axes_scale
        self.color = color
        self.y_left = str(y_left) + "                    "
        self.y_right = "                    " + str(y_right)

        self.initialize()

    def initialize(self):
        # create title
        self.title_frame = Frame(self)
        self.title = Label(self.title_frame, text=self.title_text, font=("Optima Italic", 24), foreground="gray")
        self.title.grid(row=0, column=0, sticky=(W))
        self.title_frame.grid(row=0, column=0, sticky=(W))

        # create figure
        self.fig = plt.figure()
        self.fig.set_facecolor('white')
        self.fig.set_size_inches(6,2)

        # create subplot
        self.plot = self.fig.add_subplot(111)
        self.plot.axis(self.axes_scale)

        # format subplot
        spines_to_remove = ['top','bottom']
        for spine in spines_to_remove:
            self.plot.spines[spine].set_visible(False)
        self.plot.get_xaxis().set_ticks([])
        self.plot.get_yaxis().set_ticks([])
        # excessive whitespace is so text doesn't overlap w/ plot
        self.plot.set_ylabel(self.y_left, rotation='horizontal')

        # create right axes to display text to right of figure
        # can't just create text box because it will display inside the graph
        self.plotax2 = self.plot.twinx()
        self.plotax2.get_xaxis().set_ticks([])
        self.plotax2.get_yaxis().set_ticks([])
        self.plotax2.set_ylabel(self.y_right, rotation='horizontal')
 
        distance = 0
        val = 0
        self.rects = self.plot.barh((0), (val), height=1, left=0, linewidth=0, color=self.color)

        self.fig.tight_layout()

        # display plot
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas._tkcanvas.config(highlightthickness=0)
        self.canvas.show()
        self.canvas.get_tk_widget().grid(row=1, column=0, sticky=(N))

        # hide plot until it's needed
        self.shield = Frame(self, width="6.75i", height="2i", background="white")
        self.shield.grid(row=1, column=0)

class InstructionsFrame(Frame):
    def __init__(self, parent, width=500, height=200, background="white"):
        Frame.__init__(self, parent)#, width=width, height=height, background=background)
        self.initialize()

    def initialize(self):
        self.instructions_text = \
    """ 
    Seating Chart Creator makes an optimal seating chart for a given set of people, tables, and days. It generates a preliminary chart, then searches for a better one by switching people around.\n"""    
        self.instructions_label = Label(self, text=self.instructions_text, font=("Optima",14), anchor=W, justify=LEFT)
        self.instructions_label.grid(row=0, column=0, sticky=(W))

        miniframe = Frame(self)
        miniframe.grid(row=1, column=0, padx=0, pady=(0,20))
        self.rules_button = Button(miniframe, text="View list of optimization rules", command=self.show_rules)
        self.rules_button.grid(row=1, column=0, sticky=(W), padx=10)

        self.people_example = Button(miniframe, text = "View example people input file", command=self.show_people_example)
        self.people_example.grid(row=1, column=1, sticky=(W), padx=10)

        self.tables_example = Button(miniframe, text = "View example tables input file", command=self.show_tables_example)
        self.tables_example.grid(row=1, column=2, sticky=(W), padx=10)

    def show_rules(self):
        self.windowr = Toplevel(self)
        self.windowr.wm_title("Optimization Rules")
        self.windowr.rowconfigure(0, weight=1)
        self.windowr.rowconfigure(1, weight=1)
        self.windowr.columnconfigure(0, weight=1)

        innerwindowr = Canvas(self.windowr)
        innerwindowr.pack()
        myscrollbar=Scrollbar(self.windowr,orient="vertical",command=innerwindowr.yview)
        innerwindowr.configure(yscrollcommand=myscrollbar.set)
        myscrollbar.pack(side="right",fill="y")

        #self.rtitle_label2 = Label(z,
        #                           text="Seating Chart Creator's Optimization Rules", 
        #                           font=("Optima Italic", 24))
        #self.rtitle_label2.pack()

        rtext1 = \
"""
*** Seating Chart Creator's Optimization Rules ***

Depending on the input data, it may or may not be possible to create a perfect seating
chart. Even if there is a perfect solution, there is no fast or easy way to find it.

Seating Chart Creator searches for that perfect solution using an optimization algorithm.
It specifies the criteria to evaluate the solution with, then searches for the
solution that best meets that criteria.

The search process involves random factors, so if you run it multiple times, you will 
get different answers.


*** The Criteria ***

SCC looks for a solution with the lowest 'cost'. The cost of a solution is determined by:

* The number of people sitting in the same spot multiple times.
* The number of pairs sitting together multiple times.
* The number of trios sitting together multiple times.
* The distance of each table from its optimal category balance.

The table sizes always correspond with those in the input file.


*** The Process ***

Step 1: Building the First Guess

SCC loops through the days of the event. On each day, it considers each person individually
and places him or her in the best spot available. People are shuffled each round so that
no one consistently gets the 'last pick' of the tables.

When considering where to seat a person, the following tables are excluded:
- Tables that are already full
- Tables that already have enough people of the same category as the person to be seated.

The person is then assigned to the table with the fewest people he/she has already sat with.


Step 2: Switching People Around

The strategy above is fairly good, but not perfect. SCC uses it as a starting point,
then generates new solutions by repeatedly switching individuals. The 'cost' is
calculated for each new solution. If a new solution is better than the current solution,
it is used as the starting point for the next round.

The technique SCC uses is called 'simulated annealing'. It is a frequently-used and
highly-regarded method for solving problems like this one. However, it is not guaranteed
to find a perfect solution.

The switching steps take a very long time (minutes - hours) because of the computational 
complexity of counting the number of times everyone sits together.

"""
        #scrollbar = Scrollbar(innerwindowr)
        #scrollbar.pack(side=RIGHT, fill=Y)
        #self.foo = Label(innerwindowr, text=rtext1)
        self.foo = Text(innerwindowr, width=100)
        self.foo.insert(INSERT, rtext1)
        self.foo.config(highlightthickness=0)
        self.foo.pack(padx=20)
        #self.foo.config(yscrollcommand=scrollbar.set)
        #scrollbar.config(command=self.foo.yview)

    def show_people_example(self):
        self.window = Toplevel(self)
        self.window.wm_title = "People Example"
        self.window.rowconfigure(0, weight=1)
        self.window.rowconfigure(1, weight=1)
        self.window.columnconfigure(0, weight=1)

        innerwindowp = Frame(self.window)
        innerwindowp.grid(row=0, column=0)
        self.ptitle_label2 = Label(innerwindowp, text="Example People Input File", font=("Optima Italic", 24))
        self.ptitle_label2.grid(row=0, column=0)
        ptext1 = \
"""
The 'People' input file contains information about the people to be seated and where they might have been preassigned to sit.
It should be saved in CSV format."""
        pheader1 = "COLUMN NAMES"
        ptext2 = \
"""The file should contain the column headers 'First Name', 'Last Name', and 'Category', written exactly as printed here -
capitalization is important.

All other columns are assumed to be the names of the days you are making the chart for. They must match the days in your 
'Tables' input file exactly (again, capitalization is important)."""
        pheader2 = "NOTES"
        ptext3= \
"""Each person should be assigned a category. You can name the categories whatever you like.

If a person has been preassigned to the head table on a particular day, write 'Head' (with a capital 'H') in the corresponding 
cell."""
        ptext1label = Label(innerwindowp, text=ptext1, justify=LEFT)
        ptext1label.grid(row=1, column=0, padx=20, sticky=(W))

        pheader1label = Label(innerwindowp, text=pheader1, font=("Optima Italic", 14), justify=LEFT)
        pheader1label.grid(row=2, column=0, padx=20, pady=(20,0), sticky=(W))

        ptext2label = Label(innerwindowp, text=ptext2, justify=LEFT)
        ptext2label.grid(row=3, column=0, padx=20, sticky=(W))

        pheader2label = Label(innerwindowp, text=pheader2, font=("Optima Italic", 14), justify=LEFT)
        pheader2label.grid(row=4, column=0, padx=20, pady=(20,0), sticky=(W))

        ptext3label = Label(innerwindowp, text=ptext3, justify=LEFT)
        ptext3label.grid(row=5, column=0, padx=20, sticky=(W))

        self.picture2p = PhotoImage(file='people-example.gif')
        self.picture_label2p = Label(self.window, image = self.picture2p)
        self.picture_label2p.grid(row=2, column=0)

    def show_tables_example(self):
        self.window2 = Toplevel(self)
        self.window2.wm_title = "Tables Example"
        self.window2.rowconfigure(0, weight=1)
        self.window2.rowconfigure(1, weight=1)
        self.window2.columnconfigure(0, weight=1)

        innerwindow = Frame(self.window2)
        innerwindow.grid(row=0, column=0)
        self.title_label2 = Label(innerwindow, text="Example Tables Input File", font=("Optima Italic", 24))
        self.title_label2.grid(row=0, column=0)
        text1 = \
"""
The 'Tables' input file contains information about the individual tables' names and capacities. It should be saved in CSV 
format."""
        header1 = "COLUMN NAMES"
        text2 = \
"""The file should contain the column header 'Table Name', written exactly as printed here - capitalization is important.

All other columns are assumed to be the names of the days you are making the chart for. They must match the days in your 
'People' input file exactly (again, capitalization is important)."""
        header2 = "NOTES"
        text3= \
"""You can choose arbitrary table names. If you include a table named 'Head', it will be populated exclusively with the people 
preassigned to it in the 'People' input file.

The number in each cell represents the table's capacity on that day. Make sure the overall capacity is at least as great as 
the number of people to be seated!"""
        text1label = Label(innerwindow, text=text1, justify=LEFT)
        text1label.grid(row=1, column=0, padx=20, sticky=(W))

        header1label = Label(innerwindow, text=header1, font=("Optima Italic", 14), justify=LEFT)
        header1label.grid(row=2, column=0, padx=20, pady=(20,0), sticky=(W))

        text2label = Label(innerwindow, text=text2, justify=LEFT)
        text2label.grid(row=3, column=0, padx=20, sticky=(W))

        header2label = Label(innerwindow, text=header2, font=("Optima Italic", 14), justify=LEFT)
        header2label.grid(row=4, column=0, padx=20, pady=(20,0), sticky=(W))

        text3label = Label(innerwindow, text=text3, justify=LEFT)
        text3label.grid(row=5, column=0, padx=20, sticky=(W))

        self.picture2 = PhotoImage(file='tables-example.gif')
        self.picture_label2 = Label(self.window2, image = self.picture2)
        self.picture_label2.grid(row=2, column=0)

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

class ProgressFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        plot_axes = [0, 43000, 0, 1]
        self.plot_frame = PlotFrame(self, "Quality of Solution", \
                                plot_axes, "dodgerblue", "Poor", "Perfect")
        self.plot_frame.grid(row=0, column=0, sticky=(N))
        
        self.num_tries_title = Label(self, text="Number of Attempts Made", \
                                     font=("Optima Italic", 24), fg="gray")
        self.num_tries_title.grid(row=1, column=0, sticky=(NW), pady=(20,0))
        
        self.num_tries_var = StringVar()
        self.num_tries_var.set('__')
        self.num_tries = Label(self, textvariable=self.num_tries_var, \
                          font=("Optima Bold", 24), foreground="gray")
        self.num_tries.grid(row=2, column=0, columnspan=2, sticky=(S), pady=(20,20))


        self.pause_var = StringVar()
        self.pause_var.set('Pause')
        self.pause_button = Button(self, textvariable=self.pause_var, state='disabled',\
                                   command=lambda: self.input_frame.pause_or_resume(), \
                                   width=10, pady=20)
        self.pause_button.grid(row=9, column=0)


        self.reset_button = Button(self, text="Reset", state='disabled', \
                                   command = lambda:self.input_frame.reset(), width=10)
        self.reset_button.grid(row=9, column=1)




class ThreadedBackendCall(threading.Thread):
    def __init__(self, queue, p_filename, t_filename):
        threading.Thread.__init__(self)
        self._stop_req = threading.Event()
        self.lock = threading.Lock()
        self.queue = queue
        self.input_data = InputData(p_filename.get(), t_filename.get())

    def run(self):
        max_iterations = math.log(config.T_min)/math.log(config.alpha) \
                         * config.iterations_per_temp
        gen = backend.main(self.input_data)
        for (solution, T) in gen:
            if self._stop_req.is_set():
                break
            elif not self._stop_req.is_set():
                self.lock.acquire()
                iteration = math.log(T)/math.log(config.alpha)+1
                self.queue.put((solution, iteration, solution.cost))
                self.lock.release()
                time.sleep(0.05)
        self.queue.put("Task finished")

    def stop(self):
        self._stop_req.set();

def main():

    # helper method used when quitting program
    def kill_all_threads():
        print 'foo'
        if input_frame.backend_call is not None:
            print 'bar'
            input_frame.backend_call.stop()
            print 'baz'
            input_frame.backend_call.join()
        root.destroy()

    root = Tk()
    root.wm_protocol ("WM_DELETE_WINDOW", kill_all_threads)
    root.wm_title("Seating Chart Creator")
    centered_window = Frame(root)
    centered_window.pack()

    header_frame = HeaderFrame(centered_window)
    header_frame.grid(row=0, column=0, columnspan=3, sticky=(W))

    instructions_frame = InstructionsFrame(centered_window)
    instructions_frame.grid(row=1, column=0, columnspan=3, padx=(0,20))

    progress_frame = ProgressFrame(centered_window)
    progress_frame.grid(row=2, column=1, padx=10, pady=20, sticky=(N))

    results_frame = ResultsFrame(centered_window, progress_frame.plot_frame)
    results_frame.grid(row=2, column=2, padx=10, sticky=(N))

    input_frame = InputFrame(centered_window, progress_frame, results_frame)
    input_frame.grid(row=2, column=0, padx=(30,20), sticky=(N))

    progress_frame.input_frame = input_frame
    results_frame.input_frame = input_frame
    root.mainloop()  


if __name__ == '__main__':
    main()  
