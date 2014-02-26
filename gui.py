from Tkinter import *
import ttk

import main

def run_main(*args):
    try:
        main.main(people_filename.get(), tables_filename.get())
    except ValueError:
        pass

root = Tk()
root.title("Seating Chart Creator")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

tables_filename = StringVar()
people_filename = StringVar()

tables_label = ttk.Label(mainframe, text="Tables")
tables_entry = ttk.Entry(mainframe, width=15, \
                         textvariable=tables_filename)
people_label = ttk.Label(mainframe, text="People")
people_entry = ttk.Entry(mainframe, width=15, \
                         textvariable=people_filename)
tables_label.grid()
tables_entry.grid()
people_label.grid()
people_entry.grid()

tables_button = ttk.Button(mainframe, text="Create", command=run_main)
tables_button.grid()

# display typing on screen
#tables_output = ttk.Label(mainframe, textvariable=tables_filename)
#people_output = ttk.Label(mainframe, textvariable=people_filename)

import matplotlib
matplotlib.use('TKAgg')
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def data_gen():
    t = data_gen.t
    cnt = 0
    while cnt < 1000:
        cnt+=1
        t += 0.05
        yield t, np.sin(2*np.pi*t) * np.exp(-t/10.)
data_gen.t = 0

fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)
ax.set_ylim(-1.1, 1.1)
ax.set_xlim(0, 5)
ax.grid()
xdata, ydata = [], []
def run(data):
    # update the data
    t,y = data
    xdata.append(t)
    ydata.append(y)
    xmin, xmax = ax.get_xlim()

    if t >= xmax:
        ax.set_xlim(xmin, 2*xmax)
        ax.figure.canvas.draw()
    line.set_data(xdata, ydata)

    return line,

ani = animation.FuncAnimation(fig, run, data_gen, blit=True, interval=10,
    repeat=False)
plt.show()


for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

root.bind('<Return>', run_main)

root.mainloop()
