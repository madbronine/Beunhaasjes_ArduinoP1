from tkinter import *
import gui_package.gui as ui

class OverviewGUI():

    gui = None
    tempSlider = None
    tempText = None
    tempText2 = None
    sunText = None
    sunSlider = None
    statusText = None
    lightIntensitySlider = None
    temperature = 0.1;
    type = "Unknown"
    mainframe = None

    def __init__(self, root, type):
        self.type = type
        self.gui = root
        self.build()
        self.gui.add_action(self.updateSlider)

    def build(self):
        mainframe = self.gui.add_frame(self.gui.notebook, "grey", 0, 0)
        self.mainframe = mainframe

        tempframe = self.gui.add_frame(mainframe, "grey", 0, 0)
        tempSliderFrame = self.gui.add_frame(mainframe, "grey", 1, 0)
        lightSliderFrame = self.gui.add_frame(mainframe, "grey", 2, 0)
        lightIntensityFrame = self.gui.add_frame(mainframe, "grey", 0, 1)
        sunScreenStatusFrame = self.gui.add_frame(mainframe, "grey", 1, 1)

        self.gui.add_label(tempframe, "Gemiddelde temperatuur", 0, 0)['background']="#64B5F6"
        self.tempText = self.gui.add_label(tempframe, "##,# °C", 0, 1)
        self.tempText['anchor']=CENTER
        self.tempText['padding']=8
        self.tempText['font']=("Standard", 24)
        self.tempText['background']="#9be7ff"

        self.tempText2 = self.gui.add_label(tempSliderFrame, "##,# °C", 0, 0)
        slider = self.gui.add_slider(tempSliderFrame, 0.0, 30.0, 0, 1)
        self.tempSlider = slider
        self.tempText2['anchor']=CENTER
        self.tempText2['padding']=8
        self.tempText2['font']=("Standard", 16)
        self.tempText2['background']="#9be7ff"

        self.sunText = self.gui.add_label(lightSliderFrame, "##%", 0, 0)
        sunSlider = self.gui.add_slider(lightSliderFrame, 0.0, 30.0, 0, 1)
        self.sunSlider = sunSlider
        self.sunText['anchor']=CENTER
        self.sunText['padding']=8
        self.sunText['font']=("Standard", 16)
        self.sunText['background']="#9be7ff"

        self.gui.add_label(lightIntensityFrame, "Gem. lichtintensiteit", 0, 0)['background']="#64B5F6"
        self.lightIntensitySlider = self.gui.add_slider(lightIntensityFrame, 0.0, 100.0, 0, 1)

        self.gui.add_label(sunScreenStatusFrame, "Status", 0, 0)['background']="#64B5F6"
        self.statusText = self.gui.add_label(sunScreenStatusFrame, "Open", 0, 1)
        self.statusText['anchor']=CENTER
        self.statusText['padding']=8
        self.statusText['font']=("Standard", 16)
        self.statusText['background']="#9be7ff"

        tempframe['padding'] = 8
        tempSliderFrame['padding'] = 8
        lightSliderFrame['padding'] = 8
        lightIntensityFrame['padding'] = 8
        sunScreenStatusFrame['padding'] = 8

        self.gui.notebook.add(mainframe, text=self.type)

    def update(self, temp):
        self.temperature = temp * 0.1

    def remove(self):
        self.gui.notebook.forget(self.mainframe)

    def updateSlider(self):
        if(self.tempSlider == None):
            return
        self.tempSlider.set(self.temperature)
        self.tempText['text'] = "%.1f °C" % self.temperature
        self.tempText2['text'] = "%.1f °C" % self.temperature
