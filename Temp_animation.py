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

fig = plt.figure()
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
