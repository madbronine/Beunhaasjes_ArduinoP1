from tkinter import *
from tkinter import ttk
import threading
import time

class GUI():

    title = "Untitled"
    sizeX = 50
    sizeY = 50
    root = None
    functions = []
    refreshRate = 60

    def gui_build(self):
        root = Tk()
        for i in range(0,10):
            root.columnconfigure(i, weight=1)
            root.rowconfigure(i, weight=1)

        self.root = root
        root.title(self.title)
        root.minsize(self.sizeX, self.sizeY)
        root.mainloop()

    def gui_main(self):
        while(True):
            time.sleep(self.refreshRate)
            for f in self.functions:
                f()

    def __init__(self, title, sizeX, sizeY):
        self.title = title
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.refreshRate = 1 / self.refreshRate
        uiThread = threading.Thread(target=self.gui_build)
        uiThread.start()
        mainThread = threading.Thread(target=self.gui_main)
        mainThread.start()

    def add_label(self, root, title, column, row):
        label = ttk.Label(root, text=title)
        label.grid(column=column, row=row, sticky="nsew")
        return label

    def add_button(self, root, text, column, row, command):
        button = ttk.Button(root, text=text, command=command)
        button.grid(column=column, row=row, sticky="nsew")
        return button

    def add_frame(self, background, column, row):
        frame = ttk.Frame(self.root)
        frame.grid(column=column, row=row, sticky="nsew")
        return frame

    def add_slider(self, root, min, max, column, row):
        scale = ttk.Scale(root, from_=min, to_=max, orient=HORIZONTAL)
        scale.grid(column=column, row=row, sticky="nsew")
        return scale

    def add_action(self, function):
        self.functions.append(function)
