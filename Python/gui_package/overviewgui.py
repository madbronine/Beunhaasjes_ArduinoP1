from tkinter import *
import gui_package.gui as ui
import gui_package.graph_builder as graph

class OverviewGUI():

    main = None
    device = None

    gui = None
    mainframe = None

    temperature = 0.0;
    lux = 0;

    type = "UNKNOWN"

    tempText = None
    luxText = None

    minslider = None
    maxslider = None
    intervalslider = None

    min = 0
    max = 0
    interval = 300
    rolUp = True
    automatic = True

    sunscreenStatus = "Ingerold"

    def __init__(self, root, type, device):
        self.type = type
        self.gui = root
        self.vartype = IntVar()
        self.build()
        self.device = device

    def radioButton(self):
        self.rolUp = not self.rolUp
        print(self.rolUp)

    def sendSettings(self):
        self.min = minslider
        if self.automatic:
            print("Automatic")
        else:
            print(self.rolUp)
        #self.main.sendSettings(self.device, self.min, self.max, self.automatic, self.rolUp)

    def build(self):
        mainframe = self.gui.add_frame(self.gui.notebook, "grey", 0, 0, 1, 1)
        self.mainframe = mainframe

        overviewFrame = self.gui.add_frame(mainframe, "grey", 0, 0, 1, 1)
        settingFrame = self.gui.add_frame(mainframe, "grey", 0, 1, 1, 1)
        graphFrame = self.gui.add_frame(mainframe, "grey", 1, 0, 1, 2)

        graph.build(graphFrame, 'Tijd', 'Temperatuur in ℃',  -20, 50)

        if self.type == "TEMP":
            self.gui.add_label(overviewFrame, "Temperatuur", 0, 0)['padding'] = 8
            self.tempText = self.gui.add_label(overviewFrame, "20.3 °C", 1, 3)
            self.tempText['padding'] = 8
            self.gui.add_action(self.updateTemp)

        elif self.type == "LIGHT":
            self.gui.add_label(overviewFrame, "Licht", 0, 0)['padding'] = 8
            self.luxText = self.gui.add_label(overviewFrame, "150 Lux", 1, 3)
            self.luxText['padding'] = 8
            self.gui.add_action(self.updateLight)
        else:
            print("Unkown device type")

        self.gui.add_label(overviewFrame, "Min: 100", 1, 0)['padding'] = 8
        self.gui.add_label(overviewFrame, "Max: 200", 1, 1)['padding'] = 8

        self.gui.add_label(overviewFrame, "Status:", 0, 2)['padding'] = 8
        self.gui.add_label(overviewFrame, "Ingerold", 1, 2)['padding'] = 8
        self.gui.add_label(overviewFrame, "Huidig:", 0, 3)['padding'] = 8

        self.gui.add_label(settingFrame, "Min:", 0, 0)['padding'] = 8
        self.minslider = self.gui.add_slider(settingFrame, 0, 100, 1, 0)
        self.gui.add_checkbutton(settingFrame, "Automatisch", 2, 0, self.checkbox)

        self.gui.add_label(settingFrame, "Max:", 0, 1)['padding'] = 8
        self.maxslider = self.gui.add_slider(settingFrame, 0, 100, 1, 1)
        self.gui.add_radiobutton(settingFrame, "Rol in", self.vartype, 0, self.radioButton, 2, 1)

        self.gui.add_label(settingFrame, "Interval:", 0, 2)['padding'] = 8
        self.gui.add_slider(settingFrame, 0, 100, 1, 2)
        self.gui.add_radiobutton(settingFrame, "Rol out", self.vartype, 1, self.radioButton, 2, 2)

        self.gui.add_button(settingFrame, "Update Settings", 0, 3, self.sendSettings, 3)

        overviewFrame['padding'] = 8
        settingFrame['padding'] = 8
        graphFrame['padding'] = 8

        self.gui.notebook.add(mainframe, text=self.type)

    def update(self, value):
        if self.type == "TEMP":
            self.temperature = value * 0.1
        elif self.type == "LIGHT":
            self.lux = lux

    def remove(self):
        self.gui.notebook.forget(self.mainframe)

    def updateTemp(self):
        self.tempText['text'] = "%.1f °C" % self.temperature

    def checkbox(self):
        # self.tempText['text'] = "%.1f °C" % self.temperature
        pass

    def updateLight(self):
        self.luxText['text'] = "{} Lux".format(self.lux)
