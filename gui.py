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

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

root.bind('<Return>', run_main)

root.mainloop()
