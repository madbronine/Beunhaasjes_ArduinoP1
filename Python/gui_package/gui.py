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
    notebook = None

    def gui_build(self):
        root = Tk()
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

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
        self.refreshRate = self.refreshRate
        uiThread = threading.Thread(target=self.gui_build)
        uiThread.start()
        mainThread = threading.Thread(target=self.gui_main)
        mainThread.start()

    def add_label(self, root, title, column, row):
        label = ttk.Label(root, text=title)
        label.grid(column=column, row=row, sticky="nsew")
        return label

    def add_button(self, root, text, column, row, command, columnspan, rowspan):
        button = ttk.Button(root, text=text, command=command)
        button.grid(column=column, row=row, columnspan=columnspan, rowspan=rowspan, sticky="nsew")
        return button

    def add_frame(self, root, column, row, columnspan, rowspan):
        frame = ttk.Frame(root)
        frame.grid(column=column, row=row, columnspan=columnspan, rowspan=rowspan, sticky="nsew")
        return frame

    def add_slider(self, root, min, max, column, row, columnspan, rowspan):
        scale = ttk.Scale(root, from_=min, to_=max, orient=HORIZONTAL)
        scale.grid(column=column, row=row, columnspan=columnspan, rowspan=rowspan, sticky="nsew")
        return scale

    def add_radiobutton(self, root, text, var, value, command,column, row):
        radiobutton = ttk.Radiobutton(root, text=text, variable=var, value=value, command=command)
        radiobutton.grid(column=column, row=row, sticky="nsew")
        return radiobutton

    def add_checkbutton(self, root, text, column, row, command):
        checkbutton = ttk.Checkbutton(root, text=text, command=command)
        checkbutton.grid(column=column, row=row, sticky="nsew")
        checkbutton.invoke()
        return checkbutton

    def add_notebook(self):
        notebook = ttk.Notebook(self.root)
        self.notebook = notebook
        notebook.grid(sticky="nsew")
        return notebook

    def add_progressbar(self, root, mode, column, row, width):
        progressbar = ttk.Progressbar(root, mode=mode)
        progressbar.grid(column=column, row=row, columnspan=width, sticky="nsew")
        return progressbar

    def add_action(self, function):
        self.functions.append(function)
