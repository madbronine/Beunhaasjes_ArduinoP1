from tkinter import *
import gui_package.gui as ui

class OverviewGUI():

    gui = None
    tempSlider = None
    tempText = None
    temperature = 1;

    def __init__(self):
        gui = ui.GUI("Centrale", 500, 200)
        self.gui = gui
        self.build()
        self.gui.add_action(self.updateSlider)

    def build(self):
        tempframe = self.gui.add_frame("pink", 0,0)
        lightframe = self.gui.add_frame("cyan", 1,0)

        self.gui.add_label(tempframe, "Temp", 1, 1)
        self.gui.add_button(tempframe, "0024", 2, 1, None)
        self.tempText = self.gui.add_label(tempframe, "##,# °C", 3, 1)

        self.gui.add_label(lightframe, "UV", 1, 2)
        self.gui.add_button(lightframe, "2", 2, 2, None)
        self.gui.add_button(lightframe, "3", 3, 2, None)
        self.gui.add_label(lightframe, "Sun", 4, 2)


        slider = self.gui.add_slider(tempframe, 10.0, 40.0, 2, 3)
        slider['showvalue']=False
        self.tempSlider = slider

    def update(self, temp):
        self.temperature = temp * 0.1

    def updateSlider(self):
        if(self.tempSlider == None):
            return
        self.tempSlider.set(self.temperature)
        self.tempText['text'] = "{} °C".format(self.temperature)
