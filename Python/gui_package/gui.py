from tkinter import *
import threading

class GUI(Frame):

    title = "Untitled"
    sizeX = 50
    sizeY = 50
    root = None
    functions = []

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
            for f in self.functions:
                f()

    def __init__(self, title, sizeX, sizeY):
        self.title = title
        self.sizeX = sizeX
        self.sizeY = sizeY
        uiThread = threading.Thread(target=self.gui_build)
        uiThread.start()
        mainThread = threading.Thread(target=self.gui_main)
        mainThread.start()

    def add_label(self, title, column, row):
        label = Label(self.root, text=title)
        label.grid(column=column, row=row, sticky="nsew")
        return label

    def add_button(self, text, column, row, command):
        button = Button(self.root, text=text, command=command)
        button.grid(column=column, row=row, sticky="nsew")
        return button

    def add_frame(self, background, column, row):
        frame = Frame(self.root, background=background)
        frame.grid(column=column, row=row, sticky="nsew")
        return frame

    def add_slider(self, min, max, column, row):
        scale = Scale(self.root, from_=min, to=max, orient=HORIZONTAL)
        scale.grid(column=column, row=row, columnspan=2, sticky="nsew")
        return scale

    def add_action(self, function):
        self.functions.append(function)
