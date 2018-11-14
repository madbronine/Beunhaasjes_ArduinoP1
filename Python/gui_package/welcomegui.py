from tkinter import *
import gui_package.gui as ui

class WelcomeGUI():

    gui = None
    mainframe = None
    amount = 0

    def __init__(self, root):
        self.gui = root
        self.build()

    def build(self):
        mainframe = self.gui.add_frame(self.gui.notebook, 0, 0, 1, 1)
        self.mainframe = mainframe
        self.mainframe.grid_columnconfigure(0, weight=1)
        self.mainframe.grid_rowconfigure(0, weight=1)

        self.searchingframe = self.gui.add_frame(mainframe, 0, 2, 1, 1)
        self.searchingframe.grid_columnconfigure(0, weight=1)
        self.searchingframe.grid_rowconfigure(0, weight=1)
        self.searchingframe.grid_rowconfigure(1, weight=1)
        label = self.gui.add_label(self.mainframe, "Welkom!", 0, 0)
        label['padding'] = 8
        label['font'] = ("unspecified", 24)
        label['anchor'] = CENTER
        label = self.gui.add_label(self.mainframe, "Sluit een module aan.\nHet programma herkent de aangesloten module automatisch.\nWanneer een module is gevonden zal er een nieuw tabblad bijkomen met als titel het type module", 0, 1)
        label['anchor'] = CENTER
        label['padding'] = 24
        self.connectionlabel = self.gui.add_label(self.searchingframe, "Zoeken naar apparaten... (0 connected)", 0, 0)
        self.connectionlabel['padding'] = 8
        self.connectionlabel['anchor'] = CENTER
        progressbar = self.gui.add_progressbar(self.searchingframe, "indeterminate", 0, 1, 1)
        progressbar.start(10)
        self.gui.notebook.add(mainframe, text="Welkom")

    def update(self, value):
        if value == None:
            return

        if self.type == "TEMP":
            self.temperature = value * 0.1
        elif self.type == "LIGHT":
            self.lux = value

    def device_amount(self, amount):
        if self.amount == 0:
            fromZero = True
        else:
            fromZero = False

        self.amount = amount
        self.connectionlabel['text']="Zoeken naar apparaten... ({} connected)".format(amount)
        if amount > 0:
            if fromZero == True:
                self.gui.notebook.select(1)
        #     self.searchingframe.grid_remove()
        # else:
        #     self.searchingframe.grid()
