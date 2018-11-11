from tkinter import *
from random import randint

# these two imports are important
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import time
import threading

continuePlotting = False

def change_state():
    global continuePlotting
    if continuePlotting == True:
        continuePlotting = False
    else:
        continuePlotting = True


def data_points():
    l = []
    for i in range(len(10)):
        l.append(int(10))
    return l

def build(frame, xName, yName, min, max):
    # initialise a window.
    root = Tk()
    root.config(background='white')
    root.geometry("700x700")

    lab = Label(root, text="Live Plotting", bg = 'white').pack()

    fig = Figure()

    ax = fig.add_subplot(111)
    ax.set_xlabel(xName)
    ax.set_ylabel(yName)
    ax.grid()

    graph = FigureCanvasTkAgg(fig, master=root)
    graph.get_tk_widget().pack(side="top",fill='both',expand=True)

    def plotter():
        while continuePlotting:
            ax.cla()
            ax.grid()
            dpts = data_points()
            ax.plot(range(10), dpts, marker='o', color='orange')
            graph.draw()
            time.sleep(1)

    def gui_handler():
        change_state()
        threading.Thread(target=plotter).start()

    b = Button(root, text="Start/Stop", command=gui_handler, bg="red", fg="white")
    b.pack()

    root.mainloop()


build(None, 'Tijd', 'Tempeartuur in ℃',  -20, 50)
