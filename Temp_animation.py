#---------Imports
from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import Tkinter as Tk
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import interactive
from matplotlib.pylab import subplots, close
import time

from main import main
#---------End of import
#interactive(True)


"""
x = np.arange(0, 2*np.pi, 0.01)        # x-array

def animate(i):
    line.set_ydata(np.sin(x+i/10.0))  # update the data
    print x
    return line,
"""

#label = Tk.Label(root,text="SHM Simulation").grid(column=0, row=0)

#canvas = FigureCanvasTkAgg(fig, master=root)
#canvas.get_tk_widget().grid(column=0,row=1)

fig = plt.figure()
plt.axis([0, 1, 0, 30000])
plt.ion()
plt.show()


x = [1, 2, 3]
y = [1, 2, 3]

gen = main('people.csv', 'tables.csv')
for (bcost, T) in gen:
    x.append(T)
    y.append(bcost)
    plt.scatter(x, y)
    plt.draw()
    time.sleep(0.05)

#ani = animation.FuncAnimation(fig, animate, np.arange(1, 100), interval=25, blit=False)

#Tk.mainloop()
