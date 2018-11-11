from tkinter import *
import gui_package.gui as ui
import gui_package.graph_builder as graph

class OverviewGUI():

    gui = None
    mainframe = None

    temperature = 0.0;
    lux = 0;

    type = "UNKNOWN"
    vartype = IntVar()

    tempText = None
    luxText = None

    def __init__(self, root, type):
        self.type = type
        self.gui = root
        self.build()

    def radioButton(self):
        pass

    def sendSettings(self):
        pass

    def build(self):
        mainframe = self.gui.add_frame(self.gui.notebook, "grey", 0, 0, 1, 1)
        self.mainframe = mainframe

        overviewFrame = self.gui.add_frame(mainframe, "grey", 0, 0, 1, 1)
        settingFrame = self.gui.add_frame(mainframe, "grey", 0, 1, 1, 1)
        graphFrame = self.gui.add_frame(mainframe, "grey", 1, 0, 1, 2)

        graph.build(graphFrame, 'Tijd', 'Temperatuur in ℃',  -20, 50)

        if self.type == "TEMP":
            self.gui.add_label(overviewFrame, "Temperatuur", 0, 0)['padding'] = 8
            self.gui.add_label(overviewFrame, "Min: 0", 1, 0)['padding'] = 8
            self.gui.add_label(overviewFrame, "Max: 0", 1, 1)['padding'] = 8

            self.gui.add_label(overviewFrame, "Status:", 0, 2)['padding'] = 8
            self.gui.add_label(overviewFrame, "Ingerold", 1, 2)['padding'] = 8
            self.gui.add_label(overviewFrame, "Huidig:", 0, 3)['padding'] = 8
            self.tempText = self.gui.add_label(overviewFrame, "20.3 °C", 1, 3)
            self.tempText['padding'] = 8
            self.gui.add_action(self.updateTemp)

        elif self.type == "LIGHT":
            self.gui.add_label(overviewFrame, "Licht", 0, 0)['padding'] = 8
            self.gui.add_label(overviewFrame, "Min: 100", 1, 0)['padding'] = 8
            self.gui.add_label(overviewFrame, "Max: 200", 1, 1)['padding'] = 8

            self.gui.add_label(overviewFrame, "Status:", 0, 2)['padding'] = 8
            self.gui.add_label(overviewFrame, "Ingerold", 1, 2)['padding'] = 8
            self.gui.add_label(overviewFrame, "Huidig:", 0, 3)['padding'] = 8
            self.luxText = self.gui.add_label(overviewFrame, "150 Lux", 1, 3)
            self.luxText['padding'] = 8
            self.gui.add_action(self.updateLight)
        else:
            print("Unkown device type")

        self.gui.add_label(settingFrame, "Min:", 0, 0)['padding'] = 8
        self.gui.add_slider(settingFrame, 0, 100, 1, 0)
        self.gui.add_checkbutton(settingFrame, "Automatisch", 2, 0)

        self.gui.add_label(settingFrame, "Max:", 0, 1)['padding'] = 8
        self.gui.add_slider(settingFrame, 0, 100, 1, 1)
        self.gui.add_radiobutton(settingFrame, "Rol in", self.vartype, 0, self.radioButton, 2, 1)

        self.gui.add_label(settingFrame, "Interval:", 0, 2)['padding'] = 8
        self.gui.add_slider(settingFrame, 0, 100, 1, 2)
        self.gui.add_radiobutton(settingFrame, "Rol out", self.vartype, 1, self.radioButton, 2, 2)

        self.gui.add_button(settingFrame, "Update Settings", 0, 3, self.sendSettings, 3)

        overviewFrame['padding'] = 8
        settingFrame['padding'] = 8

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

    def updateLight(self):
        self.luxText['text'] = "{} Lux".format(self.lux)
