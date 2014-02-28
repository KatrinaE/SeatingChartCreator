import config

def thingy(people_csv, tables_csv):
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
    import math

    from main import main

    fig = plt.figure()
    num_iterations = math.log(config.T_min)/math.log(config.alpha)    
    plt.axis([0, num_iterations, 0, 30000])
    plt.ion()
    plt.show()

    x = []
    y = []

    gen = main('people.csv', 'tables.csv')#people_csv, tables_csv)
    for (bcost, T) in gen:
        iteration = math.log(T)/math.log(config.alpha)
        x.append(iteration)
        y.append(bcost)
        plt.scatter(x, y)
        plt.draw()
        time.sleep(0.05)
