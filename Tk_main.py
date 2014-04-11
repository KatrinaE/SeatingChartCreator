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
from seating_io import write_to_csv        

class ResultsFrame(Frame):
    def __init__(self, parent, plot_frame):
        Frame.__init__(self, parent, bg="white")
        self.parent = parent
        self.plot_frame = plot_frame
        self.initialize()

    def initialize(self):
        self.frame_header = Label(self, text="Solution Metrics:", fg="gray", \
                                  font=("Optima Italic", 24))
        self.frame_header.grid(row=0, column=0, columnspan=2, sticky=(NW), \
                               pady=(20,10))

        self.pairs2_label = Label(self, text="Number of pairs sitting \n" + \
                                    "together twice: ", \
                                    justify=LEFT, fg="gray")
        self.pairs2_label.grid(row=2, column=0, sticky=(W), pady=10)
        self.pairs2_var = StringVar()
        self.pairs2_var.set('__')
        self.pairs2 = Label(self, textvariable=self.pairs2_var, width=10, \
                             fg="gray", font=("Optima bold", 24))
        self.pairs2.grid(row=2, column=1, sticky=(E))


        self.pairs3_label = Label(self, text="Number of pairs sitting \n" + \
                                    "together three times: ", \
                                    justify=LEFT, fg="gray")
        self.pairs3_label.grid(row=3, column=0, sticky=(W), pady=10)
        self.pairs3_var = StringVar()
        self.pairs3_var.set('__')
        self.pairs3 = Label(self, textvariable=self.pairs3_var, width=10, \
                             fg="gray", font=("Optima bold", 24))
        self.pairs3.grid(row=3, column=1, sticky=(E))

        self.trios2_label = Label(self, text="Number of trios sitting \n" + \
                                    "together twice: ", \
                                    justify=LEFT, fg="gray")
        #self.trios2_label.grid(row=4, column=0, sticky=(W), pady=10)
        self.trios2_var = StringVar()
        self.trios2_var.set('__')
        self.trios2 = Label(self, textvariable=self.trios2_var, width=10, \
                             fg="gray", font=("Optima bold", 24))
        #self.trios2.grid(row=4, column=1, sticky=(E))



        self.trios3_label = Label(self, text="Number of trios sitting \n" + \
                                    "together three times: ", \
                                    justify=LEFT, fg="gray")
        #self.trios3_label.grid(row=5, column=0, sticky=(W), pady=10)
        self.trios3_var = StringVar()
        self.trios3_var.set('__')
        self.trios3 = Label(self, textvariable=self.trios3_var, width=10, \
                             fg="gray", font=("Optima bold", 24))
        #self.trios3.grid(row=5, column=1, sticky=(E))

        self.same_spot2_label = Label(self, text="Number of people sitting \n" + \
                                     "in the same spot twice: ", \
                                     justify=LEFT, fg="gray")
        self.same_spot2_label.grid(row=6, column=0, sticky=(W), pady=10)
        self.same_spot2_var = StringVar()
        self.same_spot2_var.set('__')
        self.same_spot2 = Label(self, textvariable=self.same_spot2_var, width=10, \
                             fg="gray", font=("Optima bold", 24))
        self.same_spot2.grid(row=6, column=1, sticky=(E))


        self.same_spot3_label = Label(self, text="Number of people sitting \n" + \
                                     "in the same spot three times: ", \
                                     justify=LEFT, fg="gray")
        self.same_spot3_label.grid(row=7, column=0, sticky=(W), pady=10)
        self.same_spot3_var = StringVar()
        self.same_spot3_var.set('__')
        self.same_spot3 = Label(self, textvariable=self.same_spot3_var, width=10, \
                             fg="gray", font=("Optima bold", 24))
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

    def initialize(self):
        self.frame_header = Label(self, text="Load your files:", foreground="black", \
                                  font=("Optima Italic", 24))
        self.frame_header.grid(row=0, column=0, columnspan=2, sticky=(NW), pady=(20,10), padx=(0,0))

        self.p_filename = StringVar()
        self.t_filename = StringVar()

        # must use lamba - otherwise 'command' executes when the code is loaded,
        # not when the button is pressed
        self.p_entry = ttk.Entry(self, textvariable=self.p_filename, width=20)
        self.p_entry.grid(row=1,column=0, sticky=(W))
        self.p_button = ttk.Button(self, text='Choose People File',\
                                   command=lambda: self.get_filename(self.p_filename))
        self.p_button.grid(row=1, column=1, padx=5, pady=10)

        self.t_entry = ttk.Entry(self, textvariable=self.t_filename, width=20)
        self.t_entry.grid(row=2, column=0, sticky=(W))
        self.t_button = ttk.Button(self, text='Choose Tables File',\
                                   command=lambda: self.get_filename(self.t_filename))
        self.t_button.grid(row=2, column=1, padx=5, pady=10)

        self.submit_button = ttk.Button(self, text='Generate Seating Chart', \
                                        command=lambda: self.generate_results())
        self.submit_button.grid(row=4, column=0, columnspan=2, pady=10)

        self.save_header = Label(self, text="Save your results:", fg="Gray", \
                                  font=("Optima Italic", 24))
        self.save_header.grid(row=6, column=0, columnspan=2, sticky=(NW), \
                               pady=(20,10), padx=(10,10))

        self.save_var = StringVar()
        self.save_var.set('output.csv')
        self.save_entry = ttk.Entry(self, textvariable=self.save_var, width=20, state='disabled')
        self.save_entry.grid(row=7, column=0, pady=10)

        self.save_button_var = StringVar()
        self.save_button_var.set('Save')
        self.save_button = Button(self, textvariable=self.save_button_var, state='disabled',\
                                  command=lambda: self.save_file())
        self.save_button.grid(row=7, column=1, pady=10)

        self.pause_var = StringVar()
        self.pause_var.set('Pause')
        self.pause_button = Button(self, textvariable=self.pause_var, state='disabled',\
                                   command=lambda: self.pause_or_resume(), width=20, height=10, pady=10)
        self.pause_button.grid(row=8, column=1, pady=0)

        self.reset_button = Button(self, text="Reset", state='disabled', \
                                   command = lambda:self.reset(), width=20, \
                                   height=10, pady=10)
        self.reset_button.grid(row=8, column=0)

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
        self.backend_call.join()
        self.switch_to_input_mode()

    def save_file(self):
        write_to_csv(self.solution.solution, self.save_var.get())

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
        self.save_entry.config(state='disabled')
        self.save_button.config(state="disabled")

        self.pause_button.config(state="disabled")
        self.pause_var.set("Pause")
        self.reset_button.config(state="disabled")

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

        self.plot_frame.rects = self.plot_frame.plot.barh((0), (3000), height=1, left=0, linewidth=0, color='white')
        self.plot_frame.canvas.draw()
 
    def switch_to_output_mode(self):
        self.submit_button.config(state='disabled')
        self.frame_header.config(foreground="gray")
        self.p_entry.config(foreground="black", state="disabled")
        self.t_entry.config(foreground="black", state="disabled")
        self.p_button.config(state='disabled')
        self.t_button.config(state='disabled')

        self.save_header.config(foreground="black")
        self.save_entry.config(state='normal')
        self.save_button.config(state="active")

        self.pause_button.config(state="active")
        self.pause_var.set("Resume")
        self.reset_button.config(state="active")

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

        self.pause_button.config(state="active")
        self.pause_var.set("Pause")
        self.pause_button.config(state="normal")
        self.reset_button.config(state="active")

        self.save_header.config(foreground="gray")
        self.save_entry.config(state='disabled')
        self.save_button.config(state="disabled")

        self.progress_frame.plot_frame.title.config(foreground="black")
        self.progress_frame.plot_frame.shield.grid_forget()
        self.progress_frame.num_tries_title.config(foreground="black")
        self.progress_frame.num_tries.config(foreground="violet red")

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
        self.backend_call = ThreadedBackendCall(self.queue)
        self.backend_call.start()
        self.parent.after(2500, self.process_queue)

    def process_queue(self):
        try:
            msg = self.queue.get(0)
            if msg == "Task finished":
                self.backend_call = None
            else:
                self.solution = msg[0]
                iteration = msg[1]
                cost = msg[2]
                quality = 3000-cost # low cost = high quality
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
                self.parent.after(2500, self.process_queue)
        except Queue.Empty:
            self.parent.after(2500, self.process_queue)


class PlotFrame(Frame):
    def __init__(self, parent, title_text, axes_scale, color, y_left, y_right, width=500, height=200, bg="white"):
        Frame.__init__(self, parent, width=1000, height=5000, bg="white")
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
        self.shield = Frame(self, width="6.75i", height="2i", bg="white")
        self.shield.grid(row=1, column=0)

class InstructionsFrame(Frame):
    def __init__(self, parent, width=500, height=200, bg="white"):
        Frame.__init__(self, parent)#, width=width, height=height, bg=bg)
        self.initialize()

    def initialize(self):
        self.instructions_text = \
    """ 
    Seating Chart Creator makes an optimal seating chart for a given set of people, tables, and days. It generates a random chart, then searches for a better one by switching people around.\n
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

class ProgressFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        plot_axes = [0, 3000, 0, 1]
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
        self.num_tries.grid(row=2, column=0, sticky=(S), pady=(20,100))

class ThreadedBackendCall(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self._stop_req = threading.Event()
        self.lock = threading.Lock()
        self.queue = queue

    def run(self):
        max_iterations = math.log(config.T_min)/math.log(config.alpha) \
                         * config.iterations_per_temp
        gen = backend.main_gui("people.csv", "tables.csv")
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
        self.stop()

    def stop(self):
        self._stop_req.set();

def main():

    # helper method used when quitting program
    def kill_all_threads():
        if input_frame.backend_call is not None:
            input_frame.backend_call.stop()
            input_frame.backend_call.join()
        root.destroy()

    root = Tk()
    root.wm_protocol ("WM_DELETE_WINDOW", kill_all_threads)
    centered_window = Frame(root)
    centered_window.pack()

    header_frame = HeaderFrame(centered_window)
    header_frame.grid(row=0, column=0, columnspan=3, sticky=(W))

    instructions_frame = InstructionsFrame(centered_window)
    instructions_frame.grid(row=1, column=0, columnspan=3, sticky=(W), padx=(0,20))

    progress_frame = ProgressFrame(centered_window)
    progress_frame.grid(row=2, column=1, padx=10, pady=20, sticky=(N))

    results_frame = ResultsFrame(centered_window, progress_frame.plot_frame)
    results_frame.grid(row=2, column=2, padx=10, sticky=(N))

    input_frame = InputFrame(centered_window, progress_frame, results_frame)
    input_frame.grid(row=2, column=0, padx=10, sticky=(N))


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
